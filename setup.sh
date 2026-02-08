#!/bin/bash

# 경제 유튜브 Shorts 자동화 시스템 - 설치 및 설정 스크립트

echo "========================================"
echo "경제 유튜브 Shorts 자동화 시스템"
echo "설치 스크립트"
echo "========================================"
echo ""

# 1. Python 버전 확인
echo "1. Python 버전 확인..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3가 설치되어 있지 않습니다."
    echo "   Python 3.9 이상을 설치해주세요."
    exit 1
fi

echo "✅ Python 확인 완료"
echo ""

# 2. 가상환경 생성
echo "2. 가상환경 생성..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 가상환경 생성 완료"
else
    echo "✅ 가상환경이 이미 존재합니다"
fi
echo ""

# 3. 가상환경 활성화
echo "3. 가상환경 활성화..."
source venv/bin/activate
echo "✅ 가상환경 활성화 완료"
echo ""

# 4. pip 업그레이드
echo "4. pip 업그레이드..."
pip install --upgrade pip
echo ""

# 5. 필수 패키지 설치
echo "5. Python 패키지 설치..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ 패키지 설치 실패"
    exit 1
fi

echo "✅ 패키지 설치 완료"
echo ""

# 6. FFmpeg 확인
echo "6. FFmpeg 확인..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg 설치 확인"
    ffmpeg -version | head -n 1
else
    echo "⚠️  FFmpeg가 설치되어 있지 않습니다"
    echo "   비디오 생성을 위해 FFmpeg 설치가 필요합니다"
    echo ""
    echo "   설치 방법:"
    echo "   - Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "   - macOS: brew install ffmpeg"
    echo "   - Windows: https://ffmpeg.org/download.html"
fi
echo ""

# 7. 디렉토리 구조 확인
echo "7. 디렉토리 구조 확인..."
mkdir -p data/{raw,processed,scripts,audio,videos}
mkdir -p logs
mkdir -p config

echo "✅ 디렉토리 구조 생성 완료"
echo ""

# 8. .env 파일 생성
echo "8. 환경변수 설정..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ .env 파일 생성 완료"
    echo "   .env 파일을 열어 API 키를 설정해주세요"
else
    echo "✅ .env 파일이 이미 존재합니다"
fi
echo ""

# 9. .gitkeep 파일 생성
echo "9. Git 설정..."
touch data/raw/.gitkeep
touch data/processed/.gitkeep
touch data/scripts/.gitkeep
touch data/audio/.gitkeep
touch data/videos/.gitkeep
touch logs/.gitkeep

echo "✅ Git 설정 완료"
echo ""

# 10. 설치 완료
echo "========================================"
echo "✅ 설치 완료!"
echo "========================================"
echo ""
echo "다음 단계:"
echo ""
echo "1. API 키 설정"
echo "   vi .env  # 또는 원하는 에디터로"
echo "   - OPENAI_API_KEY: GPT-4 스크립트 생성용"
echo "   - YOUTUBE_API_KEY: 유튜브 업로드용"
echo "   - NEWS_API_KEY: 뉴스 수집용 (선택)"
echo ""
echo "2. 유튜브 OAuth 설정"
echo "   - Google Cloud Console에서 OAuth 2.0 클라이언트 ID 생성"
echo "   - client_secrets.json을 config/ 폴더에 저장"
echo ""
echo "3. 테스트 실행"
echo "   python main.py --mode single"
echo ""
echo "4. 자동화 실행"
echo "   python main.py --mode auto --interval 2  # 2시간마다"
echo ""
echo "5. 스케줄러 실행"
echo "   python src/scheduler.py"
echo ""
echo "========================================"
echo ""
echo "문서: README.md를 참고하세요"
echo "이슈: https://github.com/your-repo/issues"
echo ""
