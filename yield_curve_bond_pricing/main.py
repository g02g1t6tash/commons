import QuantLib as ql
import backtrader as bt
from datetime import datetime, timedelta
import pandas as pd

from yield_curve import build_yield_curve
from bond_pricing import price_bond
from backtrader_strategy import BondTradingStrategy

def main():
    # Set up QuantLib dates and rates
    today = ql.Date(15, 6, 2023)
    spot_dates = [today, today + ql.Period(1, ql.Years), today + ql.Period(5, ql.Years), today + ql.Period(10, ql.Years)]
    spot_rates = [0.02, 0.025, 0.03, 0.035]

    # Build yield curve
    yield_curve = build_yield_curve(today, spot_dates, spot_rates)

    # Define bond parameters
    issue_date = ql.Date(1, 1, 2020)
    maturity_date = ql.Date(1, 1, 2030)
    coupon_rate = 0.04

    # Generate bond prices for a year
    dates = []
    prices = []
    for i in range(365):
        date = today + ql.Period(i, ql.Days)
        ql.Settings.instance().evaluationDate = date
        price = price_bond(yield_curve, issue_date, maturity_date, coupon_rate)
        dates.append(date.to_date())
        prices.append(price)

    # Create a pandas DataFrame with the bond prices
    df = pd.DataFrame({'Date': dates, 'Price': prices})
    df.set_index('Date', inplace=True)

    # Set up Backtrader
    cerebro = bt.Cerebro()
    data = bt.feeds.PandasData(dataname=df)
    
    cerebro.adddata(data)
    cerebro.addstrategy(BondTradingStrategy)
    cerebro.run()
    cerebro.plot()

if __name__ == "__main__":
    main()