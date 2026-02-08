#!/usr/bin/env python3
"""
OpenAI API 없이 테스트 비디오 생성
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """테스트 비디오 생성"""
    
    # 테스트 스크립트
    script = """
비트코인이 오늘 10% 급등했습니다!
현재 가격은 5천850만원으로,
전문가들은 상승세가 계속될 것으로 전망하고 있습니다.
구독과 좋아요 부탁드립니다!
"""
    
    print("="*60)
    print("🎬 테스트 비디오 생성 시작")
    print("="*60)
    print(f"\n📝 스크립트:\n{script}\n")
    
    try:
        # 1. TTS 생성
        print("🔊 1단계: TTS 음성 생성 중...")
        from src.tts.tts_generator import TTSGenerator
        
        tts = TTSGenerator()
        audio_path = "data/audio/test_narration.mp3"
        success = tts.generate_audio(
            text=script.strip(),
            output_path=audio_path
        )
        
        if not success:
            print("   ❌ TTS 생성 실패")
            return
        
        if audio_path and os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path) / 1024
            print(f"   ✅ TTS 생성 완료: {audio_path} ({file_size:.1f} KB)")
        else:
            print("   ❌ TTS 생성 실패")
            return
        
        # 2. 비디오 생성
        print("\n🎥 2단계: 비디오 생성 중...")
        from src.video_generation.video_creator import VideoCreator
        import time
        
        creator = VideoCreator()
        timestamp = int(time.time())
        output_path = f"data/videos/test_video_{timestamp}.mp4"
        
        success = creator.create_shorts_video(
            audio_path=audio_path,
            script_text=script.strip(),
            output_path=output_path
        )
        
        if success and os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024 * 1024)
            print(f"   ✅ 비디오 생성 완료: {output_path} ({file_size:.1f} MB)")
        else:
            print("   ❌ 비디오 생성 실패")
            return
        
        # 3. 결과 출력
        print("\n" + "="*60)
        print("🎉 테스트 완료!")
        print("="*60)
        print(f"\n📁 생성된 파일:")
        print(f"   음성: {audio_path}")
        print(f"   비디오: {output_path}")
        print(f"\n💡 비디오를 확인하려면:")
        print(f"   ls -lh {os.path.dirname(output_path)}/")
        print()
        
    except ImportError as e:
        print(f"\n❌ 모듈 import 실패: {e}")
        print("필요한 패키지를 설치해주세요:")
        print("   pip install gtts moviepy pillow")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
