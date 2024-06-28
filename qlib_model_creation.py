import QuantLib as ql

today = ql.Date(15, 6, 2023)
ql.Settings.instance().evaluationDate = today

#Define market data and parameters:

spot_price = 100.0
risk_free_rate = 0.05
dividend_yield = 0.02
volatility = 0.20
maturity_date = ql.Date(15, 6, 2024)

#Create necessary QuantLib objects:

day_count = ql.Actual365Fixed()
calendar = ql.TARGET()

spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
riskfreerate_handle = ql.YieldTermStructureHandle(ql.FlatForward(0, calendar, risk_free_rate, day_count))
dividend_handle = ql.YieldTermStructureHandle(ql.FlatForward(0, calendar, dividend_yield, day_count))
volatility_handle = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(0, calendar, volatility, day_count))

#Create the process (in this case, a Black-Scholes-Merton process):

bsm_process = ql.BlackScholesMertonProcess(spot_handle, dividend_handle, riskfreerate_handle, volatility_handle)

#Define the option parameters:

strike = 100.0
option_type = ql.Option.Call

#Create the option:

payoff = ql.PlainVanillaPayoff(option_type, strike)
european_exercise = ql.EuropeanExercise(maturity_date)
european_option = ql.VanillaOption(payoff, european_exercise)

#Set up the pricing engine:

engine = ql.AnalyticEuropeanEngine(bsm_process)
european_option.setPricingEngine(engine)

print(f"Option NPV: {european_option.NPV()}")
print(f"Option delta: {european_option.delta()}")
print(f"Option gamma: {european_option.gamma()}")
print(f"Option vega: {european_option.vega()}")
print(f"Option theta: {european_option.theta()}")