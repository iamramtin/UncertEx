# UncertEx: Currency Converter with Uncertainty

UncertEx is a command-line application that performs currency conversion while accounting for uncertainty in the exchange rate. It uses the Signaloid Cloud Engine API to perform underlying computations in the cloud.

## Features

- Convert between currencies with a specified range for the exchange rate
- Utilize Signaloid's uncertainty-aware computing capabilities
- Display statistical information about the distribution of the converted value
- Option to output results in JSON format

## Understanding Currency Conversion with Uncertainty

UncertEx uses a range of exchange rates rather than a single fixed rate. Here's why this approach is valuable:

1. **Acknowledging Uncertainty**: Exchange rates fluctuate due to various economic and political factors. Using a range accounts for this variability.

2. **Realistic Planning**: Whether for travel, business, or financial analysis, considering a range of possible rates provides a more comprehensive view of potential outcomes.

3. **Risk Assessment**: This approach helps in understanding the potential variability in the value of your money when converted, allowing for better risk management.

4. **Practical Applications**:
   - Financial Planning: Businesses can budget for best and worst-case scenarios in international deals.
   - Travel Budgeting: Travelers can estimate a range for their budget in a foreign currency.
   - Economic Analysis: Analysts can model potential outcomes in international trade or investments.

5. **Example**: Converting 1000 GBP to EUR
   - Fixed rate: Might give you exactly 1180 GBP
   - Range approach: Might show your 1000 GBP could be worth between 1150 GBP to 1200 GBP, depending on rate fluctuations

By using UncertEx, you gain insights into not just a single conversion value, but a distribution of possible values, helping you make more informed decisions in situations involving different currencies.

### Understanding Variance in UncertEx

In UncertEx, we use the concept of "variance" to represent the potential fluctuation or uncertainty in the exchange rate. Here's what you need to know:

- **What is Variance?**: It's a percentage that represents the possible deviation from the current exchange rate.
- **How it Works**: 
  - If the current rate is 1 USD = 0.85 EUR and the variance is 2%,
  - The possible range of rates would be 0.833 EUR to 0.867 EUR (0.85 ± 2%).
- **Why it Matters**: 
  - Reflects Real-World Volatility: Exchange rates aren't fixed and can fluctuate.
  - Enables Risk Assessment: Helps you understand the potential variability in your conversion.
  - Aids in Planning: Knowing the range of possible outcomes is often more valuable than a single estimate.

By adjusting the variance, you can model different levels of market volatility or uncertainty in your conversions.

## Prerequisites

- Python 3.7 or higher
- A Signaloid API key
- An API key for the exchange rate API (e.g., ExchangeRate-API)

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

3. Set up your API keys and IDs as environment variables:
   ```
   export SIGNALOID_API_KEY="your_api_key_here"
   export SIGNALOID_CORE_ID="your_core_id_here"
   export EXCHANGE_RATE_API_KEY="your_exchange_rate_api_key_here"
   ```

## Usage

Run the script with the following command:

```
python uncertex.py <amount> [options]
```

Options:
- `-f`, `--from`: Source currency (default: USD)
- `-t`, `--to`: Target currency (default: EUR)
- `--variance`: Variance in exchange rate as a percentage (default: 2.0)
- `--json`: Output results as JSON

Examples:

1. Basic usage:
   ```
   python uncertex.py 100 --from GBP --to EUR --variance 2.0
   ```

2. Convert between any supported currencies:
   ```
   python uncertex.py 1000 --from JPY --to ZAR --variance 1.5
   ```

3. Output results as JSON:
   ```
   python uncertex.py 500 --from CAD --to AUD --variance 2.5 --json
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

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Acknowledgments

- Signaloid for providing the Cloud Engine API for uncertainty-aware computing
- ExchangeRate-API for providing real-time exchange rate data