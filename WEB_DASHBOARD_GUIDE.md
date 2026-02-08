# 🎨 웹 대시보드 사용 가이드

## 🚀 빠른 시작 (3단계!)

### 1️⃣ Flask 설치
```bash
pip install flask flask-cors
```

### 2️⃣ 서버 실행
```bash
python web_dashboard.py
```

### 3️⃣ 브라우저 열기
```
http://localhost:5000
```

---

## 📺 스크린샷

웹 대시보드 화면:
- ✅ 직관적인 UI
- ✅ 스타일 템플릿 선택
- ✅ 영상 길이 프리셋
- ✅ 실시간 진행 상황
- ✅ 자동 다운로드

---

## 🎯 사용 방법

### **Step 1: 주제 입력**
```
예시:
- 비트코인 급등
- 코스피 3000선 돌파
- 삼성전자 실적 분석
- 환율 변동 분석
```

### **Step 2: 스타일 선택**
- 💼 전문적 (Professional) - 비즈니스, 기업 뉴스
- 🙂 스틱맨 애니메이션 - 간단한 설명
- 👧 일본 애니메이션 - 애니메이션 스타일
- 🎬 시네마틱 - 영화 같은 느낌
- 🎮 3D 렌더링 - 3D 그래픽
- 🌍 다큐멘터리 - 실사 영상
- 📊 성과 지표 - 차트와 그래프
- 🏢 오피스 장면 - 사무실 배경

### **Step 3: 영상 길이 선택**
- ⚡ 빠른 (20초)
- 🎯 짧게 (30초)
- 📝 표준 (1분)
- 📱 Shorts (2분)
- 🎬 중간 (5분)
- 📹 긴 영상 (10분)
- 🎥 확장 (20분)
- 🎞️ 최대 (30분)

### **Step 4: 생성 버튼 클릭!**
```
🚀 비디오 생성하기 (완전 무료!)
```

### **Step 5: 결과 확인 + 다운로드**
- 🎵 TTS 음성 파일 (MP3)
- 📋 장면 데이터 (JSON)
- 자동으로 `data/` 폴더에 저장!

---

## 📁 생성된 파일 위치

```
data/
├── audio/
│   └── genspark_*.mp3          # TTS 음성 파일
├── scenes/
│   └── genspark_scenes_*.json  # 장면 데이터
└── videos/
    └── *.mp4                   # 완성된 비디오 (향후)
```

---

## 🎨 웹 UI 기능

### ✅ 실시간 피드백
- 로딩 스피너
- 진행 상황 알림
- 성공/실패 메시지

### ✅ 통계 대시보드
- 장면 수
- 총 길이
- 비용 ($0!)
- 파일 크기

### ✅ 장면 미리보기
- 장면별 텍스트
- AI 이미지 프롬프트
- 길이 정보

### ✅ 원클릭 다운로드
- TTS 음성 파일
- 장면 데이터 JSON
- 브라우저 자동 다운로드

---

## 🔧 API 엔드포인트

### **POST /api/generate**
비디오 생성
```json
{
  "topic": "비트코인 급등",
  "duration": 20,
  "style": "professional",
  "script": "optional"
}
```

### **GET /api/status**
시스템 상태 확인

### **GET /api/history**
생성 히스토리 조회

### **GET /api/download/audio/<filename>**
오디오 파일 다운로드

### **GET /api/download/scenes/<filename>**
장면 데이터 다운로드

---

## 🆘 문제 해결

### **문제 1: Flask를 찾을 수 없음**
```bash
pip install flask flask-cors
```

### **문제 2: 포트 5000이 사용 중**
`web_dashboard.py` 파일 마지막 줄 수정:
```python
app.run(host='0.0.0.0', port=8080, debug=True)  # 5000 → 8080
```

### **문제 3: 브라우저에서 접속 안 됨**
- 방화벽 확인
- 서버가 실행 중인지 확인
- `http://127.0.0.1:5000` 시도

---

## 💡 팁 & 트릭

### **빠른 테스트**
```bash
# 터미널 1: 서버 실행
python web_dashboard.py

# 브라우저: http://localhost:5000
```

### **동시에 여러 비디오 생성**
웹 UI에서 여러 탭 열어서 동시 생성 가능!

### **커스텀 스크립트**
API를 직접 호출하면 커스텀 스크립트 사용 가능:
```python
import requests

response = requests.post('http://localhost:5000/api/generate', json={
    'topic': '비트코인 급등',
    'duration': 20,
    'style': 'professional',
    'script': '여기에 커스텀 스크립트 입력...'
})

print(response.json())
```

---

## 🎉 축하합니다!

**웹 대시보드를 사용하면:**
- ✅ 코드 없이 비디오 생성
- ✅ 클릭 몇 번으로 완성
- ✅ 자동 다운로드
- ✅ 시각적 피드백
- ✅ 완전 무료!

---

## 📞 지원

문제가 발생하면:
1. `python web_dashboard.py` 터미널 로그 확인
2. 브라우저 개발자 도구 (F12) 콘솔 확인
3. `data/` 폴더에 파일이 생성되는지 확인

---

**시작하세요!** 🚀

```bash
python web_dashboard.py
```

그리고 `http://localhost:5000`를 브라우저에서 열어보세요!
