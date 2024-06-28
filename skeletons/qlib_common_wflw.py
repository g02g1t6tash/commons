import QuantLib as ql

def main():
    # Set up the evaluation date
    today = ql.Date(15, 6, 2023)
    ql.Settings.instance().evaluationDate = today

    # Define market data
    spot_price = 100
    risk_free_rate = 0.05
    volatility = 0.2
    dividend_yield = 0.01

    # Create market objects
    spot_handle = ql.QuoteHandle(ql.SimpleQuote(spot_price))
    rate_handle = ql.QuoteHandle(ql.SimpleQuote(risk_free_rate))
    vol_handle = ql.QuoteHandle(ql.SimpleQuote(volatility))
    dividend_handle = ql.QuoteHandle(ql.SimpleQuote(dividend_yield))

    # Set up the option parameters
    expiry_date = ql.Date(15, 6, 2024)
    strike = 110
    option_type = ql.Option.Call

    # Create the option
    payoff = ql.PlainVanillaPayoff(option_type, strike)
    exercise = ql.EuropeanExercise(expiry_date)
    option = ql.VanillaOption(payoff, exercise)

    # Set up the pricing engine
    day_count = ql.Actual365Fixed()
    calculation_date = today

    risk_free_ts = ql.FlatForward(calculation_date, rate_handle, day_count)
    dividend_ts = ql.FlatForward(calculation_date, dividend_handle, day_count)
    
    bs_process = ql.BlackScholesMertonProcess(spot_handle, 
                                              dividend_ts,
                                              risk_free_ts,
                                              vol_handle)
    
    engine = ql.AnalyticEuropeanEngine(bs_process)
    option.setPricingEngine(engine)

    # Calculate and print results
    print(f"Option NPV: {option.NPV()}")
    print(f"Option delta: {option.delta()}")
    print(f"Option gamma: {option.gamma()}")
    print(f"Option vega: {option.vega()}")
    print(f"Option theta: {option.theta()}")

if __name__ == "__main__":
    main()