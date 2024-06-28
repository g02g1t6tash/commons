import QuantLib as ql

# 1. Set up the environment and define market data:

# Set the evaluation date
today = ql.Date(15, 6, 2023)
ql.Settings.instance().evaluationDate = today

# Define market data
risk_free_rate = 0.03
libor_rate = 0.035
day_count = ql.Actual365Fixed()
calendar = ql.TARGET()

# 2. Create yield curves for discounting and forwarding:

# Create a flat forward curve for discounting
discount_curve = ql.YieldTermStructureHandle(
    ql.FlatForward(today, risk_free_rate, day_count)
)
# Create a flat forward curve for LIBOR
libor_curve = ql.YieldTermStructureHandle(
    ql.FlatForward(today, libor_rate, day_count)
)

# 3. Define the floating rate index:

# Use Euribor 3M as the floating rate index
index = ql.Euribor3M(libor_curve)

# Add historical fixings
fixing_calendar = index.fixingCalendar()
for i in range(1, 8):
    fixing_date = today - ql.Period(i, ql.Days)
    if index.isValidFixingDate(fixing_date):
        adjusted_fixing_date = fixing_calendar.adjust(fixing_date)
        index.addFixing(adjusted_fixing_date, libor_rate)

# 4. Set up swap parameters:

notional = 10000000
maturity_date = today + ql.Period(5, ql.Years)
fixed_rate = 0.04
fixed_leg_tenor = ql.Period(6, ql.Months)
float_leg_tenor = ql.Period(3, ql.Months)

# 5. Create schedules for fixed and floating legs:

# Schedule for the fixed leg
fixed_schedule = ql.Schedule(
    today,
    maturity_date,
    fixed_leg_tenor,
    calendar,
    ql.ModifiedFollowing,
    ql.ModifiedFollowing,
    ql.DateGeneration.Forward,
    False
)

# Schedule for the floating leg
float_schedule = ql.Schedule(
    today,
    maturity_date,
    float_leg_tenor,
    calendar,
    ql.ModifiedFollowing,
    ql.ModifiedFollowing,
    ql.DateGeneration.Forward,
    False
)

# 6. Create the swap:

# Create a vanilla swap (Payer swap: pay fixed, receive floating)
swap = ql.VanillaSwap(
    ql.VanillaSwap.Payer,
    notional,
    fixed_schedule,
    fixed_rate,
    day_count,
    float_schedule,
    index,
    0,
    day_count
)

# 7. Set up the pricing engine:

# Use DiscountingSwapEngine for pricing
engine = ql.DiscountingSwapEngine(discount_curve)
swap.setPricingEngine(engine)

# 8. Calculate and print the results:

print(f"Swap NPV: {swap.NPV():.2f}")
print(f"Fair fixed rate: {swap.fairRate():.4%}")
print(f"Fair floating spread: {swap.fairSpread():.4%}")

# 9. Additional calculations (optional):

print(f"Fixed leg BPS: {swap.fixedLegBPS():.2f}")
print(f"Floating leg BPS: {swap.floatingLegBPS():.2f}")
print(f"Fixed leg NPV: {swap.fixedLegNPV():.2f}")
print(f"Floating leg NPV: {swap.floatingLegNPV():.2f}")