# UncertEx: Currency Converter with Uncertainty

UncertEx is a command-line application that performs currency conversion while accounting for uncertainty in the exchange rate. It uses the Signaloid Cloud Engine API to perform underlying computations in the cloud.

## Features

- Convert between currencies with a specified range for the exchange rate
- Utilize Signaloid's uncertainty-aware computing capabilities
- Display statistical information about the distribution of the converted value
- Option to output results in JSON format

## Understanding Currency Conversion with Rate Ranges

UncertEx uses a range of exchange rates rather than a single fixed rate. Here's why this approach is valuable:

1. **Acknowledging Uncertainty**: Exchange rates fluctuate due to various economic and political factors. Using a range accounts for this variability.

2. **Realistic Planning**: Whether for travel, business, or financial analysis, considering a range of possible rates provides a more comprehensive view of potential outcomes.

3. **Risk Assessment**: This approach helps in understanding the potential variability in the value of your money when converted, allowing for better risk management.

4. **Practical Applications**:
   - Financial Planning: Businesses can budget for best and worst-case scenarios in international deals.
   - Travel Budgeting: Travelers can estimate a range for their budget in a foreign currency.
   - Economic Analysis: Analysts can model potential outcomes in international trade or investments.

5. **Example**: Converting £1000 to EUR
   - Fixed rate: Might give you exactly €1180
   - Range approach: Might show your £1000 could be worth between €1150 to €1200, depending on rate fluctuations

By using UncertEx, you gain insights into not just a single conversion value, but a distribution of possible values, helping you make more informed decisions in situations involving different currencies.

## Prerequisites

- Python 3.7 or higher
- A Signaloid API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/iamramtin/uncertex.git
   cd uncertex
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Signaloid API Key and Signaloid Core ID as environment variables:
   ```
   export SIGNALOID_API_KEY="your_api_key_here"
   export SIGNALOID_CORE_ID="your_core_id_here"
   ```

## Usage

Run the script with the following command:

```
python uncertex.py <amount> [options]
```

Options:
- `-f`, `--from`: Source currency (default: GBP)
- `-t`, `--to`: Target currency (default: EUR)
- `--min-rate`: Minimum conversion rate (default: 1.15)
- `--max-rate`: Maximum conversion rate (default: 1.20)
- `--json`: Output results as JSON

Examples:

1. Basic usage:
   ```
   python uncertex.py 100 --from GBP --to EUR --min-rate 1.15 --max-rate 1.20
   ```

2. Output results as JSON:
   ```
   python uncertex.py 100 --from GBP --to EUR --min-rate 1.15 --max-rate 1.20 --json
   ```

## Output

By default, the application will display:
- The input amount and currencies
- The average conversion rate and result
- Statistical information about the distribution of the converted value, including:
  - Mean
  - Median
  - Standard Deviation
  - Minimum and Maximum values
  - 10th, 25th, 75th, and 90th percentiles

When the `--json` option is used, the output will be a JSON object containing all of the above information in a structured format.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Signaloid for providing the Cloud Engine API for uncertainty-aware computing