import ccxt
import pandas as pd
from datetime import datetime


class TteolsaOppalBacktest:
    def __init__(self, exchange_name='binance', market='BTC/USDT'):
        self.exchange = getattr(ccxt, exchange_name)()
        self.market = market
        
        self.buy_threshold = -0.03
        self.sell_threshold = 0.05
        self.initial_balance = 1000000
        
        self.balance = self.initial_balance
        self.position = 0
        self.buy_price = 0
        self.trades = []
    
    def fetch_ohlcv(self, days=30):
        since = self.exchange.parse8601(
            (datetime.now() - pd.Timedelta(days=days)).isoformat()
        )
        
        ohlcv = self.exchange.fetch_ohlcv(
            self.market,
            '1h',
            since=since,
            limit=1000
        )
        
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['change'] = df['close'].pct_change() * 100
        
        return df
    
    def run_backtest(self, df):
        for i in range(1, len(df)):
            current_price = df.iloc[i]['close']
            price_change = df.iloc[i]['change']
            
            if self.position == 0:
                if price_change <= self.buy_threshold * 100:
                    amount = self.balance / current_price
                    self.position = amount
                    self.balance = 0
                    self.buy_price = current_price
                    self.trades.append({
                        'time': df.iloc[i]['timestamp'],
                        'action': 'BUY',
                        'price': current_price,
                        'amount': amount
                    })
            
            else:
                profit_rate = (current_price - self.buy_price) / self.buy_price
                
                if profit_rate >= self.sell_threshold:
                    self.balance = self.position * current_price
                    profit = current_price - self.buy_price
                    self.trades.append({
                        'time': df.iloc[i]['timestamp'],
                        'action': 'SELL',
                        'price': current_price,
                        'profit': profit,
                        'profit_rate': profit_rate * 100
                    })
                    self.position = 0
                    self.buy_price = 0
        
        return self.trades
    
    def calculate_results(self):
        total_trades = len([t for t in self.trades if t['action'] == 'SELL'])
        wins = len([t for t in self.trades if t['action'] == 'SELL' and t.get('profit', 0) > 0])
        losses = len([t for t in self.trades if t['action'] == 'SELL' and t.get('profit', 0) < 0])
        
        final_balance = self.balance + (self.position * self.trades[-1]['price'] if self.position > 0 else 0)
        total_return = (final_balance - self.initial_balance) / self.initial_balance * 100
        
        return {
            'final_balance': final_balance,
            'total_return': total_return,
            'total_trades': total_trades,
            'wins': wins,
            'losses': losses,
            'win_rate': (wins / total_trades * 100) if total_trades > 0 else 0
        }


if __name__ == "__main__":
    backtest = TteolsaOppalBacktest()
    
    print("데이터 수집 중...")
    df = backtest.fetch_ohlcv(days=30)
    
    print("백테스트 실행 중...")
    trades = backtest.run_backtest(df)
    
    results = backtest.calculate_results()
    
    print("\n=== 백테스트 결과 ===")
    print(f"최종 잔고: {results['final_balance']:,.2f}")
    print(f"총 수익률: {results['total_return']:.2f}%")
    print(f"총 거래 횟수: {results['total_trades']}")
    print(f"승리: {results['wins']}회")
    print(f"패배: {results['losses']}회")
    print(f"승률: {results['win_rate']:.2f}%")
    
    print("\n=== 거래 내역 ===")
    for trade in trades:
        if trade['action'] == 'BUY':
            print(f"[{trade['time']}] 매수: {trade['price']:,.2f}원")
        else:
            print(f"[{trade['time']}] 매도: {trade['price']:,.2f}원 (수익률: {trade['profit_rate']:.2f}%)")
