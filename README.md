# 🎬 경제 유튜브 Shorts 자동화 시스템

경제 뉴스와 데이터를 기반으로 유튜브 Shorts 비디오를 자동 생성하고 업로드하는 완전 자동화 시스템입니다.

## 🚀 주요 기능

### 1. 📊 데이터 수집
- **경제 뉴스**: 주요 경제 뉴스 사이트에서 자동 수집
- **주식 데이터**: 실시간 주가, 거래량, 시가총액
- **환율 정보**: 주요 통화 환율 정보
- **암호화폐**: 비트코인, 이더리움 등 주요 코인 시세

### 2. 🤖 AI 스크립트 생성
- GPT-4 기반 자동 스크립트 작성
- 경제사냥꾼 스타일 톤 앤 매너
- 30-60초 최적화된 콘텐츠
- 후킹 멘트 자동 생성

### 3. 🎙️ 음성 나레이션 (TTS)
- 고품질 한국어 TTS
- 자연스러운 억양과 강조
- 다양한 목소리 선택 가능

### 4. 🎥 비디오 생성
- 자막 자동 생성 (타이밍 동기화)
- 배경 영상/이미지
- 차트 및 그래프 시각화
- 트렌디한 효과 적용
- **투자 책임 문구 자동 삽입** (하단 고정 표시)
- **배경음악 및 효과음** (로컬 파일 우선 사용, AI 자동 생성 지원)
- **사용자 음악 파일 업로드** 지원 (`data/audio/bgm/`, `data/audio/sfx/`)

### 5. 📤 유튜브 자동 업로드
- YouTube Data API v3 연동
- 제목, 설명, 태그 자동 생성
- 썸네일 자동 생성
- 예약 게시 기능

### 6. ⏰ 자동화 스케줄러
- 시간별/일별 자동 실행
- 에러 핸들링 및 재시도
- 로깅 및 모니터링

## 📁 프로젝트 구조

```
economic-youtube-automation/
├── src/
│   ├── data_collection/      # 데이터 수집 모듈
│   │   ├── news_scraper.py
│   │   ├── stock_api.py
│   │   ├── crypto_api.py
│   │   └── forex_api.py
│   ├── script_generation/     # 스크립트 생성 모듈
│   │   ├── gpt_script.py
│   │   └── templates.py
│   ├── tts/                   # 음성 생성 모듈
│   │   └── tts_generator.py
│   ├── video_generation/      # 비디오 생성 모듈
│   │   ├── video_creator.py
│   │   ├── subtitle_generator.py
│   │   └── chart_generator.py
│   ├── youtube_upload/        # 유튜브 업로드 모듈
│   │   ├── uploader.py
│   │   └── metadata_generator.py
│   └── scheduler.py           # 스케줄러
├── data/
│   ├── raw/                   # 원본 데이터
│   ├── processed/             # 처리된 데이터
│   ├── scripts/               # 생성된 스크립트
│   ├── audio/                 # 음성 파일
│   └── videos/                # 최종 비디오
├── config/
│   ├── config.yaml            # 전역 설정
│   └── api_keys.yaml          # API 키 (gitignore)
├── logs/                      # 로그 파일
├── tests/                     # 테스트 코드
├── requirements.txt           # Python 패키지
├── .env.example               # 환경변수 예제
├── .gitignore
└── main.py                    # 메인 실행 파일
```

## 🛠️ 설치 방법

### 1. 필수 요구사항
```bash
Python 3.9+
FFmpeg
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. API 키 설정
`.env` 파일을 생성하고 다음 정보를 입력:

```env
# OpenAI API (스크립트 생성)
OPENAI_API_KEY=your_openai_api_key

# YouTube Data API
YOUTUBE_API_KEY=your_youtube_api_key
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret

# 데이터 수집 API
ALPHA_VANTAGE_API_KEY=your_alphavantage_key  # 주식 데이터
NEWS_API_KEY=your_news_api_key                # 뉴스 데이터
```

### 4. 음악 파일 업로드 (선택사항)

배경음악(BGM)과 효과음(SFX)을 업로드하세요:

```bash
# 업로드 도우미 실행 (업로드 방법 안내)
python upload_audio_helper.py
```

**Windows 로컬 파일 위치:**
- `C:\Users\user\Desktop\economic_shorts\assets\audio\bgm\` → BGM 파일
- `C:\Users\user\Desktop\economic_shorts\assets\audio\sfx\` → 효과음 파일

**서버 대상 폴더:**
- `data/audio/bgm/` → 배경음악
- `data/audio/sfx/{intro,hook,key_point,chart_reveal,conclusion,cta,outro,events}/` → 효과음

📖 **자세한 가이드**: [UPLOAD_AUDIO.md](UPLOAD_AUDIO.md) 참조

## 🎯 사용 방법

### 1. 수동 실행 (단일 비디오 생성)
```bash
python main.py --mode single
```

### 2. 자동화 모드 (스케줄러)
```bash
# 매시간 자동 실행
python main.py --mode auto --interval hourly

# 매일 특정 시간 실행
python main.py --mode auto --interval daily --time "09:00,12:00,18:00"
```

### 3. 데이터 수집만 테스트
```bash
python -m src.data_collection.news_scraper
```

### 4. 스크립트 생성 테스트
```bash
python -m src.script_generation.gpt_script
```

## ⚙️ 설정 커스터마이징

`config/config.yaml` 파일에서 다양한 설정을 변경할 수 있습니다:

```yaml
video:
  duration: 60  # 비디오 길이 (초)
  resolution: "1080x1920"  # Shorts 해상도
  fps: 30

script:
  style: "경제사냥꾼"  # 스크립트 스타일
  tone: "전문적이면서 친근함"
  length: "150-200자"

tts:
  voice: "ko-KR-Neural2-C"  # TTS 목소리
  speed: 1.0
  pitch: 0

youtube:
  auto_upload: true
  visibility: "public"  # public, private, unlisted
  category: "25"  # News & Politics
```

## 📊 워크플로우

```
1. 데이터 수집 → 2. AI 분석 → 3. 스크립트 생성 → 
4. TTS 생성 → 5. 비디오 제작 → 6. 유튜브 업로드
```

## 🔧 트러블슈팅

### FFmpeg 설치
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# https://ffmpeg.org/download.html 에서 다운로드
```

### API 할당량 초과
- OpenAI API: 요청 제한 확인
- YouTube API: 일일 할당량 10,000 units

## 📝 라이센스

MIT License

## 🤝 기여하기

이슈와 PR은 언제나 환영합니다!

## 📞 문의

문제가 발생하면 Issues 탭에서 문의해주세요.
