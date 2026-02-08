# 🚀 빠른 시작 가이드

경제 유튜브 Shorts 자동화 시스템을 5분 안에 시작하는 방법입니다.

## 📋 사전 준비

### 필수 요구사항
- Python 3.9 이상
- FFmpeg
- Git

### API 키 준비
다음 API 키들을 미리 준비해주세요:

1. **OpenAI API Key** (필수)
   - https://platform.openai.com/api-keys
   - 스크립트 자동 생성에 사용

2. **YouTube Data API** (필수 - 업로드 시)
   - https://console.cloud.google.com/apis
   - YouTube Data API v3 활성화
   - OAuth 2.0 클라이언트 ID 생성

3. **News API Key** (선택)
   - https://newsapi.org/
   - 뉴스 데이터 수집에 사용

## 🛠️ 설치

### 1단계: 저장소 클론 (이미 되어있음)
```bash
# 이미 /home/user/webapp에 있습니다
cd /home/user/webapp
```

### 2단계: 자동 설치 실행
```bash
./setup.sh
```

이 스크립트는 다음을 자동으로 수행합니다:
- 가상환경 생성
- 필요한 Python 패키지 설치
- 디렉토리 구조 생성
- .env 파일 생성

### 3단계: API 키 설정
```bash
vi .env  # 또는 nano .env
```

`.env` 파일에 API 키를 입력:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
YOUTUBE_API_KEY=AIzaSyxxxxxxxxxxxxx
NEWS_API_KEY=xxxxxxxxxxxxx
```

### 4단계: 유튜브 OAuth 설정 (업로드 시 필요)

1. Google Cloud Console에서 OAuth 2.0 클라이언트 ID 생성
2. `client_secrets.json` 다운로드
3. `config/` 폴더에 저장

```bash
# client_secrets.json 파일을 config/ 폴더로 이동
mv ~/Downloads/client_secrets.json config/
```

## 🎬 첫 실행

### 테스트 실행 (데이터 수집만)
```bash
# 가상환경 활성화
source venv/bin/activate

# 뉴스 수집 테스트
python -m src.data_collection.news_scraper

# 주식 데이터 수집 테스트
python -m src.data_collection.stock_api
```

### 단일 비디오 생성 (업로드 제외)
```bash
# config/config.yaml에서 auto_upload를 false로 설정
vi config/config.yaml
# youtube.auto_upload: false

# 실행
python main.py --mode single
```

생성된 파일 확인:
- `data/audio/*.mp3` - 생성된 음성 파일
- `data/videos/*.mp4` - 생성된 비디오
- `logs/app.log` - 실행 로그

### 유튜브 업로드 포함 실행
```bash
# config/config.yaml에서 auto_upload를 true로 설정
vi config/config.yaml
# youtube.auto_upload: true

# 실행 (첫 실행 시 브라우저에서 Google 로그인 필요)
python main.py --mode single
```

## ⏰ 자동화 실행

### 2시간마다 자동 실행
```bash
python main.py --mode auto --interval 2
```

### 매일 정해진 시간에 실행
`config/config.yaml` 파일 수정:
```yaml
scheduler:
  enabled: true
  mode: "daily"
  daily:
    times:
      - "09:00"  # 오전 9시
      - "12:00"  # 낮 12시
      - "18:00"  # 오후 6시
      - "21:00"  # 오후 9시
```

실행:
```bash
python src/scheduler.py
```

### 백그라운드 실행 (서버에서)
```bash
# nohup으로 백그라운드 실행
nohup python src/scheduler.py > scheduler.out 2>&1 &

# 실행 확인
ps aux | grep scheduler

# 종료
pkill -f scheduler.py
```

## 🎨 커스터마이징

### 스크립트 스타일 변경
`config/config.yaml`:
```yaml
script:
  style: "경제사냥꾼"  # 원하는 스타일로 변경
  tone: "전문적이면서 친근하게"
  target_audience: "2030 투자자"
```

### TTS 목소리 변경
```yaml
tts:
  provider: "google"  # google, elevenlabs, gtts
  voice: "ko-KR-Neural2-C"  # 다른 목소리로 변경
  speed: 1.0  # 말하기 속도 조절
```

### 비디오 설정 변경
```yaml
video:
  duration: 60  # 초 (30-60 권장)
  resolution: "1080x1920"  # Shorts 최적
  fps: 30
```

## 📊 생성 과정 모니터링

### 실시간 로그 확인
```bash
tail -f logs/app.log
```

### 생성된 파일 확인
```bash
# 최근 생성된 비디오
ls -lt data/videos/

# 최근 생성된 스크립트
ls -lt data/scripts/

# 저장 공간 확인
du -sh data/*
```

## 🔧 문제 해결

### FFmpeg 오류
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Python 패키지 오류
```bash
# 가상환경 재생성
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### OpenAI API 할당량 초과
- API 키의 사용량 확인: https://platform.openai.com/usage
- 요금제 업그레이드 또는 다른 API 키 사용

### YouTube API 할당량 초과
- 일일 할당량: 10,000 units
- 업로드 1회 = 약 1,600 units
- 하루 최대 6개 정도 업로드 가능

## 📈 성능 최적화

### 병렬 처리 설정
`config/config.yaml`:
```yaml
performance:
  max_workers: 4  # CPU 코어 수에 맞게 조정
  cache_enabled: true
```

### 임시 파일 자동 정리
```bash
# 7일 이상 된 파일 삭제
find data/audio -mtime +7 -delete
find data/videos -mtime +7 -delete
```

## 🎯 다음 단계

1. **첫 비디오 생성**: `python main.py --mode single`
2. **결과 확인**: `data/videos/` 폴더의 MP4 파일 재생
3. **스크립트 조정**: 원하는 스타일로 `config/config.yaml` 수정
4. **자동화 설정**: 스케줄러 설정 및 실행
5. **모니터링**: 로그 확인 및 성능 최적화

## 💡 유용한 명령어 모음

```bash
# 전체 프로세스 1회 실행
python main.py --mode single

# 2시간마다 자동 실행
python main.py --mode auto --interval 2

# 스케줄러로 실행
python src/scheduler.py

# 데이터 수집만 테스트
python -m src.data_collection.news_scraper
python -m src.data_collection.stock_api

# 스크립트 생성만 테스트
python -m src.script_generation.gpt_script

# TTS 생성만 테스트
python -m src.tts.tts_generator

# 로그 실시간 확인
tail -f logs/app.log

# 디스크 사용량 확인
du -sh data/*
```

## 🆘 도움이 필요하신가요?

- 📖 상세 문서: `README.md` 참고
- 🐛 버그 리포트: GitHub Issues
- 💬 질문: GitHub Discussions

---

**축하합니다! 🎉**  
이제 경제 유튜브 Shorts를 자동으로 생성할 수 있습니다!
