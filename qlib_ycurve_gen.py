import QuantLib as ql

calculation_date = ql.Date(15, 1, 2024)
ql.Settings.instance().evaluationDate = calculation_date

# market data

dates = [ql.Date(15, 1, 2024), ql.Date(15, 7, 2024), ql.Date(15, 1, 2025), ql.Date(15, 1, 2026)]
rates = [0.04, 0.045, 0.05, 0.055]

# yield curve definition using zer ocurve
day_count = ql.Actual365Fixed()
calendar = ql.TARGET()
interpolation = ql.Linear()

yield_curve = ql.ZeroCurve(dates, rates, day_count, calendar, interpolation)

# yield term struct handle
yield_curve_handle = ql.YieldTermStructureHandle(yield_curve)

target_date = ql.Date(15, 1, 2025)
zero_rate = yield_curve_handle.zeroRate(target_date, day_count, ql.Continuous).rate()
discount_factor = yield_curve_handle.discount(target_date)

print(f"Zero rate for {target_date}: {zero_rate:.4%}")
print(f"Discount factor for {target_date}: {discount_factor:.4f}")
