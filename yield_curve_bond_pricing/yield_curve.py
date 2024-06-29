import QuantLib as ql

def build_yield_curve(evaluation_date, spot_dates, spot_rates):
    """
    Constructs a yield curve using QuantLib.
    
    Args:
    evaluation_date (ql.Date): The evaluation date for the curve
    spot_dates (list): List of ql.Date objects for spot rates
    spot_rates (list): List of spot rates corresponding to spot_dates
    
    Returns:
    ql.YieldTermStructureHandle: The constructed yield curve
    """
    ql.Settings.instance().evaluationDate = evaluation_date
    
    day_count = ql.Actual365Fixed()
    calendar = ql.TARGET()
    interpolation = ql.Linear()
    compounding = ql.Compounded
    compounding_frequency = ql.Annual
    
    spot_curve = ql.ZeroCurve(spot_dates, spot_rates, day_count, calendar, 
                              interpolation, compounding, compounding_frequency)
    
    return ql.YieldTermStructureHandle(spot_curve)