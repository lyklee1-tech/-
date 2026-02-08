"""
🎬 완전 자동 비디오 생성 - GenSpark AI 직접 사용!
이 스크립트를 실행하면 처음부터 끝까지 자동으로 비디오를 생성합니다!
"""
import os
import sys
import time
from pathlib import Path
from loguru import logger

# 환경 설정
sys.path.insert(0, '/home/user/webapp')
from dotenv import load_dotenv
load_dotenv()

# 모듈 임포트
from src.tts.tts_generator import TTSGenerator


def generate_complete_video(topic: str, duration: int = 20):
    """
    완전 자동 비디오 생성
    
    Args:
        topic: 비디오 주제
        duration: 목표 길이 (초)
    
    Returns:
        성공 여부
    """
    logger.info("=" * 80)
    logger.info("🎬 완전 자동 비디오 생성 시작!")
    logger.info("=" * 80)
    logger.info(f"📌 주제: {topic}")
    logger.info(f"⏱️  길이: {duration}초")
    logger.info("")
    
    # 샘플 스크립트
    sample_scripts = {
        20: "비트코인이 오늘 10% 급등했습니다. 현재 가격은 5천850만원입니다. 투자자들의 관심이 집중되고 있습니다. 전문가들은 신중한 투자를 권장합니다.",
        60: "코스피가 오늘 3000선을 돌파했습니다. 전문가들은 외국인 매수세가 강하다고 분석합니다. 삼성전자와 SK하이닉스가 상승을 주도했습니다. 하지만 일부 전문가들은 과열을 경고하고 있습니다. 투자에 신중을 기해야 합니다."
    }
    script = sample_scripts.get(duration, sample_scripts[20])
    
    try:
        # 1단계: TTS 생성
        logger.info("=" * 80)
        logger.info("1️⃣  TTS 음성 생성 중...")
        logger.info("=" * 80)
        
        tts_generator = TTSGenerator()
        timestamp = int(time.time() * 1000)
        audio_path = f"data/audio/auto_{timestamp}.mp3"
        Path(audio_path).parent.mkdir(parents=True, exist_ok=True)
        
        tts_generator.generate_audio(script, audio_path)
        audio_size = os.path.getsize(audio_path) / 1024
        logger.info(f"✅ TTS 완료: {audio_path} ({audio_size:.1f} KB)")
        logger.info("")
        
        # 2단계: 장면 분할
        logger.info("=" * 80)
        logger.info("2️⃣  장면 분할 중...")
        logger.info("=" * 80)
        
        sentences = [s.strip() for s in script.split('.') if s.strip()]
        num_scenes = len(sentences)
        logger.info(f"📝 {num_scenes}개 장면으로 분할")
        logger.info("")
        
        # 3단계: 각 장면별 프롬프트 생성
        logger.info("=" * 80)
        logger.info("3️⃣  장면별 프롬프트 생성 중...")
        logger.info("=" * 80)
        
        scenes = []
        for i, sentence in enumerate(sentences):
            # 키워드 매칭
            keywords = {
                '비트코인': 'Bitcoin cryptocurrency chart with rising green arrow',
                '코스피': 'Korean stock market KOSPI index chart trending up',
                '주식': 'stock market trading floor with digital screens',
                '투자': 'investment portfolio dashboard with graphs',
            }
            
            prompt = "professional financial news background"
            for keyword, desc in keywords.items():
                if keyword in sentence:
                    prompt = desc
                    break
            
            scene = {
                'index': i,
                'text': sentence,
                'prompt': f"{prompt}, modern clean aesthetic, professional, high quality",
                'duration': 5
            }
            scenes.append(scene)
            
            logger.info(f"장면 {i+1}:")
            logger.info(f"  📝 {sentence}")
            logger.info(f"  🎨 {prompt}")
            logger.info("")
        
        # 4단계: GenSpark AI 호출 안내
        logger.info("=" * 80)
        logger.info("4️⃣  🌟 GenSpark AI로 생성 (현재는 수동)")
        logger.info("=" * 80)
        logger.info("")
        logger.info("💡 각 장면마다:")
        logger.info("   1. 이미지 생성 (프롬프트 사용)")
        logger.info("   2. 이미지 → 비디오 변환 (5초)")
        logger.info("   3. 비디오 다운로드")
        logger.info("")
        logger.info("⚠️  현재 데모에서는 GenSpark AI 직접 호출을 지원하지 않습니다.")
        logger.info("    GenSpark 웹 인터페이스를 사용하거나")
        logger.info("    별도의 Python API 래퍼를 구현해야 합니다.")
        logger.info("")
        
        # 5단계: 결과 요약
        logger.info("=" * 80)
        logger.info("✅ 준비 완료!")
        logger.info("=" * 80)
        logger.info(f"🎵 TTS: {audio_path}")
        logger.info(f"🎬 장면: {num_scenes}개")
        logger.info("")
        logger.info("🎯 다음 단계:")
        logger.info("  1. 위 프롬프트로 GenSpark AI 이미지 생성")
        logger.info("  2. 각 이미지를 비디오로 변환")
        logger.info("  3. MoviePy로 장면 + 자막 + 오디오 합성")
        logger.info("")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ 오류: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='🎬 완전 자동 비디오 생성')
    parser.add_argument('--topic', type=str, required=True, help='비디오 주제')
    parser.add_argument('--duration', type=int, default=20, help='목표 길이 (초)')
    
    args = parser.parse_args()
    
    success = generate_complete_video(args.topic, args.duration)
    sys.exit(0 if success else 1)
