"""
메인 실행 파일 - 경제 유튜브 Shorts 자동화 시스템
"""
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
import yaml
import json

# 모듈 임포트
from src.data_collection.news_scraper import NewsScraper
from src.data_collection.stock_api import StockDataCollector
from src.script_generation.gpt_script import ScriptGenerator
from src.tts.tts_generator import TTSGenerator
from src.video_generation.video_creator import VideoCreator
from src.youtube_upload.uploader import YouTubeUploader


class EconomicShortsAutomation:
    """경제 Shorts 자동화 메인 클래스"""
    
    def __init__(self, config_path='config/config.yaml'):
        # 환경변수 로드
        load_dotenv()
        
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # 로깅 설정
        self._setup_logging()
        
        # 모듈 초기화
        self.news_scraper = NewsScraper()
        self.stock_collector = StockDataCollector()
        self.script_generator = ScriptGenerator(config_path)
        self.tts_generator = TTSGenerator(config_path)
        self.video_creator = VideoCreator(config_path)
        self.youtube_uploader = YouTubeUploader(config_path)
        
        logger.info("경제 Shorts 자동화 시스템 초기화 완료")
    
    def _setup_logging(self):
        """로깅 설정"""
        log_config = self.config['logging']
        
        # 로그 디렉토리 생성
        Path('logs').mkdir(exist_ok=True)
        
        # 로거 설정
        logger.add(
            log_config['file']['path'],
            rotation=log_config['rotation'],
            retention=log_config['retention'],
            level=log_config['level'],
            format=log_config['format']
        )
    
    def collect_data(self) -> dict:
        """데이터 수집 단계"""
        logger.info("=" * 60)
        logger.info("1단계: 데이터 수집 시작")
        logger.info("=" * 60)
        
        # 뉴스 수집
        news = self.news_scraper.fetch_all_news()
        filtered_news = self.news_scraper.filter_economic_news(news)
        
        # 주식/시장 데이터 수집
        market_summary = self.stock_collector.get_market_summary()
        stories = self.stock_collector.get_interesting_stories()
        
        # 데이터 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        data_dir = Path('data/raw')
        data_dir.mkdir(parents=True, exist_ok=True)
        
        with open(data_dir / f'news_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(filtered_news, f, ensure_ascii=False, indent=2)
        
        with open(data_dir / f'market_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump({'summary': market_summary, 'stories': stories}, f, ensure_ascii=False, indent=2)
        
        logger.info(f"뉴스 {len(filtered_news)}개, 시장 이슈 {len(stories)}개 수집 완료")
        
        return {
            'news': filtered_news,
            'market_summary': market_summary,
            'stories': stories
        }
    
    def generate_content(self, data: dict) -> list:
        """콘텐츠 생성 단계"""
        logger.info("=" * 60)
        logger.info("2단계: 스크립트 생성 시작")
        logger.info("=" * 60)
        
        # 스크립트 생성을 위한 주제 선정
        topics_data = []
        
        # 1. 시장 이슈 기반
        for story in data['stories'][:2]:  # 상위 2개
            topics_data.append({
                'topic': story['title'],
                'data': story
            })
        
        # 2. 주요 뉴스 기반
        for news in data['news'][:2]:  # 상위 2개
            topics_data.append({
                'topic': news['title'],
                'data': {
                    'source': news['source'],
                    'content': news['summary']
                }
            })
        
        # 스크립트 생성
        scripts = self.script_generator.generate_multiple_scripts(topics_data, count=3)
        
        # 스크립트 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        script_dir = Path('data/scripts')
        script_dir.mkdir(parents=True, exist_ok=True)
        
        with open(script_dir / f'scripts_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(scripts, f, ensure_ascii=False, indent=2)
        
        logger.info(f"{len(scripts)}개 스크립트 생성 완료")
        
        return scripts
    
    def produce_videos(self, scripts: list) -> list:
        """비디오 제작 단계"""
        logger.info("=" * 60)
        logger.info("3단계: 비디오 제작 시작")
        logger.info("=" * 60)
        
        produced_videos = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for i, script in enumerate(scripts, 1):
            logger.info(f"\n비디오 {i}/{len(scripts)} 제작 중: {script['title']}")
            
            try:
                # 1. TTS 생성
                audio_path = f"data/audio/{timestamp}_{i:02d}.mp3"
                logger.info("  → TTS 생성 중...")
                
                if not self.tts_generator.generate_audio(script['script'], audio_path):
                    logger.error(f"  ✗ TTS 생성 실패")
                    continue
                
                logger.info(f"  ✓ TTS 완료: {audio_path}")
                
                # 2. 비디오 생성
                video_path = f"data/videos/{timestamp}_{i:02d}_shorts.mp4"
                logger.info("  → 비디오 생성 중...")
                
                if not self.video_creator.create_shorts_video(
                    audio_path=audio_path,
                    script_text=script['script'],
                    output_path=video_path,
                    title_text=script.get('hook', '')
                ):
                    logger.error(f"  ✗ 비디오 생성 실패")
                    continue
                
                logger.info(f"  ✓ 비디오 완료: {video_path}")
                
                # 3. 썸네일 생성
                thumbnail_path = f"data/videos/{timestamp}_{i:02d}_thumbnail.jpg"
                logger.info("  → 썸네일 생성 중...")
                
                self.video_creator.create_thumbnail(
                    script.get('thumbnail_text', script['title'][:15]),
                    thumbnail_path
                )
                
                logger.info(f"  ✓ 썸네일 완료: {thumbnail_path}")
                
                produced_videos.append({
                    'script': script,
                    'video_path': video_path,
                    'audio_path': audio_path,
                    'thumbnail_path': thumbnail_path
                })
                
                logger.info(f"✅ 비디오 {i} 제작 완료!\n")
                
            except Exception as e:
                logger.error(f"비디오 {i} 제작 실패: {e}")
                continue
        
        logger.info(f"총 {len(produced_videos)}개 비디오 제작 완료")
        return produced_videos
    
    def upload_videos(self, videos: list) -> list:
        """유튜브 업로드 단계"""
        logger.info("=" * 60)
        logger.info("4단계: 유튜브 업로드 시작")
        logger.info("=" * 60)
        
        if not self.config['youtube']['auto_upload']:
            logger.info("자동 업로드가 비활성화되어 있습니다")
            return []
        
        uploaded = []
        
        for i, video in enumerate(videos, 1):
            logger.info(f"\n비디오 {i}/{len(videos)} 업로드 중...")
            
            try:
                video_id = self.youtube_uploader.upload_from_script(
                    video_path=video['video_path'],
                    script_data=video['script'],
                    thumbnail_path=video['thumbnail_path']
                )
                
                if video_id:
                    video['video_id'] = video_id
                    video['url'] = f"https://www.youtube.com/watch?v={video_id}"
                    uploaded.append(video)
                    logger.info(f"✅ 업로드 완료: {video['url']}\n")
                else:
                    logger.error(f"✗ 업로드 실패\n")
                
            except Exception as e:
                logger.error(f"업로드 실패: {e}")
                continue
        
        logger.info(f"총 {len(uploaded)}개 비디오 업로드 완료")
        return uploaded
    
    def run_single(self):
        """단일 실행 모드"""
        logger.info("\n🚀 경제 Shorts 자동화 시작 (단일 실행 모드)\n")
        
        try:
            # 1. 데이터 수집
            data = self.collect_data()
            
            # 2. 스크립트 생성
            scripts = self.generate_content(data)
            
            if not scripts:
                logger.error("생성된 스크립트가 없습니다")
                return
            
            # 3. 비디오 제작
            videos = self.produce_videos(scripts)
            
            if not videos:
                logger.error("제작된 비디오가 없습니다")
                return
            
            # 4. 유튜브 업로드
            uploaded = self.upload_videos(videos)
            
            # 결과 출력
            logger.info("\n" + "=" * 60)
            logger.info("✅ 자동화 완료!")
            logger.info("=" * 60)
            logger.info(f"제작된 비디오: {len(videos)}개")
            logger.info(f"업로드된 비디오: {len(uploaded)}개")
            
            if uploaded:
                logger.info("\n업로드된 비디오 목록:")
                for i, v in enumerate(uploaded, 1):
                    logger.info(f"{i}. {v['script']['title']}")
                    logger.info(f"   URL: {v['url']}")
            
        except Exception as e:
            logger.error(f"자동화 실행 중 오류 발생: {e}")
            raise
    
    def run_scheduler(self, mode='hourly', interval=2):
        """스케줄러 모드"""
        logger.info(f"\n⏰ 스케줄러 시작 (모드: {mode}, 간격: {interval})")
        
        import schedule
        import time
        
        if mode == 'hourly':
            schedule.every(interval).hours.do(self.run_single)
        elif mode == 'daily':
            # 설정된 시간에 실행
            times = self.config['scheduler']['daily']['times']
            for t in times:
                schedule.every().day.at(t).do(self.run_single)
        
        logger.info("스케줄러 대기 중... (Ctrl+C로 종료)")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 1분마다 체크
        except KeyboardInterrupt:
            logger.info("\n스케줄러 종료")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='경제 유튜브 Shorts 자동화 시스템')
    parser.add_argument('--mode', choices=['single', 'auto'], default='single',
                       help='실행 모드 (single: 1회 실행, auto: 자동 스케줄)')
    parser.add_argument('--interval', type=int, default=2,
                       help='자동 실행 간격 (시간, 기본값: 2)')
    parser.add_argument('--config', default='config/config.yaml',
                       help='설정 파일 경로')
    parser.add_argument('--duration', type=int, choices=range(20, 171), metavar='20-170',
                       help='비디오 길이 (초) - 20초~170초(2분50초) 사이 선택 가능')
    parser.add_argument('--preset', choices=['quick', 'short', 'standard', 'detailed', 'extended', 'maximum'],
                       help='비디오 길이 프리셋 (quick:20초, short:30초, standard:60초, detailed:90초, extended:120초, maximum:170초)')
    
    args = parser.parse_args()
    
    # 비디오 길이 설정
    if args.preset:
        # 프리셋 사용
        presets = {
            'quick': 20,
            'short': 30,
            'standard': 60,
            'detailed': 90,
            'extended': 120,
            'maximum': 170
        }
        duration = presets[args.preset]
        logger.info(f"프리셋 '{args.preset}' 선택: {duration}초 비디오 생성")
    elif args.duration:
        duration = args.duration
        logger.info(f"사용자 지정 길이: {duration}초 비디오 생성")
    else:
        duration = None  # config 기본값 사용
    
    # 시스템 초기화
    automation = EconomicShortsAutomation(args.config)
    
    # duration을 config에 임시로 설정
    if duration is not None:
        automation.config['video']['duration'] = duration
        logger.info(f"비디오 길이 설정: {duration}초")
    
    # 실행
    if args.mode == 'single':
        automation.run_single()
    else:
        automation.run_scheduler(mode='hourly', interval=args.interval)


if __name__ == "__main__":
    main()
