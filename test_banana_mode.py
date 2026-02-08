"""
🍌 Banana 모드 테스트 스크립트
다양한 길이의 비디오를 자동 생성하여 시스템 검증
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
from src.script_generation.gpt_script import ScriptGenerator
from src.tts.tts_generator import TTSGenerator
from src.video_generation.banana_video_creator import BananaVideoCreator


# 테스트 시나리오
TEST_SCENARIOS = [
    {
        'name': '20초 빠른 뉴스',
        'topic': '비트코인이 오늘 급등',
        'duration': 20,
        'style': 'professional'
    },
    {
        'name': '1분 표준 뉴스',
        'topic': '코스피가 3000선 돌파',
        'duration': 60,
        'style': 'professional'
    },
    {
        'name': '5분 중간 분석',
        'topic': '환율 변동과 경제 영향',
        'duration': 300,
        'style': 'cinematic'
    },
]


def test_banana_mode():
    """Banana 모드 통합 테스트"""
    
    logger.info("=" * 80)
    logger.info("🍌 Banana 모드 테스트 시작")
    logger.info("=" * 80)
    
    # 모듈 초기화
    script_generator = ScriptGenerator()
    tts_generator = TTSGenerator()
    video_creator = BananaVideoCreator()
    
    results = []
    
    for i, scenario in enumerate(TEST_SCENARIOS, 1):
        logger.info("")
        logger.info("=" * 80)
        logger.info(f"테스트 {i}/{len(TEST_SCENARIOS)}: {scenario['name']}")
        logger.info("=" * 80)
        logger.info(f"📌 토픽: {scenario['topic']}")
        logger.info(f"⏱️  목표 길이: {scenario['duration']}초")
        logger.info(f"🎨 스타일: {scenario['style']}")
        
        try:
            start_time = time.time()
            
            # 1. 스크립트 생성
            logger.info("")
            logger.info("1️⃣  스크립트 생성 중...")
            
            # 수동 스크립트 사용 (OpenAI 없이도 테스트 가능)
            manual_scripts = {
                20: "비트코인이 오늘 10% 급등했습니다. 현재 가격은 5천850만원입니다. 투자자들의 관심이 집중되고 있습니다.",
                60: "코스피가 오늘 3000선을 돌파했습니다. 전문가들은 외국인 매수세가 강하다고 분석합니다. 삼성전자와 SK하이닉스가 상승을 주도했습니다. 하지만 일부 전문가들은 과열을 경고하고 있습니다. 투자에 신중을 기해야 합니다.",
                300: "최근 환율 변동이 경제에 미치는 영향을 분석해봅니다. 달러 대비 원화 가치가 급등락하면서 수출입 기업들의 고민이 깊어지고 있습니다. 환율 상승은 수출 기업에 유리하지만, 수입 원자재 가격 상승으로 제조업체들의 부담이 커지고 있습니다. 전문가들은 환율 변동성 확대에 대비한 헤지 전략이 필요하다고 조언합니다. 특히 중소기업들은 환위험 관리에 더욱 신경 써야 할 시점입니다." * 3  # 약 5분 분량
            }
            
            script_text = manual_scripts.get(scenario['duration'], manual_scripts[60])
            logger.info(f"✅ 스크립트 준비 완료 ({len(script_text)}자)")
            
            # 2. TTS 생성
            logger.info("")
            logger.info("2️⃣  TTS 생성 중...")
            
            timestamp = int(time.time() * 1000)
            audio_path = f"data/audio/test_banana_{i}_{timestamp}.mp3"
            Path(audio_path).parent.mkdir(parents=True, exist_ok=True)
            
            tts_generator.generate_audio(script_text, audio_path)
            audio_size = os.path.getsize(audio_path) / 1024
            logger.info(f"✅ TTS 완료: {audio_size:.1f} KB")
            
            # 3. Banana 비디오 생성
            logger.info("")
            logger.info("3️⃣  🍌 Banana 비디오 생성 중...")
            
            output_path = f"data/videos/test_banana_{i}_{timestamp}.mp4"
            
            success = video_creator.create_banana_video(
                topic=scenario['topic'],
                script_text=script_text,
                audio_path=audio_path,
                output_path=output_path,
                target_duration=scenario['duration'],
                style=scenario['style']
            )
            
            elapsed_time = time.time() - start_time
            
            if success and os.path.exists(output_path):
                video_size = os.path.getsize(output_path) / (1024 * 1024)
                
                result = {
                    'scenario': scenario['name'],
                    'success': True,
                    'output': output_path,
                    'size_mb': video_size,
                    'duration_sec': scenario['duration'],
                    'elapsed_sec': elapsed_time
                }
                
                logger.info(f"✅ 비디오 생성 완료!")
                logger.info(f"   📹 파일: {output_path}")
                logger.info(f"   💾 크기: {video_size:.1f} MB")
                logger.info(f"   ⏱️  소요 시간: {elapsed_time:.1f}초")
            else:
                result = {
                    'scenario': scenario['name'],
                    'success': False,
                    'error': 'Video file not created'
                }
                logger.error(f"❌ 비디오 생성 실패")
            
            results.append(result)
            
        except Exception as e:
            logger.error(f"❌ 테스트 실패: {e}")
            import traceback
            logger.error(traceback.format_exc())
            
            results.append({
                'scenario': scenario['name'],
                'success': False,
                'error': str(e)
            })
    
    # 결과 요약
    logger.info("")
    logger.info("=" * 80)
    logger.info("🍌 Banana 모드 테스트 결과 요약")
    logger.info("=" * 80)
    
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)
    
    logger.info(f"✅ 성공: {success_count}/{total_count}")
    logger.info(f"❌ 실패: {total_count - success_count}/{total_count}")
    
    logger.info("")
    logger.info("📊 상세 결과:")
    for i, result in enumerate(results, 1):
        logger.info(f"  {i}. {result['scenario']}: {'✅ 성공' if result['success'] else '❌ 실패'}")
        if result['success']:
            logger.info(f"     - 크기: {result['size_mb']:.1f} MB")
            logger.info(f"     - 길이: {result['duration_sec']}초")
            logger.info(f"     - 소요: {result['elapsed_sec']:.1f}초")
        else:
            logger.info(f"     - 오류: {result.get('error', 'Unknown')}")
    
    logger.info("=" * 80)
    
    # 생성된 파일 확인
    logger.info("")
    logger.info("📁 생성된 파일:")
    os.system("ls -lh data/videos/test_banana_* 2>/dev/null || echo '   (파일 없음)'")
    
    return success_count == total_count


if __name__ == '__main__':
    success = test_banana_mode()
    sys.exit(0 if success else 1)
