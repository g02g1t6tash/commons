import backtrader as bt
import QuantLib as ql
import datetime

class YieldCurveBondStrategy(bt.Strategy):
    params = (
        ('bond_maturity', 5),  # years
        ('coupon_rate', 0.04),  # 4%
        ('face_value', 100),
    )

    def __init__(self):
        self.order = None
        self.yield_curve = None
        self.bond = None

    def next(self):
        # Update yield curve and price bond on each bar
        self.update_yield_curve()
        self.price_bond()

        # Your trading logic here
        # For example, buy if bond price is below face value
        if self.bond.NPV() < self.p.face_value and not self.position:
            self.buy()
        # Sell if bond price is above face value and we have a position
        elif self.bond.NPV() > self.p.face_value and self.position:
            self.sell()

    def update_yield_curve(self):
        today = ql.Date(self.data.datetime.date(0).day,
                        self.data.datetime.date(0).month,
                        self.data.datetime.date(0).year)
        ql.Settings.instance().evaluationDate = today

        # Use closing prices as "rates" for simplicity
        spot_dates = [today + ql.Period(i, ql.Years) for i in range(1, 11)]
        spot_rates = [self.data.close[0] / 100 for _ in range(10)]  # Convert to decimal

        day_count = ql.Actual365Fixed()
        calendar = ql.UnitedStates()
        interpolation = ql.Linear()
        compounding = ql.Compounded
        compounding_frequency = ql.Annual

        self.yield_curve = ql.ZeroCurve(spot_dates, spot_rates, day_count, calendar, interpolation,
                                        compounding, compounding_frequency)

    def price_bond(self):
        if self.yield_curve is None:
            return

        today = ql.Settings.instance().evaluationDate
        maturity_date = today + ql.Period(self.p.bond_maturity, ql.Years)
        tenor = ql.Period(ql.Semiannual)
        calendar = ql.UnitedStates()
        business_convention = ql.Unadjusted
        date_generation = ql.DateGeneration.Backward
        month_end = False
        schedule = ql.Schedule(today, maturity_date, tenor, calendar, business_convention,
                               business_convention, date_generation, month_end)

        coupons = [self.p.coupon_rate]
        day_count = ql.Actual365Fixed()
        settlement_days = 2

        self.bond = ql.FixedRateBond(settlement_days, self.p.face_value, schedule, coupons, day_count)

        bond_engine = ql.DiscountingBondEngine(ql.YieldTermStructureHandle(self.yield_curve))
        self.bond.setPricingEngine(bond_engine)

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price:.2f}')
            else:
                self.log(f'SELL EXECUTED, Price: {order.executed.price:.2f}')

        self.order = None

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # Add data feed
    data = bt.feeds.YahooFinanceData(dataname='AAPL', fromdate=datetime.datetime(2020, 1, 1),
                                     todate=datetime.datetime(2021, 12, 31))
    cerebro.adddata(data)

    # Add strategy
    cerebro.addstrategy(YieldCurveBondStrategy)

    # Set initial cash
    cerebro.broker.setcash(100000.0)

    # Run the strategy
    cerebro.run()

    # Plot the results
    cerebro.plot()