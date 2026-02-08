"""
🍌 Banana 모드 - AutoPilot 실행 스크립트
토픽만 입력하면 자동으로 비디오 생성 (20초 ~ 30분)
"""
import os
import sys
import argparse
import time
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# 환경변수 로드
load_dotenv()

# 모듈 임포트
from src.script_generation.gpt_script import ScriptGenerator
from src.tts.tts_generator import TTSGenerator
from src.video_generation.banana_video_creator import BananaVideoCreator


def main():
    parser = argparse.ArgumentParser(description='🍌 Banana 모드 - AutoPilot 비디오 생성')
    parser.add_argument(
        '--topic',
        type=str,
        required=True,
        help='비디오 토픽 (예: "비트코인 가격 분석", "코스피 급등 원인")'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='목표 영상 길이 (초, 20~1800). 기본값: 60초'
    )
    parser.add_argument(
        '--style',
        type=str,
        default='professional',
        choices=['professional', 'cinematic', 'anime', '3d'],
        help='스타일 템플릿. 기본값: professional'
    )
    parser.add_argument(
        '--preset',
        type=str,
        default=None,
        choices=['quick', 'short', 'standard', 'shorts', 'medium', 'long', 'extended', 'maximum'],
        help='길이 프리셋 (quick=20초, short=30초, standard=60초, shorts=120초, medium=300초, long=600초, extended=1200초, maximum=1800초)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='출력 비디오 경로 (지정하지 않으면 자동 생성)'
    )
    
    args = parser.parse_args()
    
    # 프리셋 적용
    duration_presets = {
        'quick': 20,
        'short': 30,
        'standard': 60,
        'shorts': 120,
        'medium': 300,
        'long': 600,
        'extended': 1200,
        'maximum': 1800
    }
    
    if args.preset:
        target_duration = duration_presets[args.preset]
        logger.info(f"📋 프리셋 적용: {args.preset} → {target_duration}초")
    else:
        target_duration = args.duration
    
    # 길이 검증
    if not (20 <= target_duration <= 1800):
        logger.error("❌ 영상 길이는 20초 ~ 1800초(30분) 사이여야 합니다.")
        sys.exit(1)
    
    logger.info("=" * 80)
    logger.info("🍌 BANANA 모드 시작!")
    logger.info("=" * 80)
    logger.info(f"📌 토픽: {args.topic}")
    logger.info(f"⏱️  목표 길이: {target_duration}초 ({target_duration // 60}분 {target_duration % 60}초)")
    logger.info(f"🎨 스타일: {args.style}")
    logger.info("=" * 80)
    
    # 출력 경로 설정
    if args.output:
        output_path = args.output
    else:
        timestamp = int(time.time())
        output_path = f"data/videos/banana_{args.style}_{timestamp}.mp4"
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # 1단계: AI 스크립트 생성
        logger.info("")
        logger.info("=" * 80)
        logger.info("1️⃣  AI 스크립트 생성 중...")
        logger.info("=" * 80)
        
        script_generator = ScriptGenerator()
        
        # 길이에 맞는 스크립트 생성 (한국어 평균 3.5자/초)
        target_chars = int(target_duration * 3.5)
        
        script_data = script_generator.generate_script(
            topic=args.topic,
            target_length=target_chars
        )
        
        script_text = script_data['script']
        logger.info(f"✅ 스크립트 생성 완료 ({len(script_text)}자)")
        logger.info(f"📝 스크립트 미리보기: {script_text[:100]}...")
        
        # 2단계: TTS 음성 생성
        logger.info("")
        logger.info("=" * 80)
        logger.info("2️⃣  TTS 음성 생성 중...")
        logger.info("=" * 80)
        
        tts_generator = TTSGenerator()
        
        timestamp = int(time.time())
        audio_path = f"data/audio/banana_narration_{timestamp}.mp3"
        Path(audio_path).parent.mkdir(parents=True, exist_ok=True)
        
        tts_generator.generate_audio(script_text, audio_path)
        
        audio_size = os.path.getsize(audio_path) / 1024  # KB
        logger.info(f"✅ TTS 생성 완료: {audio_path} ({audio_size:.1f} KB)")
        
        # 3단계: Banana 모드 비디오 생성
        logger.info("")
        logger.info("=" * 80)
        logger.info("3️⃣  🍌 Banana 모드 비디오 생성 중...")
        logger.info("=" * 80)
        
        video_creator = BananaVideoCreator()
        
        success = video_creator.create_banana_video(
            topic=args.topic,
            script_text=script_text,
            audio_path=audio_path,
            output_path=output_path,
            target_duration=target_duration,
            style=args.style
        )
        
        if success:
            video_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            logger.info("")
            logger.info("=" * 80)
            logger.info("✅ 🍌 Banana 모드 완료!")
            logger.info("=" * 80)
            logger.info(f"📹 비디오: {output_path}")
            logger.info(f"💾 크기: {video_size:.1f} MB")
            logger.info(f"⏱️  길이: {target_duration}초 ({target_duration // 60}분 {target_duration % 60}초)")
            logger.info("=" * 80)
            
            # 4단계 (선택): AI 썸네일 생성
            logger.info("")
            logger.info("4️⃣  (선택) AI 썸네일 생성 중...")
            
            thumbnail_path = output_path.replace('.mp4', '_thumbnail.png')
            if video_creator.create_thumbnail(args.topic, thumbnail_path):
                thumb_size = os.path.getsize(thumbnail_path) / 1024  # KB
                logger.info(f"✅ 썸네일 생성 완료: {thumbnail_path} ({thumb_size:.1f} KB)")
            
        else:
            logger.error("❌ 비디오 생성 실패")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"❌ 오류 발생: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == '__main__':
    main()
