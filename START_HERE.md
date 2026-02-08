# 🚀 **프로그램 실행 가이드 - 5분 안에 시작하기!**

---

## 🎯 **가장 빠른 방법 (3단계)**

### **1단계: 프로그램 실행** (1분)

```bash
cd /home/user/webapp
python genspark_autopilot.py --topic "비트코인 급등" --duration 20
```

**출력:**
```
✅ TTS 완료: data/audio/genspark_*.mp3
✅ 장면 4개 준비 완료
✅ 프롬프트 자동 생성
```

---

### **2단계: 생성된 파일 확인** (30초)

```bash
# TTS 음성 확인
ls -lh data/audio/genspark_*.mp3

# 장면 정보 확인
cat data/scenes/genspark_scenes_*.json
```

---

### **3단계: 결과 사용** (선택)

**옵션 A: 수동으로 GenSpark AI 사용**
1. 장면 정보 JSON에서 프롬프트 복사
2. GenSpark 웹에서 이미지 생성
3. 이미지 → 비디오 변환

**옵션 B: 기존 영상 확인**
```bash
# 이미 생성된 테스트 비디오 확인
ls -lh data/videos/test_banana_*.mp4
ls -lh data/videos/quick_test_*.mp4
```

---

## 📋 **전체 명령어 모음**

### **1️⃣ GenSpark AI (무료!) - 추천**

```bash
# 20초 빠른 뉴스
python genspark_autopilot.py --topic "비트코인 급등" --duration 20

# 1분 표준 뉴스
python genspark_autopilot.py --topic "코스피 3000선" --duration 60

# 5분 분석 영상
python genspark_autopilot.py --topic "경제 전망" --duration 300
```

### **2️⃣ Banana 모드 (OpenAI 필요)**

```bash
# OpenAI API 키가 설정된 경우에만 작동
python banana_autopilot.py --topic "비트코인 분석" --preset quick
```

### **3️⃣ 테스트 스크립트**

```bash
# 빠른 테스트 (20초)
python test_banana_quick.py

# 통합 테스트 (20초, 1분, 5분)
python test_banana_mode.py
```

---

## 🎨 **다양한 주제로 실행해보기**

### **경제 뉴스**

```bash
python genspark_autopilot.py --topic "비트코인이 5000만원 돌파" --duration 20
python genspark_autopilot.py --topic "코스피가 급등했습니다" --duration 20
python genspark_autopilot.py --topic "환율이 크게 변동" --duration 20
```

### **투자 정보**

```bash
python genspark_autopilot.py --topic "삼성전자 주가 분석" --duration 60
python genspark_autopilot.py --topic "부동산 시장 전망" --duration 60
```

### **시장 분석**

```bash
python genspark_autopilot.py --topic "2024년 경제 전망" --duration 300
python genspark_autopilot.py --topic "금리 인상의 영향" --duration 300
```

---

## 📁 **생성된 파일 확인**

### **파일 위치**

```bash
# TTS 음성 파일
data/audio/genspark_*.mp3
data/audio/auto_*.mp3

# 장면 정보
data/scenes/genspark_scenes_*.json

# 생성된 비디오 (테스트)
data/videos/test_banana_*.mp4
data/videos/quick_test_*.mp4
```

### **파일 확인 명령어**

```bash
# 모든 생성 파일 확인
ls -lh data/audio/ data/scenes/ data/videos/

# 최근 생성 파일만
ls -lt data/audio/genspark_*.mp3 | head -3
ls -lt data/scenes/*.json | head -3
```

---

## 🎬 **실전 워크플로우**

### **완전 자동화 (권장)**

```bash
# 1. 토픽 준비
TOPIC="비트코인이 급등했습니다"

# 2. GenSpark AutoPilot 실행
python genspark_autopilot.py --topic "$TOPIC" --duration 20

# 3. 결과 확인
ls -lh data/audio/genspark_*.mp3 | tail -1
cat data/scenes/genspark_scenes_*.json | tail -1

# 4. (선택) GenSpark AI로 이미지/비디오 생성
# - 웹 인터페이스 사용
# - 또는 Python API 사용
```

### **대량 생성**

```bash
# 여러 주제 자동 생성
for topic in "비트코인 급등" "코스피 3000" "환율 변동"; do
  python genspark_autopilot.py --topic "$topic" --duration 20
  sleep 2
done

# 결과 확인
ls -lh data/audio/ | tail -5
```

---

## 💡 **팁 & 트릭**

### **1. 길이 조절**

```bash
# 빠른 뉴스 (20초)
--duration 20

# 표준 길이 (60초)
--duration 60

# 긴 분석 (5분 = 300초)
--duration 300
```

### **2. 프롬프트 커스터마이징**

장면 JSON 파일을 수동으로 편집:

```bash
# 1. JSON 파일 찾기
ls data/scenes/genspark_scenes_*.json | tail -1

# 2. 편집
nano data/scenes/genspark_scenes_1770579431540.json

# 3. 프롬프트 수정
# "prompt": "당신만의 프롬프트..."
```

### **3. 스크립트 변경**

`genspark_autopilot.py` 편집:

```python
# 샘플 스크립트 섹션 수정
sample_scripts = {
    20: "당신의 스크립트...",
    60: "더 긴 스크립트...",
}
```

---

## 🐛 **문제 해결**

### **문제: TTS 생성 실패**

```bash
# 해결: gTTS 재설치
pip install --upgrade gtts
```

### **문제: 디렉토리 없음**

```bash
# 해결: 디렉토리 생성
mkdir -p data/audio data/scenes data/videos
```

### **문제: 권한 오류**

```bash
# 해결: 실행 권한 부여
chmod +x *.py
```

---

## 📊 **현재 작동하는 기능**

| 기능 | 상태 | 설명 |
|------|------|------|
| ✅ TTS 생성 | 완료 | gTTS 무료 사용 |
| ✅ 장면 분할 | 완료 | 자동 분할 |
| ✅ 프롬프트 생성 | 완료 | 키워드 기반 |
| ✅ JSON 저장 | 완료 | 장면 정보 |
| ⚠️ AI 이미지 | 준비 | GenSpark 수동 |
| ⚠️ AI 비디오 | 준비 | GenSpark 수동 |
| ⚠️ 합성 | 준비 | MoviePy 대기 |

---

## 🎯 **다음 단계**

### **레벨 1: 기본 사용** ✅ (지금 가능)
```bash
python genspark_autopilot.py --topic "테스트" --duration 20
```

### **레벨 2: GenSpark AI 사용** (수동)
1. 장면 JSON 확인
2. GenSpark 웹에서 이미지 생성
3. 이미지 → 비디오 변환

### **레벨 3: 완전 자동화** (개발 필요)
- GenSpark AI API 직접 호출
- 이미지 + 비디오 자동 생성
- MoviePy 자동 합성

---

## 📞 **도움말**

### **명령어 도움말**

```bash
# 전체 옵션 확인
python genspark_autopilot.py --help

# 예제 확인
cat GENSPARK_AI_FREE.md
cat BANANA_MODE.md
```

### **로그 확인**

```bash
# 최근 실행 로그
tail -f logs/app.log

# 오류 로그만
grep ERROR logs/app.log
```

---

## 🎉 **지금 바로 시작하세요!**

**가장 간단한 방법:**

```bash
# 1. 프로그램 실행
cd /home/user/webapp
python genspark_autopilot.py --topic "테스트" --duration 20

# 2. 결과 확인
ls -lh data/audio/genspark_*.mp3 | tail -1

# 3. 성공! 🎉
```

**더 많은 예제:**

```bash
# 비트코인 뉴스
python genspark_autopilot.py --topic "비트코인 급등" --duration 20

# 주식 뉴스
python genspark_autopilot.py --topic "코스피 상승" --duration 20

# 경제 분석
python genspark_autopilot.py --topic "경제 전망" --duration 60
```

---

**🌟 GenSpark AI로 완전 무료 비디오 제작을 시작하세요!** 🎬✨

**💰 비용: $0 | ⏱️ 시간: 5분 | 🎯 난이도: 쉬움**
