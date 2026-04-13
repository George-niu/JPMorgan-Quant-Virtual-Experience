import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression

# Load data and train the prediction model
df = pd.read_csv('Nat_Gas.csv', parse_dates=['Dates'])
df['Ordinal_Dates'] = df['Dates'].map(datetime.toordinal)

X = df[['Ordinal_Dates']]
y = df['Prices']
model = LinearRegression().fit(X, y)

# Forecast future prices based on linear trends and seasonality
def get_predicted_price(target_date):
    target_ordinal = target_date.toordinal()
    trend = model.predict([[target_ordinal]])[0]

    amplitude = 1.0
    day_of_year = target_date.timetuple().tm_yday
    seasonality = amplitude * np.sin(2 * np.pi * (day_of_year - 200) / 365)

    return trend + seasonality


# Pricing Model
def calculate_contract_value(
        injection_dates,
        withdrawal_dates,
        target_volumes,
        max_volume,
        rate_limit,
        storage_cost_per_month, 
        injection_cost_per_unit=0.0, 
        withdrawal_cost_per_unit=0.0, 
        transport_cost_per_unit=0.0
):
    """
    Calculate the fair value of the natural gas storage contract (considering all cash flows)
    
    Parameters:
    injection_dates: list, injection (purchase) dates
    withdrawal_dates: list, withdrawal (sale) dates
    target_volumes: list, target transaction volumes for each batch
    max_volume: float, maximum physical storage capacity limit
    rate_limit: float, maximum daily injection/withdrawal rate
    storage_cost_per_month: float, fixed monthly storage cost per unit
    injection_cost_per_unit: float, cost to inject 1 unit of gas
    withdrawal_cost_per_unit: float, cost to withdraw 1 unit of gas
    transport_cost_per_unit: float, one-way transport cost per unit
    """
    total_contract_value = 0

    for i in range(len(injection_dates)):
        inj_date = injection_dates[i]
        wit_date = withdrawal_dates[i]
        volume = target_volumes[i]

        # Maximum capacity limit
        if volume > max_volume:
            print(f"Warning: Planned Trading Volume {volume} Exceeded the maximum capacity {max_volume}. Will be calculated based on maximum capacity.")
            volume = max_volume

        # Rate Limiting and Time Verification
        days_to_inject = np.ceil(volume / rate_limit)
        days_to_withdraw = np.ceil(volume / rate_limit)
        days_stored = (wit_date - inj_date).days

        if days_stored <= 0:
            print(f"Error: Extraction Date ({wit_date.date()}) Must be later than the injection date ({inj_date.date()}). Jump")
            continue

        # Get predicted price
        price_buy = get_predicted_price(inj_date)
        price_sell = get_predicted_price(wit_date)

        # Cash Outflows
        months_stored = days_stored / 30.0
        cost_storage = months_stored * storage_cost_per_month * volume   # Storage rental fee
        cost_injection = injection_cost_per_unit * volume                # Injection fee
        cost_withdrawal = withdrawal_cost_per_unit * volume              # Withdrawal fee
        cost_transport = transport_cost_per_unit * volume * 2            # Round-trip transport fee

        total_cost = cost_storage + cost_injection + cost_withdrawal + cost_transport

        # Trade Cash Flows
        expense_gas = price_buy * volume    # Cost of buying gas (outflow)
        revenue_gas = price_sell * volume   # Revenue from selling gas (inflow)

        # Net Value
        net_profit = revenue_gas - expense_gas - total_cost
        total_contract_value += net_profit

        print(f"--- Transaction Batch {i+1} ---")
        print(f"Injection (Buy): {inj_date.date()} @ ${price_buy:.2f} | Withdrawal (Sell): {wit_date.date()} @ ${price_sell:.2f}")
        print(f"Actual volume: {volume:,.0f} MMBtu")
        print(f"Gross Profit (Sell - Buy): ${(revenue_gas - expense_gas):,.2f}")
        print(f"Total operational costs: ${total_cost:,.2f}")
        print(f"Net profit for this batch: ${net_profit:,.2f}\n")

    return total_contract_value





# Test Code
if __name__ == "__main__":
    # Simulate a client wanting to buy in summer and sell in winter for two batches
    test_inj_dates = [datetime(2024, 6, 1), datetime(2025, 7, 15)]
    test_wit_dates = [datetime(2024, 12, 1), datetime(2026, 1, 15)]
    
    # The second batch is intentionally set to 150,000 to test the max capacity limit
    test_volumes = [50000, 150000] 
    
    final_value = calculate_contract_value(
        injection_dates=test_inj_dates,
        withdrawal_dates=test_wit_dates,
        target_volumes=test_volumes,
        max_volume=100000,          # Parameter 5: Max storage capacity 
        rate_limit=10000,           # Parameter 4: Max daily injection/withdrawal rate
        storage_cost_per_month=0.1, # Parameter 6: Storage cost per unit per month
        injection_cost_per_unit=0.01,
        withdrawal_cost_per_unit=0.01,
        transport_cost_per_unit=0.05
    )
    
    print(f"=====================================")
    print(f"Final Total Contract Value: ${final_value:,.2f}")
    print(f"=====================================")