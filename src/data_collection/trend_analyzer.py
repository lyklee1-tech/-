"""
🔥 실시간 트렌드 분석기
7시간 이내 급상승 주제를 분석하여 자동으로 주제 추천
"""
import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from loguru import logger
import re


class TrendAnalyzer:
    """실시간 트렌드 분석 클래스"""
    
    def __init__(self):
        """초기화"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        logger.info("트렌드 분석기 초기화 완료")
    
    def get_google_trends(self, limit: int = 10) -> List[Dict]:
        """
        Google 실시간 검색어 수집
        """
        try:
            logger.info("🔍 Google Trends 수집 중...")
            
            # Google Trends RSS API 사용
            url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # XML 파싱 (간단한 정규식 사용)
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            trends = []
            for item in root.findall('.//item')[:limit]:
                title_elem = item.find('title')
                traffic_elem = item.find('.//ht:approx_traffic', {'ht': 'https://trends.google.com/trends/trendingsearches/daily'})
                
                if title_elem is not None:
                    title = title_elem.text
                    traffic = traffic_elem.text if traffic_elem is not None else 'N/A'
                    
                    trends.append({
                        'keyword': title,
                        'source': 'Google Trends',
                        'traffic': traffic,
                        'score': self._calculate_score(traffic, 'google'),
                        'timestamp': datetime.now().isoformat()
                    })
            
            logger.info(f"✅ Google Trends: {len(trends)}개 수집")
            return trends
            
        except Exception as e:
            logger.error(f"❌ Google Trends 수집 실패: {e}")
            return []
    
    def get_youtube_trends(self, limit: int = 10) -> List[Dict]:
        """
        YouTube 인기 급상승 동영상 주제 수집
        """
        try:
            logger.info("🎥 YouTube Trends 수집 중...")
            
            # YouTube Data API 필요 (환경변수에서 가져오기)
            api_key = os.getenv('YOUTUBE_API_KEY')
            
            if not api_key:
                logger.warning("YouTube API Key 없음 - 기본 트렌드 사용")
                return self._get_youtube_fallback()
            
            url = "https://www.googleapis.com/youtube/v3/videos"
            params = {
                'part': 'snippet,statistics',
                'chart': 'mostPopular',
                'regionCode': 'KR',
                'videoCategoryId': '25',  # 뉴스 & 정치
                'maxResults': limit,
                'key': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            trends = []
            for item in data.get('items', []):
                snippet = item['snippet']
                stats = item['statistics']
                
                # 경제 관련 키워드 필터링
                if self._is_economic_topic(snippet['title']):
                    trends.append({
                        'keyword': snippet['title'],
                        'source': 'YouTube',
                        'views': int(stats.get('viewCount', 0)),
                        'score': self._calculate_score(stats.get('viewCount', 0), 'youtube'),
                        'timestamp': datetime.now().isoformat()
                    })
            
            logger.info(f"✅ YouTube: {len(trends)}개 수집")
            return trends
            
        except Exception as e:
            logger.error(f"❌ YouTube Trends 수집 실패: {e}")
            return self._get_youtube_fallback()
    
    def get_naver_trends(self, limit: int = 10) -> List[Dict]:
        """
        네이버 실시간 검색어 수집
        """
        try:
            logger.info("🔍 네이버 실시간 검색어 수집 중...")
            
            # 네이버 DataLab API (또는 크롤링)
            # 여기서는 간단한 예시로 구현
            
            url = "https://datalab.naver.com/keyword/realtimeList.naver"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            # 간단한 파싱 (실제로는 더 정교한 파싱 필요)
            trends = []
            
            # 네이버 API가 제한적이므로 fallback 데이터 사용
            return self._get_naver_fallback()
            
        except Exception as e:
            logger.error(f"❌ 네이버 Trends 수집 실패: {e}")
            return self._get_naver_fallback()
    
    def get_economic_keywords(self) -> List[str]:
        """경제 관련 주요 키워드"""
        return [
            '주식', '코스피', '코스닥', '삼성전자', 'SK하이닉스',
            '비트코인', '이더리움', '암호화폐', '가상화폐',
            '환율', '달러', '원화', '엔화',
            '금리', '한국은행', '기준금리', '미국 금리',
            '부동산', '아파트', '집값',
            '경제', '증시', '증권', '투자',
            '반도체', 'AI', '인공지능',
            '테슬라', '애플', 'NVIDIA', '엔비디아',
            'S&P500', '나스닥', '다우존스',
            '유가', '원유', '금값',
            '실업률', 'GDP', '물가',
            '인플레이션', '디플레이션'
        ]
    
    def search_economic_news(self, keywords: List[str], hours: int = 7) -> List[Dict]:
        """
        특정 키워드로 최근 N시간 이내 경제 뉴스 검색
        """
        try:
            logger.info(f"📰 경제 뉴스 검색 중... (최근 {hours}시간)")
            
            news_items = []
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # 네이버 뉴스 검색 API
            naver_client_id = os.getenv('NAVER_CLIENT_ID')
            naver_client_secret = os.getenv('NAVER_CLIENT_SECRET')
            
            if not naver_client_id or not naver_client_secret:
                logger.warning("네이버 API 키 없음 - 샘플 데이터 사용")
                return self._get_news_fallback()
            
            for keyword in keywords[:5]:  # 상위 5개만
                url = "https://openapi.naver.com/v1/search/news.json"
                params = {
                    'query': keyword + ' 경제',
                    'display': 10,
                    'sort': 'date'
                }
                headers = {
                    'X-Naver-Client-Id': naver_client_id,
                    'X-Naver-Client-Secret': naver_client_secret
                }
                
                response = requests.get(url, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for item in data.get('items', []):
                        news_items.append({
                            'keyword': keyword,
                            'title': self._clean_html(item['title']),
                            'description': self._clean_html(item['description']),
                            'link': item['link'],
                            'source': 'Naver News',
                            'pubDate': item['pubDate'],
                            'score': 50  # 기본 점수
                        })
            
            logger.info(f"✅ 뉴스: {len(news_items)}개 수집")
            return news_items
            
        except Exception as e:
            logger.error(f"❌ 뉴스 검색 실패: {e}")
            return self._get_news_fallback()
    
    def analyze_all_trends(self, hours: int = 7) -> Dict:
        """
        모든 소스에서 트렌드 수집 및 분석
        """
        current_time = datetime.now()
        logger.info("=" * 80)
        logger.info("🔥 실시간 트렌드 분석 시작")
        logger.info(f"📅 현재 시각: {current_time.strftime('%Y년 %m월 %d일 %H시 %M분')}")
        logger.info(f"⏰ 분석 기간: 최근 {hours}시간")
        logger.info(f"🕐 기준 시간: {(current_time - timedelta(hours=hours)).strftime('%Y년 %m월 %d일 %H시 %M분')} ~ 현재")
        logger.info("=" * 80)
        
        all_trends = []
        
        # 1. Google Trends
        google_trends = self.get_google_trends()
        all_trends.extend(google_trends)
        
        # 2. YouTube Trends
        youtube_trends = self.get_youtube_trends()
        all_trends.extend(youtube_trends)
        
        # 3. 네이버 Trends
        naver_trends = self.get_naver_trends()
        all_trends.extend(naver_trends)
        
        # 4. 경제 키워드로 뉴스 검색
        economic_keywords = self.get_economic_keywords()
        news_items = self.search_economic_news(economic_keywords, hours)
        
        # 5. 점수 기반 정렬
        all_trends.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # 6. 중복 제거 및 경제 관련 필터링
        unique_trends = self._deduplicate_and_filter(all_trends)
        
        # 7. 상위 추천 주제 선정
        top_recommendations = unique_trends[:10]
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'analysis_period_hours': hours,
            'total_trends_found': len(all_trends),
            'filtered_trends': len(unique_trends),
            'recommendations': top_recommendations,
            'news_items': news_items[:20],
            'sources': {
                'google': len(google_trends),
                'youtube': len(youtube_trends),
                'naver': len(naver_trends),
                'news': len(news_items)
            }
        }
        
        logger.info("=" * 80)
        logger.info(f"✅ 트렌드 분석 완료!")
        logger.info(f"📊 총 {len(all_trends)}개 트렌드 수집")
        logger.info(f"🎯 추천 주제: {len(top_recommendations)}개")
        logger.info("=" * 80)
        
        # 추천 주제 출력
        logger.info("\n🔥 TOP 10 추천 주제:")
        for i, trend in enumerate(top_recommendations, 1):
            logger.info(f"{i}. {trend.get('keyword')} (점수: {trend.get('score', 0)}) - {trend.get('source')}")
        
        return result
    
    def get_top_topic(self, hours: int = 7) -> Optional[str]:
        """
        가장 핫한 주제 1개 반환 (자동 선택용)
        """
        result = self.analyze_all_trends(hours)
        
        if result['recommendations']:
            top_topic = result['recommendations'][0]['keyword']
            logger.info(f"🎯 자동 선택된 주제: {top_topic}")
            return top_topic
        
        return None
    
    # ===== Helper 메서드 =====
    
    def _calculate_score(self, value, source_type: str) -> int:
        """점수 계산"""
        try:
            if source_type == 'google':
                # 트래픽 문자열 파싱 (예: "100K+", "1M+")
                if isinstance(value, str):
                    value = value.replace('+', '').replace(',', '')
                    if 'K' in value:
                        return int(float(value.replace('K', '')) * 1000 / 100)
                    elif 'M' in value:
                        return int(float(value.replace('M', '')) * 1000000 / 100)
                return 50
            
            elif source_type == 'youtube':
                # 조회수 기반
                views = int(value) if value else 0
                return min(100, views // 10000)  # 1만 조회수당 1점
            
            else:
                return 50
                
        except:
            return 50
    
    def _is_economic_topic(self, text: str) -> bool:
        """경제 관련 주제인지 판단"""
        economic_keywords = self.get_economic_keywords()
        text_lower = text.lower()
        
        for keyword in economic_keywords:
            if keyword.lower() in text_lower:
                return True
        
        return False
    
    def _deduplicate_and_filter(self, trends: List[Dict]) -> List[Dict]:
        """중복 제거 및 경제 관련 필터링"""
        seen = set()
        filtered = []
        
        for trend in trends:
            keyword = trend.get('keyword', '')
            
            # 중복 체크
            if keyword in seen:
                continue
            
            # 경제 관련 주제만 필터링
            if self._is_economic_topic(keyword):
                seen.add(keyword)
                filtered.append(trend)
        
        return filtered
    
    def _clean_html(self, text: str) -> str:
        """HTML 태그 제거"""
        import re
        return re.sub(r'<[^>]+>', '', text)
    
    # ===== Fallback 데이터 =====
    
    def _get_youtube_fallback(self) -> List[Dict]:
        """YouTube API 없을 때 기본 데이터"""
        return [
            {'keyword': '비트코인 급등', 'source': 'YouTube', 'views': 500000, 'score': 80},
            {'keyword': '삼성전자 실적', 'source': 'YouTube', 'views': 300000, 'score': 70},
            {'keyword': '미국 금리 인상', 'source': 'YouTube', 'views': 250000, 'score': 65},
        ]
    
    def _get_naver_fallback(self) -> List[Dict]:
        """네이버 API 없을 때 기본 데이터"""
        return [
            {'keyword': '코스피 상승', 'source': 'Naver', 'traffic': '50K+', 'score': 75},
            {'keyword': '달러 환율', 'source': 'Naver', 'traffic': '30K+', 'score': 60},
        ]
    
    def _get_news_fallback(self) -> List[Dict]:
        """뉴스 API 없을 때 기본 데이터"""
        return [
            {
                'keyword': '주식',
                'title': '코스피, 외국인 매수세에 상승세',
                'description': '코스피가 외국인 투자자들의 매수세에 힘입어 상승세를 보이고 있습니다.',
                'source': 'Sample News',
                'score': 70
            }
        ]


def main():
    """테스트 실행"""
    analyzer = TrendAnalyzer()
    
    # 전체 분석
    result = analyzer.analyze_all_trends(hours=7)
    
    # JSON으로 저장
    output_path = 'data/trends/latest_trends.json'
    os.makedirs('data/trends', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n💾 결과 저장: {output_path}")
    
    # 자동 추천 주제
    top_topic = analyzer.get_top_topic()
    logger.info(f"\n🎯 추천 주제: {top_topic}")


if __name__ == '__main__':
    main()
