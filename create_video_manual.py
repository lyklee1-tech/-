#!/usr/bin/env python3
"""
수동 스크립트로 비디오 생성
OpenAI API 없이 직접 스크립트를 작성해서 비디오 생성
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 여기에 원하는 스크립트를 입력하세요!
SCRIPTS = [
    {
        "title": "비트코인 급등",
        "script": """
오늘 비트코인이 10% 급등했습니다!
현재 가격은 5천850만원입니다.
전문가들은 상승세가 계속될 것으로 전망하고 있습니다.
구독과 좋아요 부탁드립니다!
"""
    },
    {
        "title": "코스피 상승",
        "script": """
코스피가 오늘 2% 상승 마감했습니다!
외국인 매수세가 강하게 유입되고 있습니다.
주요 대형주들이 동반 상승했습니다.
구독과 좋아요 부탁드립니다!
"""
    },
    {
        "title": "환율 변동",
        "script": """
원달러 환율이 급등하고 있습니다!
현재 1달러당 1,350원을 기록했습니다.
수출 기업들의 실적 개선이 예상됩니다.
구독과 좋아요 부탁드립니다!
"""
    }
]

def main():
    """수동 스크립트로 비디오 생성"""
    
    print("="*60)
    print("📝 수동 스크립트 비디오 생성")
    print("="*60)
    print(f"\n총 {len(SCRIPTS)}개의 스크립트를 처리합니다.\n")
    
    from src.tts.tts_generator import TTSGenerator
    from src.video_generation.video_creator import VideoCreator
    import time
    
    tts = TTSGenerator()
    creator = VideoCreator()
    
    success_count = 0
    
    for i, script_data in enumerate(SCRIPTS, 1):
        title = script_data['title']
        script = script_data['script'].strip()
        
        print(f"\n{'='*60}")
        print(f"🎬 {i}/{len(SCRIPTS)}: {title}")
        print(f"{'='*60}")
        print(f"📝 스크립트:\n{script}\n")
        
        try:
            # 1. TTS 생성
            print("🔊 TTS 음성 생성 중...")
            audio_path = f"data/audio/narration_{i}_{int(time.time())}.mp3"
            success = tts.generate_audio(
                text=script,
                output_path=audio_path
            )
            
            if not success or not os.path.exists(audio_path):
                print(f"   ❌ TTS 생성 실패")
                continue
            
            file_size = os.path.getsize(audio_path) / 1024
            print(f"   ✅ TTS 생성 완료: {file_size:.1f} KB")
            
            # 2. 비디오 생성
            print("🎥 비디오 생성 중...")
            output_path = f"data/videos/shorts_{i}_{int(time.time())}.mp4"
            
            success = creator.create_shorts_video(
                audio_path=audio_path,
                script_text=script,
                output_path=output_path,
                title_text=title
            )
            
            if success and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                print(f"   ✅ 비디오 생성 완료: {file_size:.1f} MB")
                success_count += 1
            else:
                print(f"   ❌ 비디오 생성 실패")
        
        except Exception as e:
            print(f"   ❌ 오류 발생: {e}")
            continue
    
    # 최종 결과
    print("\n" + "="*60)
    print("🎉 처리 완료!")
    print("="*60)
    print(f"\n성공: {success_count}/{len(SCRIPTS)}")
    print(f"\n📁 생성된 파일 확인:")
    print(f"   ls -lh data/videos/")
    print()

if __name__ == "__main__":
    main()
