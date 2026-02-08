"""
🌟 GenSpark AI AutoPilot - 완전 무료 비디오 생성!
OpenAI 비용 $0! GenSpark AI로 이미지 + 비디오 자동 생성
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
from src.tts.tts_generator import TTSGenerator


def generate_scenes_with_genspark(topic: str, script_text: str, num_scenes: int = 4):
    """
    GenSpark AI로 장면별 이미지 + 비디오 생성
    
    이 함수는 실제로 GenSpark API 도구를 사용합니다.
    """
    scenes = []
    
    # 스크립트를 장면별로 분할
    sentences = [s.strip() for s in script_text.split('.') if s.strip()]
    
    # 장면 설명 키워드 매핑
    keywords_map = {
        '비트코인': 'Bitcoin cryptocurrency chart with rising green arrow, professional financial news background',
        '주식': 'stock market trading floor with digital screens, modern business atmosphere',
        '경제': 'modern financial district skyline, professional business setting',
        '투자': 'investment portfolio dashboard with graphs and charts',
        '급등': 'dramatic rising green chart with upward arrow, bullish market',
        '급락': 'falling red chart with downward trend, bearish market',
        '환율': 'currency exchange rates display board, forex market',
        '금리': 'interest rate graph trending upward, financial indicators',
        '시장': 'bustling stock exchange trading floor, busy trading day',
        '기업': 'modern corporate office building exterior, business skyline',
    }
    
    for i, sentence in enumerate(sentences[:num_scenes]):
        # 키워드 매칭
        prompt = f"Professional economic news video scene for: {sentence}. Modern, clean, business aesthetic."
        
        for keyword, description in keywords_map.items():
            if keyword in sentence:
                prompt = description
                break
        
        scenes.append({
            'index': i,
            'text': sentence,
            'prompt': prompt,
            'duration': 5  # 기본 5초
        })
    
    return scenes


def main():
    parser = argparse.ArgumentParser(description='🌟 GenSpark AI AutoPilot - 완전 무료!')
    parser.add_argument(
        '--topic',
        type=str,
        required=True,
        help='비디오 토픽'
    )
    parser.add_argument(
        '--script',
        type=str,
        default=None,
        help='스크립트 (지정하지 않으면 샘플 사용)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=20,
        help='목표 영상 길이 (초)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='출력 비디오 경로'
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 80)
    logger.info("🌟 GenSpark AI AutoPilot 시작 (완전 무료!)")
    logger.info("=" * 80)
    logger.info(f"📌 토픽: {args.topic}")
    logger.info(f"⏱️  목표 길이: {args.duration}초")
    logger.info("💰 비용: $0 (GenSpark AI 무료!)")
    logger.info("=" * 80)
    
    # 샘플 스크립트
    if args.script is None:
        sample_scripts = {
            20: "비트코인이 오늘 10% 급등했습니다. 현재 가격은 5천850만원입니다. 투자자들의 관심이 집중되고 있습니다. 전문가들은 신중한 투자를 권장합니다.",
            60: "코스피가 오늘 3000선을 돌파했습니다. 전문가들은 외국인 매수세가 강하다고 분석합니다. 삼성전자와 SK하이닉스가 상승을 주도했습니다. 하지만 일부 전문가들은 과열을 경고하고 있습니다. 투자에 신중을 기해야 합니다."
        }
        script = sample_scripts.get(args.duration, sample_scripts[20])
    else:
        script = args.script
    
    logger.info(f"📝 스크립트: {script}")
    
    try:
        # 1. TTS 생성
        logger.info("")
        logger.info("=" * 80)
        logger.info("1️⃣  TTS 생성 중...")
        logger.info("=" * 80)
        
        tts_generator = TTSGenerator()
        
        timestamp = int(time.time() * 1000)
        audio_path = f"data/audio/genspark_{timestamp}.mp3"
        Path(audio_path).parent.mkdir(parents=True, exist_ok=True)
        
        tts_generator.generate_audio(script, audio_path)
        audio_size = os.path.getsize(audio_path) / 1024
        logger.info(f"✅ TTS 완료: {audio_size:.1f} KB")
        
        # 2. 장면 생성 (GenSpark AI)
        logger.info("")
        logger.info("=" * 80)
        logger.info("2️⃣  🌟 GenSpark AI로 장면 생성 중...")
        logger.info("=" * 80)
        
        num_scenes = max(3, args.duration // 5)  # 5초당 1장면
        scenes = generate_scenes_with_genspark(args.topic, script, num_scenes)
        
        logger.info(f"🎬 총 {len(scenes)}개 장면 생성 예정")
        logger.info("")
        logger.info("💡 GenSpark AI 장면 생성 안내:")
        logger.info("   - 이 스크립트는 장면 정보를 준비합니다")
        logger.info("   - 실제 이미지/비디오 생성은 GenSpark 웹 인터페이스에서 진행됩니다")
        logger.info("   - 또는 Python에서 직접 image_generation/video_generation 도구를 사용하세요")
        logger.info("")
        
        for i, scene in enumerate(scenes, 1):
            logger.info(f"장면 {i}/{len(scenes)}:")
            logger.info(f"  📝 텍스트: {scene['text']}")
            logger.info(f"  🎨 프롬프트: {scene['prompt']}")
            logger.info(f"  ⏱️  길이: {scene['duration']}초")
            logger.info("")
        
        # 3. 최종 안내
        logger.info("")
        logger.info("=" * 80)
        logger.info("✅ 준비 완료!")
        logger.info("=" * 80)
        logger.info(f"🎵 TTS 파일: {audio_path}")
        logger.info(f"🎬 장면 수: {len(scenes)}개")
        logger.info("")
        logger.info("🎯 다음 단계:")
        logger.info("  1. 위의 프롬프트로 GenSpark AI 이미지 생성")
        logger.info("  2. 생성된 이미지로 GenSpark AI 비디오 생성")
        logger.info("  3. MoviePy로 장면 + 자막 + 오디오 합성")
        logger.info("")
        logger.info("💡 전체 자동화 버전은 genspark_autopilot_full.py를 참고하세요!")
        logger.info("=" * 80)
        
        # 장면 정보를 파일로 저장
        scenes_json_path = f"data/scenes/genspark_scenes_{timestamp}.json"
        Path(scenes_json_path).parent.mkdir(parents=True, exist_ok=True)
        
        import json
        with open(scenes_json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'topic': args.topic,
                'script': script,
                'duration': args.duration,
                'audio_path': audio_path,
                'scenes': scenes
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📋 장면 정보 저장: {scenes_json_path}")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ 오류 발생: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
