import backtrader as bt
import datetime

# 1. Data Feed
class MyDataFeed(bt.feeds.GenericCSVData):
    params = (
        ('datetime', 0),
        ('open', 1),
        ('high', 2),
        ('low', 3),
        ('close', 4),
        ('volume', 5),
        ('openinterest', -1)
    )

# 2. Strategy
class MyStrategy(bt.Strategy):
    params = (('param1', 20), ('param2', 50))

    def __init__(self):
        self.dataclose = self.datas[0].close
        # Initialize indicators
        self.sma1 = bt.indicators.SimpleMovingAverage(self.dataclose, period=self.params.param1)
        self.sma2 = bt.indicators.SimpleMovingAverage(self.dataclose, period=self.params.param2)

    def next(self):
        if not self.position:
            if self.sma1 > self.sma2:
                self.buy()
        else:
            if self.sma1 < self.sma2:
                self.sell()

# 3. Backtest Setup
def run_backtest(data_path, strategy, start_date, end_date, cash=100000.0):
    cerebro = bt.Cerebro()

    # Add data feed
    data = MyDataFeed(dataname=data_path, fromdate=start_date, todate=end_date)
    cerebro.adddata(data)

    # Add strategy
    cerebro.addstrategy(strategy)

    # Set initial cash
    cerebro.broker.setcash(cash)

    # Add analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

    # Run backtest
    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
    results = cerebro.run()
    print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')

    # Print analyzer results
    strat = results[0]
    print(f'Sharpe Ratio: {strat.analyzers.sharpe.get_analysis()["sharperatio"]:.3f}')
    print(f'Max Drawdown: {strat.analyzers.drawdown.get_analysis()["max"]["drawdown"]:.2f}%')

    # Plot results
    cerebro.plot()

# 4. Main execution
if __name__ == '__main__':
    data_path = 'path/to/your/data.csv'
    start_date = datetime.datetime(2010, 1, 1)
    end_date = datetime.datetime(2020, 12, 31)
    
    run_backtest(data_path, MyStrategy, start_date, end_date)