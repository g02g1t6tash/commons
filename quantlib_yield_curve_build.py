import QuantLib as ql
import matplotlib.pyplot as plt

# Set evaluation date
today = ql.Date(28, 6, 2024)
ql.Settings.instance().evaluationDate = today

# Market data
spot_dates = [ql.Date(28, 6, 2024), ql.Date(30, 6, 2024), ql.Date(31, 7, 2024), ql.Date(30, 9, 2024),
              ql.Date(31, 12, 2024), ql.Date(30, 6, 2025), ql.Date(30, 6, 2026), ql.Date(30, 6, 2029)]
spot_rates = [0.0350, 0.0350, 0.0355, 0.0359, 0.0368, 0.0375, 0.0385, 0.0402]

# Build yield curve
day_count = ql.Actual365Fixed()
calendar = ql.UnitedStates()
interpolation = ql.Linear()
compounding = ql.Compounded
compounding_frequency = ql.Annual

spot_curve = ql.ZeroCurve(spot_dates, spot_rates, day_count, calendar, interpolation, 
                          compounding, compounding_frequency)
spot_curve_handle = ql.YieldTermStructureHandle(spot_curve)

# Plot yield curve
plt.figure(figsize=(10, 6))
plt.plot([spot_curve.timeFromReference(d) for d in spot_dates], spot_rates, 'o-')
plt.title('Zero Coupon Yield Curve')
plt.xlabel('Time (years)')
plt.ylabel('Zero Rate')
plt.grid(True)
plt.show()

# Price a fixed-rate bond
issue_date = today
maturity_date = ql.Date(30, 6, 2029)
tenor = ql.Period(ql.Semiannual)
calendar = ql.UnitedStates()
business_convention = ql.Unadjusted
date_generation = ql.DateGeneration.Backward
month_end = False
schedule = ql.Schedule(issue_date, maturity_date, tenor, calendar, business_convention, 
                       business_convention, date_generation, month_end)

coupon_rate = 0.04
coupons = [coupon_rate]
settlement_days = 2
face_amount = 100
fixed_rate_bond = ql.FixedRateBond(settlement_days, face_amount, schedule, coupons, day_count)

# Set up pricing engine
bond_engine = ql.DiscountingBondEngine(spot_curve_handle)
fixed_rate_bond.setPricingEngine(bond_engine)

# Calculate bond price and yield
bond_price = fixed_rate_bond.NPV()
bond_yield = fixed_rate_bond.yield_(day_count, ql.Compounded, ql.Annual)

print(f"Bond Price: {bond_price:.4f}")
print(f"Bond Yield: {bond_yield:.4%}")

# Calculate key rate durations
shifts = [0.0001] * len(spot_dates)
key_rate_durations = []

for i in range(len(spot_dates)):
    up_rates = spot_rates.copy()
    up_rates[i] += shifts[i]
    down_rates = spot_rates.copy()
    down_rates[i] -= shifts[i]
    
    up_curve = ql.ZeroCurve(spot_dates, up_rates, day_count, calendar, interpolation, 
                            compounding, compounding_frequency)
    down_curve = ql.ZeroCurve(spot_dates, down_rates, day_count, calendar, interpolation, 
                              compounding, compounding_frequency)
    
    up_engine = ql.DiscountingBondEngine(ql.YieldTermStructureHandle(up_curve))
    down_engine = ql.DiscountingBondEngine(ql.YieldTermStructureHandle(down_curve))
    
    fixed_rate_bond.setPricingEngine(up_engine)
    up_price = fixed_rate_bond.NPV()
    fixed_rate_bond.setPricingEngine(down_engine)
    down_price = fixed_rate_bond.NPV()
    
    key_rate_duration = (down_price - up_price) / (2 * shifts[i] * bond_price)
    key_rate_durations.append(key_rate_duration)

# Plot key rate durations
plt.figure(figsize=(10, 6))
plt.bar([spot_curve.timeFromReference(d) for d in spot_dates], key_rate_durations)
plt.title('Key Rate Durations')
plt.xlabel('Time (years)')
plt.ylabel('Key Rate Duration')
plt.grid(True)
plt.show()