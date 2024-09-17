"""
UncertEx: Currency Converter with Uncertainty

This script provides a command-line interface for currency conversion
with uncertainty using the Signaloid Cloud Engine API.

Usage:
    python uncertex.py <amount> [options]

Options:
    -f, --from: Source currency (default: GBP)
    -t, --to: Target currency (default: EUR)
    -v, --variance: Variance in exchange rate as a percentage (default: 2.0)
    -j, --json: Output results as JSON

Example:
    python uncertex.py 100 --from GBP --to EUR --min-rate 1.15 --max-rate 1.20 --json

Author: Ramtin Mesgari
Date: September 2024
Version: 1.0
"""

import os
import time
import json
import re
import argparse
import requests
import numpy as np
from enum import Enum


SIGNALOID_API_URL = "https://api.signaloid.io"
SIGNALOID_API_KEY = os.environ.get("SIGNALOID_API_KEY")
SIGNALOID_CORE_ID = os.environ.get("SIGNALOID_CORE_ID")
EXCHANGE_RATE_API_URL = "https://api.exchangerate-api.com/v4/latest"
EXCHANGE_RATE_API_KEY = os.environ.get("EXCHANGE_RATE_API_KEY")


class TaskStatus(Enum):
    """Enum representing possible task statuses."""
    BUILDING = "Building"
    IN_PROGRESS = 'In Progress'
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    STOPPED = "Stopped"


def get_args() -> argparse.Namespace:
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(description="UncertEx: Currency Converter with Uncertainty")
    parser.add_argument('amount', type=float, help='Amount to convert')
    parser.add_argument('-f', '--from', dest='from_currency', default='GBP', help='Source currency (default: GBP)')
    parser.add_argument('-t', '--to', dest='to_currency', default='EUR', help='Target currency (default: EUR)')
    parser.add_argument('--min-rate', type=float, default=1.15, help='Minimum conversion rate')
    parser.add_argument('--variance', type=float, default=2.0, help='Variance in exchange rate as a percentage (default: 2.0)')
    parser.add_argument('-j', '--json', action='store_true', help='Output results as JSON')
    
    return parser.parse_args()


def create_task_object(amount: float, rate: float, variance: float) -> dict[str, any]:
    """Create a task object with the given parameters for the Signaloid API."""
    min_rate = rate * (1 - variance/100)
    max_rate = rate * (1 + variance/100)
    
    source_code = f'''
        #include <math.h>
        #include <stdint.h>
        #include <stdio.h>
        #include <uxhw.h>

        int main() {{
            double amount = {amount};
            double rate = UxHwDoubleUniformDist({min_rate}, {max_rate});
            double result = amount * rate;

            printf("{{\\n");
            printf("  \\"amount\\": %.2f,\\n", amount);
            printf("  \\"rate\\": %.4f,\\n", rate);
            printf("  \\"result\\": %.2f\\n", result);
            printf("}}\\n");
 
            return 0;
        }}
    '''
    
    return {
        "Type": "SourceCode",
        "SourceCode": {
            "Object": "SourceCode",
            "Code": source_code,
            "Arguments": "",
            "Language": "C"
        },
        "Overrides": {
            "Core": SIGNALOID_CORE_ID
        }
    }


def get_exchange_rates(from_currency: str, to_currency: str) -> dict[str, float]:
    """Retrieve current exchange rates from the API."""
    response = requests.get(f"{EXCHANGE_RATE_API_URL}/{from_currency}?api_key={EXCHANGE_RATE_API_KEY}")

    if response.status_code == 200:
        data = response.json()
        return data['rates'][to_currency]
    else:
        raise Exception(f"Failed to fetch exchange rates. Status code: {response.status_code}")


def create_task(task_object: dict[str, any]) -> dict[str, any]:
    """Create a new task with the given payload using the Signaloid API."""
    headers = {"Authorization": SIGNALOID_API_KEY, "Content-Type": "application/json"}
    response = requests.post(f"{SIGNALOID_API_URL}/tasks", headers=headers, json=task_object)

    if response.status_code == 202:
        return response.json()
    else:
        raise Exception(f"Failed to create task. Status code: {response.status_code}. {response.json()}")


def get_task_status(task_id: str) -> dict[str, any]:
    """Retrieve the task status from the Signaloid API."""
    headers = {"Authorization": SIGNALOID_API_KEY}
    response = requests.get(f"{SIGNALOID_API_URL}/tasks/{task_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get task status. Status code: {response.status_code}")


def get_task_output(task_id: str) -> dict[str, any]:
    """Retrieve the task output from the Signaloid API."""
    headers = {"Authorization": SIGNALOID_API_KEY}
    response = requests.get(f"{SIGNALOID_API_URL}/tasks/{task_id}/outputs?sanitized=false", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get task output. Status code: {response.status_code}")


def wait_for_task_completion(task_id: str, max_wait_time: int = 60, check_interval: int = 5) -> TaskStatus:
    """Wait for the task to complete, checking periodically."""
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        task_status = get_task_status(task_id)
        status = TaskStatus(task_status['Status'])

        if status in {TaskStatus.COMPLETED, TaskStatus.CANCELLED, TaskStatus.STOPPED}:
            return status
        
        print("Specified task is still in progress. Waiting...")
        time.sleep(check_interval)
    
    raise Exception("Task timed out")


def handle_request(url: str) -> str:
    """Handle a request to the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        return response.content.decode('utf-8')
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return ""


def extract_value(ux_string: str) -> float:
    """Extract the numerical value from a Ux string."""
    match = re.match(r'(\d+\.\d+)Ux', ux_string)
    
    if match:
        return float(match.group(1))
    return None


def parse_custom_json(json_string: str) -> dict[str, any]:
    """Parse the custom JSON format with Ux values."""
    # Replace Ux values with string representations
    json_string = re.sub(r'(\d+\.\d+Ux[0-9A-Fa-f]+)', r'"\1"', json_string)
    
    # Parse the modified JSON string
    data = json.loads(json_string)
    
    # Extract numerical values from Ux strings
    for key in data:
        if isinstance(data[key], str) and data[key].startswith(tuple('0123456789')) and 'Ux' in data[key]:
            data[key] = extract_value(data[key])
    
    return data


def generate_samples(mean: float, min_rate: float, max_rate: float, num_samples: int = 10000) -> np.ndarray:
    """Generate samples based on uniform distribution of rates."""
    rates = np.random.uniform(min_rate, max_rate, num_samples)
    return mean * rates


def format_output_as_json(amount: float, min_rate: float, max_rate: float, from_currency: str, to_currency: str, 
                          rate: float, result: float, samples: np.ndarray) -> dict[str, any]:
    """Format the output results as a JSON-serializable dictionary."""
    return {
        "input": {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "min_rate": min_rate,
            "max_rate": max_rate
        },
        "output": {
            "average_rate": rate,
            "average_result": result,
            "distribution": {
                "mean": float(np.mean(samples)),
                "median": float(np.median(samples)),
                "standard_deviation": float(np.std(samples)),
                "minimum": float(np.min(samples)),
                "maximum": float(np.max(samples)),
                "percentiles": {
                    "10th": float(np.percentile(samples, 10)),
                    "25th": float(np.percentile(samples, 25)),
                    "75th": float(np.percentile(samples, 75)),
                    "90th": float(np.percentile(samples, 90))
                }
            }
        }
    }


def process_task_output(task_status: TaskStatus, task_output: dict[str, str], 
                        from_currency: str, to_currency: str, rate: float, variance: float, 
                        json_output: bool) -> None:
    """Process and display the task output."""
    if task_status == TaskStatus.COMPLETED:
        url = task_output['Stdout']
        decoded_response = handle_request(url)
        
        if decoded_response:
            try:
                stdout_response = parse_custom_json(decoded_response)
                amount = stdout_response['amount']
                result = stdout_response['result']

                min_rate = rate * (1 - variance/100)
                max_rate = rate * (1 + variance/100)
                samples = generate_samples(amount, min_rate, max_rate)
                
                if json_output:
                    output = format_output_as_json(amount, min_rate, max_rate, from_currency, to_currency, rate, result, samples)
                    print(json.dumps(output, indent=2))
                else:
                    print(f"\nAmount: {amount:.2f} {from_currency}")
                    print(f"Average Rate: {rate:.4f} (±{variance}%)")
                    print(f"Average Result: {result:.2f} {to_currency}")
                    
                    mean = np.mean(samples)
                    median = np.median(samples)
                    stdev = np.std(samples)
                    min_val = np.min(samples)
                    max_val = np.max(samples)
                    
                    print(f"\nDistribution of converted value in {to_currency}:")
                    print(f"  Mean: {mean:.2f}")
                    print(f"  Median: {median:.2f}")
                    print(f"  Standard Deviation: {stdev:.2f}")
                    print(f"  Minimum: {min_val:.2f}")
                    print(f"  Maximum: {max_val:.2f}")
                    
                    percentiles = [10, 25, 75, 90]
                    print("\nPercentiles:")
                    for p in percentiles:
                        value = np.percentile(samples, p)
                        print(f"  {p}th: {value:.2f}")
            except Exception as e:
                print(f"Error processing output: {e}")
                print("Raw output:")
                print(decoded_response)
    
    elif task_status == TaskStatus.CANCELLED:
        url = task_output['Stderr']
        decoded_response = handle_request(url)
        
        if decoded_response:
            print(f"\nError:\n{decoded_response}")
    
    else:
        url = task_output['Build']
        decoded_response = handle_request(url)
        
        if decoded_response:
            print(f"\nBuild issue:\n{decoded_response}")


def main() -> None:
    """Main function to execute the currency conversion."""
    print("Welcome to UncertEx: Currency Converter with Uncertainty")
    args = get_args()
    
    try:
        rate = get_exchange_rates(args.from_currency, args.to_currency)
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return
    
    if not args.json:
        print(f"\nConverting {args.amount} {args.from_currency} to {args.to_currency}")
        print(f"Current exchange rate: 1 {args.from_currency} = {rate:.4f} {args.to_currency}")
        print(f"Using a variance of ±{args.variance}%")
    
    task_object = create_task_object(args.amount, rate, args.variance)
    task = create_task(task_object)
    task_id = task['TaskID']
    
    if not args.json:
        print(f"\nTask submitted successfully with ID: {task_id}")
    
    task_status = wait_for_task_completion(task_id)
    
    if not args.json:
        print(f"Task completed with status: {task_status.value}.")
    
    task_output = get_task_output(task_id)
    process_task_output(task_status, task_output, args.from_currency, args.to_currency, rate, args.variance, args.json)


if __name__ == "__main__":
    main()