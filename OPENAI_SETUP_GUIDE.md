# OpenAI API 키 설정 가이드

## 문제 상황
- API 키 인증 실패 (401 오류)
- 스크립트 자동 생성 불가

## 해결 방법

### 1단계: OpenAI 계정 확인

1. **로그인**
   - https://platform.openai.com/ 접속
   - 계정으로 로그인

2. **크레딧 확인**
   - https://platform.openai.com/account/billing
   - 사용 가능한 크레딧이 있는지 확인
   - **최소 $5 이상 권장**

3. **결제 수단 등록**
   - Settings → Billing
   - 신용카드 등록
   - Auto-recharge 설정 (선택)

### 2단계: 새 API 키 발급

1. **API Keys 페이지 접속**
   - https://platform.openai.com/api-keys

2. **기존 키 확인**
   - 현재 키가 'Active' 상태인지 확인
   - 삭제되었거나 만료된 경우 새로 생성

3. **새 키 생성**
   ```
   1) 'Create new secret key' 클릭
   2) 이름 입력: "YouTube Shorts Automation"
   3) 권한 설정: All (전체 권한)
   4) Create 클릭
   5) ⚠️ 키가 한 번만 표시됩니다! 즉시 복사하세요
   ```

4. **키 형식 확인**
   - 올바른 형식: `sk-proj-xxxxxx...`
   - 전체 길이: 약 200자 이상

### 3단계: 키 등록

새 키를 받으시면 여기에 붙여넣어주세요:
```
OPENAI_API_KEY=sk-proj-여기에_새_키_붙여넣기
```

## 비용 안내

### 예상 사용량
- **GPT-4 Turbo**: 1 스크립트 생성 약 $0.002-0.005
- **월 100개 생성**: 약 $0.20-0.50
- **월 1,000개 생성**: 약 $2-5

### 권장 크레딧
- **테스트용**: $5
- **월간 운영**: $10-20
- **대량 생성**: $50+

## 대안: 무료 테스트 방법

API 키 없이 시스템을 테스트하려면:

### 옵션 A: 수동 스크립트 사용
```bash
cd /home/user/webapp
python -c "
from src.tts.tts_generator import TTSGenerator
from src.video_generation.video_creator import VideoCreator

# 수동 스크립트
script = '''
비트코인이 10% 급등했습니다!
현재 가격은 5천850만원입니다.
전문가들은 상승세가 계속될 것으로 전망하고 있습니다.
구독과 좋아요 부탁드립니다!
'''

# TTS 생성
tts = TTSGenerator()
audio = tts.generate(script, 'test_audio.mp3')

# 비디오 생성
creator = VideoCreator()
video = creator.create_video(
    script=script,
    audio_path='test_audio.mp3',
    duration=20,
    preset='quick'
)
print(f'비디오 생성 완료: {video}')
"
```

### 옵션 B: 다른 AI 모델 사용
- **Google Gemini API** (무료 쿼터 제공)
- **Anthropic Claude API**
- **로컬 LLM** (Ollama, LM Studio)

## 다음 단계

1. **즉시 진행**: OpenAI 계정 확인 후 새 키 발급
2. **나중에 진행**: 문서 정리 및 시스템 구조 확인
3. **대안 테스트**: 수동 스크립트로 TTS/비디오 생성 테스트

어떤 방법으로 진행하시겠습니까?

---

**시스템 준비 상태**
- ✅ 전체 코드 구현 완료
- ✅ BGM 4개 + SFX 4개 업로드 완료
- ✅ 설정 파일 완성
- ✅ 패키지 설치 완료
- ⏳ OpenAI API 키만 필요!
