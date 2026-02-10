"""
6가지 목소리 샘플 생성 스크립트
"""
from gtts import gTTS
from pathlib import Path
import os

# 샘플 텍스트
SAMPLE_TEXTS = {
    'male_young': '안녕하세요! 저는 젊고 에너지 넘치는 남성 목소리입니다. 경제 뉴스를 전해드립니다.',
    'male_mature': '안녕하십니까. 저는 차분하고 신뢰감 있는 성숙한 남성 목소리입니다. 오늘의 시장 동향을 말씀드리겠습니다.',
    'female_young': '안녕하세요! 저는 친근하고 활발한 여성 목소리예요. 함께 경제 소식 알아볼까요?',
    'female_professional': '안녕하세요. 저는 정확하고 명료한 전문가 목소리입니다. 오늘의 주요 뉴스를 전달하겠습니다.',
    'news_anchor': '시청자 여러분, 안녕하십니까. 뉴스 앵커 스타일의 목소리로 경제 소식을 전해드립니다.',
    'youtube_creator': '여러분 안녕하세요! 유튜버 스타일의 생동감 있는 목소리로 재미있게 전해드릴게요!'
}

# 오디오 디렉토리
AUDIO_DIR = Path('data/audio')
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("🎤 목소리 샘플 생성 시작")
print("=" * 70)

for voice_key, text in SAMPLE_TEXTS.items():
    try:
        filename = f"sample_{voice_key}.mp3"
        file_path = AUDIO_DIR / filename
        
        print(f"\n생성 중: {voice_key}...")
        print(f"텍스트: {text[:50]}...")
        
        # gTTS로 생성 (기본 한국어 목소리)
        # 실제로는 Google Cloud TTS를 사용하면 더 다양한 목소리 가능
        tts = gTTS(text=text, lang='ko', slow=False)
        tts.save(str(file_path))
        
        file_size = file_path.stat().st_size / 1024  # KB
        print(f"✅ 완료: {filename} ({file_size:.1f} KB)")
        
    except Exception as e:
        print(f"❌ 오류: {voice_key} - {e}")

print("\n" + "=" * 70)
print("🎉 모든 샘플 생성 완료!")
print(f"📁 위치: {AUDIO_DIR.absolute()}")
print("=" * 70)

# 생성된 파일 목록
print("\n📋 생성된 파일:")
for file in sorted(AUDIO_DIR.glob("sample_*.mp3")):
    size = file.stat().st_size / 1024
    print(f"   • {file.name} ({size:.1f} KB)")
