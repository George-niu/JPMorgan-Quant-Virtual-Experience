import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np


# Load data
df = pd.read_csv('Nat_Gas.csv' , parse_dates=['Dates'])
print(df.head())

# Visualize and observe trends
plt.figure(figsize=(10, 5))
plt.plot(df['Dates'], df['Prices'], marker ='o')
plt.title('Natural Gas Prices Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.show()

from sklearn.linear_model import LinearRegression

# Convert the date to a number
df['Ordinal_Dates'] = df['Dates'].map(datetime.toordinal)

# Fit a Linear Trend
X = df[['Ordinal_Dates']]
y = df['Prices']
model = LinearRegression().fit(X, y)

def get_predicted_price(target_date):
    """
    Enter a date to return the predicted price
    Principle: Linear trend + sine function 
    to simulate seasonal fluctuations 
    """
    target_ordinal = target_date.toordinal()
    
    # Calculating the linear trend section
    trend = model.predict([[target_ordinal]])[0]

    # Calculate the seasonal component
    amplitude = 1.0
    day_of_year = target_date.timetuple().tm_yday
    seasonality = amplitude * np.sin(2 * np.pi * (day_of_year - 200) / 365)

    return trend + seasonality

# Test
test_date = datetime(2025, 12, 15)
print(f"Predicted price for {test_date.date()}: &{get_predicted_price(test_date):.2f}")


def calculate_contract_value(injection_dates, withdrawal_dates, quantities,
                             storage_rate=0.1, transport_cost=0.05):
    """
    injection_dates: List of purchase dates
    withdrawal_dates: List of sale dates
    quantities: Transaction volume for each batch
    storage_rate: Storage cost per unit per month
    """

    total_value = 0
    for inj_date, wit_date, qty in zip(injection_dates, withdrawal_dates, quantities):
        p_buy = get_predicted_price(inj_date)
        p_sell = get_predicted_price(wit_date)

        # Calculating Storage Days and Costs
        days_stored = (wit_date - inj_date).days
        cost_storage = (days_stored / 30) * storage_rate * qty
        cost_transport = transport_cost * qty * 2

        # Net Income
        revenue = (p_sell - p_buy) * qty
        net_profit = revenue - cost_storage - cost_transport
        total_value += net_profit

        print(f"Transaction details: Buy ${p_buy:.2f}, Sell &{p_sell:.2f}, Profit: ${net_profit:.2f}")

    return total_value

# test
inj = [datetime(2025, 6, 1)]     
wit = [datetime(2025, 12, 15)]    
q = [1000]                       

final_profit = calculate_contract_value(inj, wit, q)
print(f"\nTotal contract value: ${final_profit:.2f}")