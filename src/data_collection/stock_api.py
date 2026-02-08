"""
주식 및 금융 데이터 수집 모듈
"""
import yfinance as yf
from datetime import datetime, timedelta
from typing import Dict, List
from loguru import logger


class StockDataCollector:
    """주식 및 금융 시장 데이터 수집"""
    
    def __init__(self):
        self.symbols = {
            'KOSPI': '^KS11',
            'KOSDAQ': '^KQ11',
            '삼성전자': '005930.KS',
            'NASDAQ': '^IXIC',
            'S&P500': '^GSPC',
            'DOW': '^DJI',
            '달러/원': 'KRW=X',
            '비트코인': 'BTC-USD',
            '이더리움': 'ETH-USD',
        }
    
    def get_current_price(self, symbol: str) -> Dict:
        """현재 가격 및 변동률 조회"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            history = ticker.history(period='2d')
            
            if len(history) < 2:
                return None
            
            current_price = history['Close'].iloc[-1]
            prev_price = history['Close'].iloc[-2]
            change = current_price - prev_price
            change_percent = (change / prev_price) * 100
            
            return {
                'symbol': symbol,
                'current_price': round(current_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'volume': int(history['Volume'].iloc[-1]) if 'Volume' in history else 0,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"{symbol} 데이터 수집 실패: {e}")
            return None
    
    def get_market_summary(self) -> Dict:
        """주요 시장 지표 요약"""
        summary = {}
        
        for name, symbol in self.symbols.items():
            data = self.get_current_price(symbol)
            if data:
                summary[name] = data
                logger.info(f"{name}: {data['current_price']} ({data['change_percent']:+.2f}%)")
        
        return summary
    
    def get_top_movers(self, market='KRW') -> Dict:
        """급등/급락 종목 조회"""
        if market == 'KRW':
            # KOSPI 200 주요 종목 (예시)
            top_symbols = [
                '005930.KS',  # 삼성전자
                '000660.KS',  # SK하이닉스
                '035420.KS',  # NAVER
                '005380.KS',  # 현대차
                '051910.KS',  # LG화학
            ]
        else:
            # 나스닥 주요 종목
            top_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        
        movers = []
        for symbol in top_symbols:
            data = self.get_current_price(symbol)
            if data and abs(data['change_percent']) > 2:  # 2% 이상 변동
                movers.append(data)
        
        # 변동률 기준 정렬
        movers.sort(key=lambda x: abs(x['change_percent']), reverse=True)
        
        return {
            'gainers': [m for m in movers if m['change_percent'] > 0][:3],
            'losers': [m for m in movers if m['change_percent'] < 0][:3]
        }
    
    def analyze_trend(self, symbol: str, period='1mo') -> Dict:
        """추세 분석"""
        try:
            ticker = yf.Ticker(symbol)
            history = ticker.history(period=period)
            
            if len(history) < 2:
                return None
            
            # 간단한 추세 분석
            first_price = history['Close'].iloc[0]
            last_price = history['Close'].iloc[-1]
            total_change = ((last_price - first_price) / first_price) * 100
            
            # 이동평균
            ma_5 = history['Close'].rolling(window=5).mean().iloc[-1]
            ma_20 = history['Close'].rolling(window=min(20, len(history))).mean().iloc[-1]
            
            # 추세 판단
            if last_price > ma_5 > ma_20:
                trend = '강한 상승세'
            elif last_price > ma_20:
                trend = '상승세'
            elif last_price < ma_5 < ma_20:
                trend = '강한 하락세'
            else:
                trend = '하락세'
            
            return {
                'symbol': symbol,
                'period': period,
                'total_change_percent': round(total_change, 2),
                'ma_5': round(ma_5, 2),
                'ma_20': round(ma_20, 2),
                'trend': trend,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"{symbol} 추세 분석 실패: {e}")
            return None
    
    def get_interesting_stories(self) -> List[Dict]:
        """흥미로운 시장 이야기 추출"""
        stories = []
        summary = self.get_market_summary()
        
        # 1. 큰 변동
        for name, data in summary.items():
            if abs(data['change_percent']) > 3:
                stories.append({
                    'type': 'big_move',
                    'title': f"{name} {'급등' if data['change_percent'] > 0 else '급락'}",
                    'description': f"{name}이(가) {abs(data['change_percent']):.2f}% {'상승' if data['change_percent'] > 0 else '하락'}했습니다",
                    'data': data,
                    'importance': 'high'
                })
        
        # 2. 환율 변동
        if '달러/원' in summary:
            usd_krw = summary['달러/원']
            if abs(usd_krw['change_percent']) > 1:
                stories.append({
                    'type': 'forex',
                    'title': '환율 급변동',
                    'description': f"달러/원 환율이 {usd_krw['change_percent']:+.2f}% 변동",
                    'data': usd_krw,
                    'importance': 'medium'
                })
        
        # 3. 암호화폐 변동
        if '비트코인' in summary:
            btc = summary['비트코인']
            if abs(btc['change_percent']) > 5:
                stories.append({
                    'type': 'crypto',
                    'title': '비트코인 급변동',
                    'description': f"비트코인이 {btc['change_percent']:+.2f}% 변동",
                    'data': btc,
                    'importance': 'high'
                })
        
        return stories


# 테스트 코드
if __name__ == "__main__":
    logger.add("logs/stock_data.log", rotation="1 day")
    
    collector = StockDataCollector()
    
    print("=" * 50)
    print("주요 시장 지표")
    print("=" * 50)
    
    summary = collector.get_market_summary()
    for name, data in summary.items():
        print(f"{name:12} {data['current_price']:>10,.2f} ({data['change_percent']:>6.2f}%)")
    
    print("\n" + "=" * 50)
    print("흥미로운 시장 이야기")
    print("=" * 50)
    
    stories = collector.get_interesting_stories()
    for i, story in enumerate(stories, 1):
        print(f"\n{i}. [{story['importance'].upper()}] {story['title']}")
        print(f"   {story['description']}")
