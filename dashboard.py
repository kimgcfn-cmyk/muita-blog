import ccxt
from datetime import datetime
from dotenv import load_dotenv
import os


class TradingDashboard:
    def __init__(self):
        load_dotenv()
        
        self.exchange_name = os.getenv('EXCHANGE', 'upbit')
        self.market = os.getenv('MARKET', 'KRW-BTC')
        
        self.exchange = getattr(ccxt, self.exchange_name)({
            'apiKey': os.getenv('API_KEY'),
            'secret': os.getenv('SECRET_KEY'),
        })
    
    def get_market_info(self):
        ticker = self.exchange.fetch_ticker(self.market)
        return {
            'current_price': ticker['last'],
            'high_24h': ticker['high'],
            'low_24h': ticker['low'],
            'volume_24h': ticker['baseVolume'],
            'change_24h': ticker['percentage']
        }
    
    def get_balance(self):
        balance = self.exchange.fetch_balance()
        return {
            'total_krw': balance['total'].get('KRW', 0),
            'available_krw': balance['free'].get('KRW', 0),
            'btc': balance['total'].get('BTC', 0),
            'usdt': balance['total'].get('USDT', 0)
        }
    
    def display_dashboard(self):
        market_info = self.get_market_info()
        balance = self.get_balance()
        
        print("\n" + "=" * 60)
        print("=== 떨사오팔 트레이딩 대시보드 ===")
        print(f"업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        print("\n[시장 정보]")
        print(f"현재가: {market_info['current_price']:,.0f}원")
        print(f"24시간 최고: {market_info['high_24h']:,.0f}원")
        print(f"24시간 최저: {market_info['low_24h']:,.0f}원")
        print(f"24시간 거래량: {market_info['volume_24h']:,.2f}")
        print(f"24시간 등락: {market_info['change_24h']:+.2f}%")
        
        print("\n[잔고 정보]")
        print(f"원화 잔고: {balance['total_krw']:,.0f}원")
        print(f"사용 가능: {balance['available_krw']:,.0f}원")
        print(f"보유 비트코인: {balance['btc']:.8f}BTC")
        
        if balance['btc'] > 0:
            btc_value = balance['btc'] * market_info['current_price']
            print(f"비트코인 평가액: {btc_value:,.0f}원")
            total = balance['total_krw'] + btc_value
            print(f"총 자산: {total:,.0f}원")
        
        print("\n" + "=" * 60)


if __name__ == "__main__":
    dashboard = TradingDashboard()
    dashboard.display_dashboard()
