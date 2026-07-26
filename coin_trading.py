import ccxt
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv
import os


class TteolsaOppalBot:
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
        self.balance = 0
        
        self.log_file = f"trade_log_{datetime.now().strftime('%Y%m%d')}.txt"
    
    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def get_current_price(self):
        ticker = self.exchange.fetch_ticker(self.market)
        return ticker['last']
    
    def get_price_change_percent(self):
        ticker = self.exchange.fetch_ticker(self.market)
        return ticker['percentage']
    
    def get_balance(self):
        try:
            balance = self.exchange.fetch_balance()
            if self.market.startswith('KRW'):
                return balance['total'].get('KRW', 0)
            else:
                coin = self.market.split('-')[1]
                return balance['total'].get(coin, 0)
        except:
            return 0
    
    def buy(self):
        try:
            current_price = self.get_current_price()
            amount = self.invest_amount / current_price
            
            order = self.exchange.create_market_buy_order(
                self.market,
                amount
            )
            
            self.is_holding = True
            self.buy_price = current_price
            
            self.log(f"매수 완료: {current_price:,.0f}원 x {amount:.8f}")
            self.log(f"주문 ID: {order['id']}")
            return True
            
        except Exception as e:
            self.log(f"매수 실패: {e}")
            return False
    
    def sell(self):
        try:
            current_price = self.get_current_price()
            amount = self.invest_amount / self.buy_price
            
            order = self.exchange.create_market_sell_order(
                self.market,
                amount
            )
            
            profit = (current_price - self.buy_price) / self.buy_price * 100
            profit_amount = current_price - self.buy_price
            
            self.log(f"매도 완료: {current_price:,.0f}원")
            self.log(f"수익률: {profit:+.2f}% ({profit_amount:+,.0f}원)")
            self.log(f"주문 ID: {order['id']}")
            
            self.is_holding = False
            self.buy_price = 0
            return True
            
        except Exception as e:
            self.log(f"매도 실패: {e}")
            return False
    
    def check_strategy(self):
        try:
            current_price = self.get_current_price()
            price_change = self.get_price_change_percent()
            
            self.log(f"현재가: {current_price:,.0f}원 | 24h 등락: {price_change:+.2f}%")
            
            if not self.is_holding:
                if price_change <= self.buy_threshold * 100:
                    self.log("매수 조건 충족!")
                    self.buy()
            else:
                profit_rate = (current_price - self.buy_price) / self.buy_price
                
                if profit_rate >= self.sell_threshold:
                    self.log("매도 조건 충족!")
                    self.sell()
                elif profit_rate <= -0.10:
                    self.log("손절 매도 (10% 하락)")
                    self.sell()
                    
        except Exception as e:
            self.log(f"전략 체크 실패: {e}")
    
    def run(self):
        self.log("=" * 50)
        self.log("=== 떨사오팔 봇 시작 ===")
        self.log(f"거래소: {self.exchange_name}")
        self.log(f"마켓: {self.market}")
        self.log(f"매수 임계값: {self.buy_threshold * 100}%")
        self.log(f"매도 임계값: {self.sell_threshold * 100}%")
        self.log(f"매수 금액: {self.invest_amount:,.0f}원")
        self.log(f"체크 간격: {self.interval}분")
        self.log("=" * 50)
        
        self.check_strategy()
        
        schedule.every(self.interval).minutes.do(self.check_strategy)
        
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    bot = TteolsaOppalBot()
    bot.run()
