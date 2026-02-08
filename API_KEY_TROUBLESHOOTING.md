# OpenAI API 키 문제 해결

## 🚨 현재 상황
- 제공하신 API 키가 401 오류 발생
- "Invalid or expired token" 메시지

## ✅ 체크리스트

### 1. API 키 확인사항

#### 키 형식 확인
```
정상 키 형식: sk-proj-xxxxxxxxxx...
키 길이: 약 150-200자
```

#### 복사 확인
- ⚠️ **키를 복사할 때 공백이나 줄바꿈이 포함되지 않았는지 확인**
- ⚠️ **전체 키가 모두 복사되었는지 확인**

### 2. OpenAI 계정 확인

#### A. 크레딧 잔액 확인
1. https://platform.openai.com/account/billing 접속
2. Credit balance 확인
3. **최소 $5 이상 필요**

#### B. 결제 수단 등록
1. Settings → Billing
2. Payment method 추가
3. Auto-recharge 설정 (권장)

#### C. API 키 상태 확인
1. https://platform.openai.com/api-keys 접속
2. 키 목록에서 상태 확인:
   - ✅ **Active** (정상)
   - ❌ **Revoked** (삭제됨)
   - ❌ **Expired** (만료됨)

### 3. 새 키 발급 방법

```
1) https://platform.openai.com/api-keys 접속
2) "Create new secret key" 클릭
3) 이름: "YouTube Shorts Bot"
4) Permissions: All (전체 권한)
5) Create 버튼 클릭
6) ⚠️ 키가 화면에 한 번만 표시됩니다!
7) 전체 키를 복사 (Ctrl+A → Ctrl+C)
8) 안전한 곳에 저장
```

### 4. 키 등록 방법

새 키를 발급받으면 이렇게 전달해주세요:

```
OPENAI_API_KEY=sk-proj-여기에_전체_키_붙여넣기
```

**주의사항:**
- 키 앞뒤에 공백 없이
- 한 줄로 전체 키 복사
- 따옴표 없이 키만 전달

## 💡 대안 방법

### 옵션 1: 무료 테스트용 스크립트 사용

OpenAI API 없이 시스템을 테스트할 수 있습니다:

```bash
cd /home/user/webapp

# 수동 스크립트로 테스트
python -c "
from src.tts.tts_generator import TTSGenerator
from src.video_generation.video_creator import VideoCreator

# 테스트 스크립트
script = '''
비트코인이 10% 급등했습니다!
현재 가격은 5천850만원입니다.
전문가들은 상승세가 계속될 것으로 전망하고 있습니다.
구독과 좋아요 부탁드립니다!
'''

print('TTS 생성 중...')
tts = TTSGenerator()
audio_path = tts.generate_speech(script, 'test_audio.mp3')

print('비디오 생성 중...')
creator = VideoCreator()
video_path = creator.create_video(
    script_text=script,
    audio_path=audio_path,
    duration=20,
    preset='quick'
)

print(f'✅ 비디오 생성 완료: {video_path}')
"
```

### 옵션 2: 구글 Gemini API 사용 (무료)

Google AI Studio에서 무료 API 키를 발급받을 수 있습니다:
- https://makersuite.google.com/app/apikey
- 월 60 요청까지 무료

### 옵션 3: 로컬 LLM 사용

Ollama나 LM Studio로 로컬에서 실행 가능:
- https://ollama.ai/
- https://lmstudio.ai/

## 📊 비용 참고

### OpenAI GPT-4 가격
- Input: $0.03 / 1K tokens
- Output: $0.06 / 1K tokens
- 1개 스크립트: 약 $0.002-0.005
- 100개 스크립트: 약 $0.20-0.50

### 권장 충전 금액
- **테스트용**: $5
- **월간 운영**: $10-20
- **대량 생성**: $50+

## 🎯 다음 단계

1. **OpenAI 계정 로그인**
   - https://platform.openai.com/

2. **크레딧 확인**
   - Billing 페이지에서 잔액 확인

3. **새 키 발급**
   - API Keys 페이지에서 생성

4. **키 전달**
   - 전체 키를 복사해서 여기에 붙여넣기

5. **테스트 실행**
   ```bash
   python main.py --mode single --preset quick
   ```

---

**시스템 준비 완료!**
- ✅ 코드 구현 완료
- ✅ 음악 파일 업로드 완료
- ✅ 설정 완료
- ⏳ API 키만 필요합니다!

궁금한 점이 있으면 알려주세요! 😊
