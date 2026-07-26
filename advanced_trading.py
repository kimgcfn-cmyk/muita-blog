import ccxt
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv
import os


class AdvancedTteolsaBot:
    def __init__(self):
        load_dotenv()
        
        self.exchange_name = os.getenv('EXCHANGE', 'upbit')
        self.market = os.getenv('MARKET', 'KRW-BTC')
        
        self.buy_threshold = float(os.getenv('BUY_THRESHOLD', -3.0)) / 100
        self.sell_threshold = float(os.getenv('SELL_THRESHOLD', 5.0)) / 100
        self.invest_amount = float(os.getenv('INVEST_AMOUNT', 10000))
        self.interval = int(os.getenv('INTERVAL_MINUTES', 5))
        
        self.exchange = getattr(ccxt, self.exchange_name)({
            'apiKey': os.getenv('API_KEY'),
            'secret': os.getenv('SECRET_KEY'),
        })
        
        self.is_holding = False
        self.buy_price = 0
        self.position_size = 0
        
        self.max_position = 5
        self.dca_threshold = -0.05
        self.dca_amount = 5000
        
        self.price_history = []
        self.trade_history = []
        
        self.log_file = f"advanced_trade_log_{datetime.now().strftime('%Y%m%d')}.txt"
    
    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def get_current_price(self):
        ticker = self.exchange.fetch_ticker(self.market)
        return ticker['last']
    
    def get_ohlcv(self, timeframe='1h', limit=100):
        ohlcv = self.exchange.fetch_ohlcv(self.market, timeframe, limit=limit)
        return ohlcv
    
    def calculate_rsi(self, period=14):
        ohlcv = self.get_ohlcv('1h', limit=period + 10)
        closes = [candle[4] for candle in ohlcv]
        
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_moving_average(self, period=20):
        ohlcv = self.get_ohlcv('1h', limit=period)
        closes = [candle[4] for candle in ohlcv]
        return sum(closes) / len(closes)
    
    def check_trend(self):
        ma_short = self.calculate_moving_average(10)
        ma_long = self.calculate_moving_average(30)
        current_price = self.get_current_price()
        
        if current_price > ma_short > ma_long:
            return 'UP'
        elif current_price < ma_short < ma_long:
            return 'DOWN'
        else:
            return 'SIDEWAY'
    
    def buy(self, amount=None):
        try:
            current_price = self.get_current_price()
            buy_amount = amount or self.invest_amount
            
            order = self.exchange.create_market_buy_order(
                self.market,
                buy_amount / current_price
            )
            
            if not self.is_holding:
                self.buy_price = current_price
                self.position_size = buy_amount / current_price
            else:
                total_cost = self.buy_price * self.position_size + current_price * (buy_amount / current_price)
                total_size = self.position_size + (buy_amount / current_price)
                self.buy_price = total_cost / total_size
                self.position_size = total_size
            
            self.is_holding = True
            
            self.log(f"매수 완료: {current_price:,.0f}원 ({buy_amount:,.0f}원)")
            self.trade_history.append({
                'time': datetime.now(),
                'action': 'BUY',
                'price': current_price,
                'amount': buy_amount,
                'total_position': self.position_size
            })
            return True
            
        except Exception as e:
            self.log(f"매수 실패: {e}")
            return False
    
    def sell(self, percentage=100):
        try:
            current_price = self.get_current_price()
            sell_amount = self.position_size * (percentage / 100)
            
            order = self.exchange.create_market_sell_order(
                self.market,
                sell_amount
            )
            
            profit = (current_price - self.buy_price) / self.buy_price * 100
            
            self.log(f"매도 완료: {current_price:,.0f}원 ({percentage:.0f}%)")
            self.log(f"수익률: {profit:+.2f}%")
            
            self.position_size -= sell_amount
            if self.position_size <= 0:
                self.is_holding = False
                self.position_size = 0
                self.buy_price = 0
            
            self.trade_history.append({
                'time': datetime.now(),
                'action': 'SELL',
                'price': current_price,
                'amount': sell_amount,
                'profit': profit
            })
            return True
            
        except Exception as e:
            self.log(f"매도 실패: {e}")
            return False
    
    def check_strategy(self):
        try:
            current_price = self.get_current_price()
            rsi = self.calculate_rsi()
            trend = self.check_trend()
            
            self.log(f"현재가: {current_price:,.0f}원 | RSI: {rsi:.1f} | 추세: {trend}")
            
            if not self.is_holding:
                if trend == 'DOWN' and rsi < 30:
                    self.log("강력 매수 신호!")
                    self.buy()
                elif trend == 'SIDEWAY' and rsi < 40:
                    self.log("약한 매수 신호")
                    self.buy()
            
            else:
                profit_rate = (current_price - self.buy_price) / self.buy_price
                
                if profit_rate >= self.sell_threshold:
                    if rsi > 70:
                        self.log("전량 매도 (RSI 과매수)")
                        self.sell(100)
                    else:
                        self.log("부분 매도 (50%)")
                        self.sell(50)
                
                elif profit_rate <= self.dca_threshold:
                    if self.position_size < self.max_position:
                        self.log("추가 매수 (DCA)")
                        self.buy(self.dca_amount)
                    else:
                        self.log("손절 매도 (최대 물림)")
                        self.sell(100)
                
                elif profit_rate <= -0.15:
                    self.log("강제 손절매 (15% 하락)")
                    self.sell(100)
                    
        except Exception as e:
            self.log(f"전략 체크 실패: {e}")
    
    def run(self):
        self.log("=" * 60)
        self.log("=== 고급 떨사오팔 봇 시작 ===")
        self.log(f"거래소: {self.exchange_name}")
        self.log(f"마켓: {self.market}")
        self.log(f"매수 임계값: {self.buy_threshold * 100}%")
        self.log(f"매도 임계값: {self.sell_threshold * 100}%")
        self.log(f"매수 금액: {self.invest_amount:,.0f}원")
        self.log(f"DCA 임계값: {self.dca_threshold * 100}%")
        self.log(f"최대 물림: {self.max_position}회")
        self.log("=" * 60)
        
        self.check_strategy()
        
        schedule.every(self.interval).minutes.do(self.check_strategy)
        
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    bot = AdvancedTteolsaBot()
    bot.run()
