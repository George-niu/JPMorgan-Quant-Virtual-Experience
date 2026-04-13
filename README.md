# JPMorgan Chase - Quantitative Research Virtual Experience

This repository contains my solutions for the JPMorgan Chase Quantitative Research Virtual Experience program, focusing on commodity trading, data analysis, and financial modeling for the natural gas market.

## Task 1：Natural Gas Price Prediction
* Analyzed historical natural gas price data and extrapolated trends one year into the future.
* Used the `pandas` library to clean, store, and manipulate the historical dataset.
* Created a `matplotlib` plot to visualize price trends and identify strong seasonal patterns.
* Built a predictive function using Scikit-Learn's `LinearRegression` combined with a sine wave transformation to accurately model both the long-term linear trend and the short-term seasonal fluctuations of natural gas prices.

## Task 2: Commodity Storage Contract Pricing Model
* Developed a prototype pricing model in Python to evaluate the fair value of a natural gas seasonal arbitrage contract.
* Integrated the predictive model from Task 1 to dynamically forecast purchase (injection) and sale (withdrawal) prices based on client-specified dates.
* Implemented comprehensive cash flow logic to calculate net profit by factoring in gross revenue, gas purchase expenses, fixed monthly storage fees, injection/withdrawal rates, and transportation costs.
* Engineered constraint checks to enforce physical facility limitations, ensuring trade volumes do not exceed maximum storage capacity and accurately accounting for daily injection/withdrawal rate limits.
* Executed boundary testing with sample trade batches to validate the model's robustness and accuracy before potential deployment by the trading desk.
