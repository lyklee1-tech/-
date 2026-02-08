# 💻 **내 컴퓨터에서 실행하기 - 완전 가이드**

---

## 🎯 **GitHub에서 다운로드 (가장 쉬움!)**

### **📦 저장소 정보**
```
🔗 GitHub: https://github.com/lyklee1-tech/-
🌿 Branch: main
✅ 최신 버전: aaa06f0
```

---

## 🚀 **방법 1: Git으로 다운로드 (추천!)**

### **Windows**

```bash
# 1. Git 설치 확인 (없으면 https://git-scm.com/download/win 에서 다운로드)
git --version

# 2. 원하는 폴더로 이동 (예: 바탕화면)
cd Desktop

# 3. 저장소 다운로드
git clone https://github.com/lyklee1-tech/-.git economic-shorts

# 4. 폴더로 이동
cd economic-shorts

# 5. 파일 확인
dir
```

### **Mac/Linux**

```bash
# 1. Git 설치 확인
git --version

# 2. 원하는 폴더로 이동
cd ~/Desktop

# 3. 저장소 다운로드
git clone https://github.com/lyklee1-tech/-.git economic-shorts

# 4. 폴더로 이동
cd economic-shorts

# 5. 파일 확인
ls -la
```

---

## 📦 **방법 2: ZIP 파일 다운로드**

### **1단계: GitHub에서 다운로드**

1. 웹브라우저에서 접속:
   ```
   https://github.com/lyklee1-tech/-
   ```

2. 초록색 **"Code"** 버튼 클릭

3. **"Download ZIP"** 클릭

4. 다운로드한 ZIP 파일 압축 해제

5. 압축 해제된 폴더로 이동

---

## 🔧 **Python 설치 및 설정**

### **1단계: Python 설치**

#### **Windows**
```bash
# Python 다운로드
# https://www.python.org/downloads/

# 설치 시 "Add Python to PATH" 체크!

# 설치 확인
python --version
# 또는
python3 --version
```

#### **Mac**
```bash
# Homebrew로 설치
brew install python3

# 확인
python3 --version
```

#### **Linux**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# 확인
python3 --version
```

---

### **2단계: 가상환경 생성 (권장)**

#### **Windows**
```bash
# 프로젝트 폴더로 이동
cd economic-shorts

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
venv\Scripts\activate

# 활성화 확인 (프롬프트 앞에 (venv) 표시)
```

#### **Mac/Linux**
```bash
# 프로젝트 폴더로 이동
cd economic-shorts

# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 활성화 확인
```

---

### **3단계: 패키지 설치**

```bash
# 가상환경이 활성화된 상태에서

# requirements.txt 확인
cat requirements.txt

# 패키지 설치
pip install -r requirements.txt

# 또는 수동 설치
pip install gtts moviepy pillow pyyaml loguru python-dotenv requests numpy
```

---

## ⚙️ **환경 설정**

### **1단계: .env 파일 생성**

```bash
# .env.example을 복사
cp .env.example .env

# Windows에서는
copy .env.example .env
```

### **2단계: .env 파일 편집**

```bash
# 텍스트 에디터로 .env 파일 열기
notepad .env    # Windows
nano .env       # Mac/Linux
```

**내용:**
```env
# OpenAI API 키 (선택 - Banana 모드용)
OPENAI_API_KEY=sk-proj-your-key-here

# YouTube API (선택 - 업로드용)
YOUTUBE_CLIENT_ID=your-client-id
YOUTUBE_CLIENT_SECRET=your-client-secret
```

**💡 중요:** OpenAI 키가 없어도 GenSpark AI로 무료 사용 가능!

---

## 🎬 **프로그램 실행!**

### **테스트 실행**

```bash
# 1. 폴더로 이동
cd economic-shorts

# 2. 가상환경 활성화 (아직 안 했다면)
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 3. GenSpark AI로 첫 비디오 생성!
python genspark_autopilot.py --topic "비트코인 급등" --duration 20

# 4. 결과 확인
# Windows
dir data\audio\genspark_*.mp3
dir data\scenes\genspark_scenes_*.json

# Mac/Linux
ls -lh data/audio/genspark_*.mp3
ls -lh data/scenes/genspark_scenes_*.json
```

---

## ✅ **성공 확인**

실행 후 이런 메시지가 나오면 성공!

```
🌟 GenSpark AI AutoPilot 시작 (완전 무료!)
================================================================================
📌 토픽: 비트코인 급등
⏱️  목표 길이: 20초
💰 비용: $0 (GenSpark AI 무료!)
================================================================================

✅ TTS 완료: 115.9 KB
🎬 장면 수: 4개
✅ 준비 완료!
```

---

## 📁 **폴더 구조**

다운로드한 폴더 구조:

```
economic-shorts/
├── README.md               # 프로젝트 소개
├── START_HERE.md          # ⭐ 시작 가이드
├── GENSPARK_AI_FREE.md    # 🌟 GenSpark AI 가이드
├── BANANA_MODE.md         # 🍌 Banana 모드 가이드
│
├── genspark_autopilot.py  # 🌟 GenSpark AI 실행 스크립트
├── banana_autopilot.py    # 🍌 Banana 모드 실행
├── create_video_auto.py   # 🎬 자동 비디오 생성
│
├── requirements.txt       # 필요한 패키지 목록
├── .env.example          # 환경변수 예시
├── .env                  # 환경변수 (직접 생성)
│
├── config/
│   └── config.yaml       # 설정 파일
│
├── src/                  # 소스 코드
│   ├── tts/             # TTS 생성
│   ├── video_generation/ # 비디오 생성
│   └── ...
│
└── data/                 # 생성된 파일
    ├── audio/           # TTS 음성
    ├── scenes/          # 장면 정보
    ├── videos/          # 완성 비디오
    └── ...
```

---

## 🐛 **문제 해결**

### **문제 1: Python을 찾을 수 없음**

```bash
# Windows
# PATH에 Python 추가 또는
python3 genspark_autopilot.py --topic "test" --duration 20

# Mac/Linux
python3 genspark_autopilot.py --topic "test" --duration 20
```

### **문제 2: 패키지 설치 오류**

```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 다시 설치
pip install -r requirements.txt
```

### **문제 3: 권한 오류 (Mac/Linux)**

```bash
# 실행 권한 부여
chmod +x *.py

# 다시 실행
python3 genspark_autopilot.py --topic "test" --duration 20
```

### **문제 4: 가상환경 활성화 안 됨**

```bash
# Windows (PowerShell에서 실행 정책 오류 시)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 다시 활성화
venv\Scripts\activate
```

---

## 💡 **자주 묻는 질문**

### **Q1: OpenAI API 키가 필요한가요?**
**A:** 아니요! GenSpark AI는 완전 무료입니다. OpenAI는 선택사항입니다.

### **Q2: 오프라인에서도 작동하나요?**
**A:** TTS 생성은 온라인이 필요하지만, 대부분 기능은 오프라인 가능합니다.

### **Q3: 다른 언어로도 사용할 수 있나요?**
**A:** 네! 스크립트만 바꾸면 됩니다. gTTS는 여러 언어를 지원합니다.

### **Q4: 상업적으로 사용해도 되나요?**
**A:** 네! GenSpark AI 이용약관을 확인하세요.

---

## 🎯 **빠른 시작 체크리스트**

- [ ] 1. Git 또는 ZIP으로 프로젝트 다운로드
- [ ] 2. Python 설치 (3.8 이상)
- [ ] 3. 프로젝트 폴더로 이동
- [ ] 4. 가상환경 생성 및 활성화
- [ ] 5. pip install -r requirements.txt
- [ ] 6. .env 파일 생성 (선택)
- [ ] 7. python genspark_autopilot.py --topic "테스트" --duration 20
- [ ] 8. 성공! 🎉

---

## 📚 **다음 단계**

### **1. 문서 읽기**
```bash
# 시작 가이드
cat START_HERE.md

# GenSpark AI 가이드
cat GENSPARK_AI_FREE.md

# Banana 모드 가이드
cat BANANA_MODE.md
```

### **2. 첫 비디오 만들기**
```bash
python genspark_autopilot.py --topic "당신의 주제" --duration 20
```

### **3. 고급 기능 탐색**
- 다양한 길이 (20초 ~ 30분)
- 여러 주제 대량 생성
- GenSpark AI 웹 통합

---

## 🎉 **축하합니다!**

이제 **내 컴퓨터에서** 프로그램을 실행할 수 있습니다! 🎊

**다음 명령어로 바로 시작하세요:**

```bash
cd economic-shorts
python genspark_autopilot.py --topic "테스트" --duration 20
```

**🌟 성공을 기원합니다!** 🚀
