
# 1.  Set up the environment:


import QuantLib as ql
import numpy as np


# 2.  Define market data and parameters:


today = ql.Date(15, 6, 2023)
ql.Settings.instance().evaluationDate = today

spot_price = 100.0
risk_free_rate = 0.05
dividend_yield = 0.02
volatility = 0.20
maturity_date = ql.Date(15, 6, 2024)


# 3.  Create QuantLib objects:


day_count = ql.Actual365Fixed()
calendar = ql.TARGET()

spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
riskfreerate_handle = ql.YieldTermStructureHandle(ql.FlatForward(0, calendar, risk_free_rate, day_count))
dividend_handle = ql.YieldTermStructureHandle(ql.FlatForward(0, calendar, dividend_yield, day_count))
volatility_handle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(0, calendar, volatility, day_count))

process = ql.BlackScholesMertonProcess(spot_handle, dividend_handle, riskfreerate_handle, volatility_handle)


# 4.  Create and price the option:


strike = 100.0
option_type = ql.Option.Call

payoff = ql.PlainVanillaPayoff(option_type, strike)
european_exercise = ql.EuropeanExercise(maturity_date)
european_option = ql.VanillaOption(payoff, european_exercise)

engine = ql.AnalyticEuropeanEngine(process)
european_option.setPricingEngine(engine)

price = european_option.NPV()


# 5.  Calculate risk measures:


delta = european_option.delta()
gamma = european_option.gamma()
vega = european_option.vega()
theta = european_option.theta()


# 6.  Perform sensitivity analysis:


def calculate_price(spot):
    new_spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot))
    new_process = ql.BlackScholesMertonProcess(new_spot_handle, dividend_handle, riskfreerate_handle, volatility_handle)
    new_engine = ql.AnalyticEuropeanEngine(new_process)
    european_option.setPricingEngine(new_engine)
    return european_option.NPV()

spots = np.linspace(80, 120, 41)
prices = [calculate_price(spot) for spot in spots]


# 7.  Calculate Value at Risk (VaR):


def calculate_portfolio_value(spot):
    return calculate_price(spot) * 1000  # Assuming 1000 options

portfolio_values = [calculate_portfolio_value(spot) for spot in spots]
changes = np.diff(portfolio_values)
var_95 = np.percentile(changes, 5)


# 8.  Print results:


print(f"Option Price: {price:.2f}")
print(f"Delta: {delta:.4f}")
print(f"Gamma: {gamma:.4f}")
print(f"Vega: {vega:.4f}")
print(f"Theta: {theta:.4f}")
print(f"95% VaR: {-var_95:.2f}")

