import QuantLib as ql

def price_bond(yield_curve, issue_date, maturity_date, coupon_rate, face_value=100):
    """
    Prices a fixed-rate bond using QuantLib.
    
    Args:
    yield_curve (ql.YieldTermStructureHandle): The yield curve
    issue_date (ql.Date): The bond's issue date
    maturity_date (ql.Date): The bond's maturity date
    coupon_rate (float): The bond's coupon rate (as a decimal)
    face_value (float): The bond's face value
    
    Returns:
    float: The bond's price
    """
    schedule = ql.Schedule(issue_date, maturity_date, ql.Period(ql.Semiannual),
                           ql.TARGET(), ql.ModifiedFollowing, ql.ModifiedFollowing,
                           ql.DateGeneration.Backward, False)
    
    bond = ql.FixedRateBond(2, face_value, schedule, [coupon_rate], ql.Actual360())
    
    engine = ql.DiscountingBondEngine(yield_curve)
    bond.setPricingEngine(engine)
    
    return bond.cleanPrice()