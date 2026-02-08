"""
🍌 Banana 모드 빠른 테스트 (OpenAI 없이)
기본 배경으로 20초 비디오 생성
"""
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# 환경변수 로드
load_dotenv()

# 모듈 임포트
from src.tts.tts_generator import TTSGenerator
from src.video_generation.banana_video_creator import BananaVideoCreator


def quick_test():
    """빠른 테스트: 20초 비디오"""
    
    logger.info("=" * 80)
    logger.info("🍌 Banana 모드 빠른 테스트")
    logger.info("=" * 80)
    
    # 테스트 스크립트
    topic = "비트코인 급등"
    script = "비트코인이 오늘 10% 급등했습니다. 현재 가격은 5천850만원입니다. 투자자들의 관심이 집중되고 있습니다. 전문가들은 신중한 투자를 권장합니다."
    duration = 20
    
    logger.info(f"📌 토픽: {topic}")
    logger.info(f"⏱️  목표 길이: {duration}초")
    logger.info(f"📝 스크립트: {script}")
    
    try:
        # 1. TTS 생성
        logger.info("")
        logger.info("1️⃣  TTS 생성 중...")
        
        tts_generator = TTSGenerator()
        
        timestamp = int(time.time() * 1000)
        audio_path = f"data/audio/quick_test_{timestamp}.mp3"
        Path(audio_path).parent.mkdir(parents=True, exist_ok=True)
        
        tts_generator.generate_audio(script, audio_path)
        audio_size = os.path.getsize(audio_path) / 1024
        logger.info(f"✅ TTS 완료: {audio_size:.1f} KB")
        
        # 2. Banana 비디오 생성
        logger.info("")
        logger.info("2️⃣  🍌 Banana 비디오 생성 중...")
        
        video_creator = BananaVideoCreator()
        
        output_path = f"data/videos/quick_test_{timestamp}.mp4"
        
        start_time = time.time()
        success = video_creator.create_banana_video(
            topic=topic,
            script_text=script,
            audio_path=audio_path,
            output_path=output_path,
            target_duration=duration,
            style='professional'
        )
        elapsed_time = time.time() - start_time
        
        if success and os.path.exists(output_path):
            video_size = os.path.getsize(output_path) / (1024 * 1024)
            
            logger.info("")
            logger.info("=" * 80)
            logger.info("✅ 🍌 테스트 성공!")
            logger.info("=" * 80)
            logger.info(f"📹 비디오: {output_path}")
            logger.info(f"💾 크기: {video_size:.1f} MB")
            logger.info(f"⏱️  소요 시간: {elapsed_time:.1f}초")
            logger.info("=" * 80)
            
            # 파일 확인
            logger.info("")
            logger.info("📁 생성된 파일:")
            os.system(f"ls -lh {output_path}")
            
            return True
        else:
            logger.error("❌ 비디오 생성 실패")
            return False
    
    except Exception as e:
        logger.error(f"❌ 오류 발생: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == '__main__':
    success = quick_test()
    sys.exit(0 if success else 1)
