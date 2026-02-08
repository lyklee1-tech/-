"""
데이터 수집 모듈 - 경제 뉴스 크롤러
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from typing import List, Dict
import feedparser
from loguru import logger


class NewsScraper:
    """경제 뉴스를 수집하는 크롤러"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # RSS 피드 URL들
        self.rss_feeds = {
            '한국경제': 'https://www.hankyung.com/rss/economy',
            '매일경제': 'https://www.mk.co.kr/rss/30100041/',
            '서울경제': 'https://www.sedaily.com/RSS/S00.xml',
            '연합뉴스': 'https://www.yonhapnews.co.kr/rss/economy.xml',
        }
    
    def fetch_news_from_rss(self, source: str, url: str) -> List[Dict]:
        """RSS 피드에서 뉴스 가져오기"""
        try:
            feed = feedparser.parse(url)
            news_list = []
            
            for entry in feed.entries[:5]:  # 최신 5개만
                news = {
                    'source': source,
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'timestamp': datetime.now().isoformat()
                }
                news_list.append(news)
            
            logger.info(f"{source}에서 {len(news_list)}개 뉴스 수집 완료")
            return news_list
            
        except Exception as e:
            logger.error(f"{source} RSS 파싱 실패: {e}")
            return []
    
    def fetch_all_news(self) -> List[Dict]:
        """모든 소스에서 뉴스 수집"""
        all_news = []
        
        for source, url in self.rss_feeds.items():
            news = self.fetch_news_from_rss(source, url)
            all_news.extend(news)
            time.sleep(1)  # Rate limiting
        
        logger.info(f"총 {len(all_news)}개 뉴스 수집 완료")
        return all_news
    
    def get_trending_topics(self, news_list: List[Dict]) -> List[str]:
        """트렌딩 키워드 추출"""
        from collections import Counter
        import re
        
        # 간단한 키워드 추출 (실제로는 더 정교한 NLP 필요)
        keywords = []
        for news in news_list:
            text = news['title'] + ' ' + news['summary']
            # 한글 2글자 이상 단어 추출
            words = re.findall(r'[가-힣]{2,}', text)
            keywords.extend(words)
        
        # 불용어 제거 (간단한 예시)
        stopwords = {'것으로', '있는', '하는', '되는', '대한', '관련', '위한', '통해', '때문에'}
        keywords = [w for w in keywords if w not in stopwords]
        
        # 빈도수 기반 상위 10개
        counter = Counter(keywords)
        trending = [word for word, count in counter.most_common(10)]
        
        logger.info(f"트렌딩 키워드: {trending}")
        return trending
    
    def filter_economic_news(self, news_list: List[Dict]) -> List[Dict]:
        """경제 관련 뉴스 필터링"""
        economic_keywords = [
            '주식', '증시', '코스피', '코스닥', '환율', '금리', 
            '투자', '재테크', '부동산', '경기', '인플레이션',
            '금융', '은행', '채권', '펀드', '암호화폐', '비트코인'
        ]
        
        filtered = []
        for news in news_list:
            text = news['title'] + ' ' + news['summary']
            if any(keyword in text for keyword in economic_keywords):
                filtered.append(news)
        
        logger.info(f"{len(news_list)}개 중 {len(filtered)}개 경제 뉴스 필터링")
        return filtered


# 테스트 코드
if __name__ == "__main__":
    logger.add("logs/news_scraper.log", rotation="1 day")
    
    scraper = NewsScraper()
    news = scraper.fetch_all_news()
    
    if news:
        filtered_news = scraper.filter_economic_news(news)
        trending = scraper.get_trending_topics(filtered_news)
        
        print(f"\n총 {len(news)}개 뉴스 수집")
        print(f"경제 뉴스 {len(filtered_news)}개 필터링")
        print(f"\n트렌딩 키워드: {', '.join(trending)}")
        
        print("\n최신 뉴스 3개:")
        for i, n in enumerate(filtered_news[:3], 1):
            print(f"\n{i}. [{n['source']}] {n['title']}")
            print(f"   {n['summary'][:100]}...")
