# 🍌 Banana 모드 - 완전 자동화 비디오 생성 시스템

> **YouTube Shorts 자동화 시스템**을 **Banana 스타일**로 업그레이드!
> **20초 ~ 30분** 영상을 **원클릭**으로 자동 생성합니다.

---

## 🎯 **Banana 모드란?**

**Banana 모드**는 AI 기반 완전 자동화 비디오 생성 시스템입니다.

### ✨ **핵심 기능**

| 기능 | 설명 | 상태 |
|------|------|------|
| **🎨 AI 이미지 생성** | 장면별 AI 이미지 자동 생성 (DALL-E 3) | ✅ |
| **🎬 장면 자동 분할** | 스크립트 → 장면 분할 (루프 지원) | ✅ |
| **📏 가변 길이** | 20초 ~ 30분 (1800초) | ✅ |
| **🎭 모션 효과** | Ken Burns 효과 (줌 + 팬) | ✅ |
| **🤖 AutoPilot** | 토픽 입력 → 자동 생성 | ✅ |
| **🖼️ AI 썸네일** | 자동 썸네일 생성 | ✅ |
| **🎨 스타일 템플릿** | Professional, Cinematic, Anime, 3D | ✅ |
| **📝 자동 자막** | 단어 단위 애니메이션 | ✅ |
| **🎵 BGM/SFX** | 자동 오디오 믹싱 | ✅ |

---

## 🚀 **빠른 시작**

### 1️⃣ **AutoPilot 모드 (원클릭 자동화)**

```bash
# 기본 실행 (60초 비디오)
python banana_autopilot.py --topic "비트코인 가격 분석"

# 길이 지정 (300초 = 5분)
python banana_autopilot.py --topic "코스피 급등 원인" --duration 300

# 프리셋 사용
python banana_autopilot.py --topic "환율 변동 분석" --preset medium

# 스타일 지정
python banana_autopilot.py --topic "투자 전략" --duration 120 --style cinematic
```

### 2️⃣ **길이 프리셋**

| 프리셋 | 길이 | 용도 |
|--------|------|------|
| `quick` | 20초 | 빠른 뉴스 |
| `short` | 30초 | 짧은 정보 |
| `standard` | 60초 | 표준 길이 |
| `shorts` | 120초 | YouTube Shorts 최대 |
| `medium` | 300초 (5분) | 중간 분석 |
| `long` | 600초 (10분) | 긴 영상 |
| `extended` | 1200초 (20분) | 확장 콘텐츠 |
| `maximum` | 1800초 (30분) | 최대 길이 |

### 3️⃣ **스타일 템플릿**

| 스타일 | 특징 | 적합 콘텐츠 |
|--------|------|------------|
| `professional` | 전문적, 깔끔 | 경제 뉴스, 투자 정보 |
| `cinematic` | 영화적, 드라마틱 | 스토리텔링, 다큐멘터리 |
| `anime` | 생동감, 화려함 | 엔터테인먼트, 트렌드 |
| `3d` | 미래적, 기술적 | 테크 뉴스, 혁신 주제 |

---

## 📦 **설치 및 설정**

### 1️⃣ **필수 패키지 설치**

```bash
# Python 가상환경 활성화
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# 패키지 설치
pip install -r requirements.txt
```

### 2️⃣ **환경변수 설정**

`.env` 파일 생성:

```env
# OpenAI API 키 (AI 이미지 생성용)
OPENAI_API_KEY=sk-proj-...

# YouTube API (업로드용, 선택)
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
```

### 3️⃣ **설정 파일**

`config/config.yaml`에서 Banana 모드 설정:

```yaml
# Banana 모드 설정
banana_mode:
  enabled: true  # Banana 모드 활성화
  
  # AutoPilot 설정
  autopilot:
    enabled: true  # 원클릭 자동화
    topic_based: true  # 토픽 입력만으로 전체 자동 생성
    
  # 장면 자동 분할
  scene_segmentation:
    enabled: true
    method: "auto"  # auto: AI 기반 자동
    min_scene_duration: 3  # 최소 장면 길이 (초)
    max_scene_duration: 10  # 최대 장면 길이 (초)
    
  # AI 이미지 생성
  background:
    type: "ai_image"
    ai_image:
      enabled: true
      provider: "openai"  # DALL-E 3
      model: "dall-e-3"
      quality: "hd"
```

---

## 🎬 **사용 예시**

### **예시 1: 20초 빠른 뉴스**

```bash
python banana_autopilot.py \
  --topic "비트코인 급등" \
  --preset quick \
  --style professional
```

**결과:**
- 📹 **영상 길이**: 20초
- 🎨 **장면 수**: 3-4개
- ⏱️ **생성 시간**: ~3분
- 💾 **파일 크기**: ~300KB

### **예시 2: 5분 중간 분석**

```bash
python banana_autopilot.py \
  --topic "코스피 3000선 돌파 원인 분석" \
  --preset medium \
  --style cinematic
```

**결과:**
- 📹 **영상 길이**: 5분 (300초)
- 🎨 **장면 수**: 30-50개
- ⏱️ **생성 시간**: ~10-15분
- 💾 **파일 크기**: ~5-8MB

### **예시 3: 30분 최대 길이**

```bash
python banana_autopilot.py \
  --topic "2024년 경제 전망과 투자 전략" \
  --preset maximum \
  --style professional
```

**결과:**
- 📹 **영상 길이**: 30분 (1800초)
- 🎨 **장면 수**: 180-360개
- ⏱️ **생성 시간**: ~1-2시간
- 💾 **파일 크기**: ~30-50MB

---

## 🛠️ **고급 사용법**

### **1. 수동 스크립트 모드**

OpenAI API 없이도 작동 가능:

```python
# test_banana_quick.py 참고
from src.video_generation.banana_video_creator import BananaVideoCreator

creator = BananaVideoCreator()
creator.create_banana_video(
    topic="비트코인 분석",
    script_text="당신의 스크립트...",
    audio_path="audio.mp3",
    output_path="output.mp4",
    target_duration=60,
    style='professional'
)
```

### **2. AI 이미지 없이 실행**

`config/config.yaml` 수정:

```yaml
background:
  type: "gradient"  # ai_image → gradient로 변경
  ai_image:
    enabled: false  # AI 이미지 비활성화
```

### **3. 배치 생성**

여러 비디오 동시 생성:

```bash
# 스크립트 작성
for topic in "비트코인" "이더리움" "리플"; do
  python banana_autopilot.py \
    --topic "${topic} 가격 분석" \
    --preset standard
done
```

---

## 📊 **성능 벤치마크**

| 영상 길이 | 장면 수 | 생성 시간 | 파일 크기 | OpenAI 비용* |
|-----------|---------|----------|----------|--------------|
| 20초 | 3-4개 | ~3분 | ~300KB | ~$0.12 |
| 1분 | 6-12개 | ~5분 | ~500KB | ~$0.36 |
| 5분 | 30-50개 | ~15분 | ~5MB | ~$1.80 |
| 10분 | 60-120개 | ~30분 | ~10MB | ~$3.60 |
| 30분 | 180-360개 | ~2시간 | ~30MB | ~$10.80 |

_*DALL-E 3 HD 기준 ($0.04/이미지)_

---

## 🧪 **테스트**

### **빠른 테스트 (20초)**

```bash
python test_banana_quick.py
```

### **전체 테스트 (20초, 1분, 5분)**

```bash
python test_banana_mode.py
```

### **생성된 파일 확인**

```bash
ls -lh data/videos/
```

---

## 🎨 **Banana vs 기존 시스템 비교**

| 기능 | 기존 시스템 | 🍌 Banana 모드 |
|------|------------|----------------|
| **영상 길이** | ~170초 (Shorts 최대) | ✅ **20초 ~ 30분** |
| **AI 이미지** | ❌ 없음 | ✅ **DALL-E 3 자동 생성** |
| **장면 분할** | ❌ 고정 배경 | ✅ **자동 분할 + 루프** |
| **모션 효과** | ❌ 정적 | ✅ **Ken Burns 효과** |
| **스타일 템플릿** | ❌ 1종류 | ✅ **4종류** |
| **AutoPilot** | ⚠️ 부분 지원 | ✅ **완전 자동화** |
| **AI 썸네일** | ❌ 수동 | ✅ **자동 생성** |
| **비용** | 무료 | ~$0.04/장면 (AI 이미지) |

---

## 💡 **팁 & 트릭**

### 1️⃣ **비용 절감**

```yaml
# AI 이미지 비활성화 (무료)
background:
  type: "gradient"  # 그라데이션 배경 사용
```

### 2️⃣ **속도 최적화**

```yaml
# 장면 수 줄이기
scene_segmentation:
  min_scene_duration: 5  # 3초 → 5초
  max_scene_duration: 15  # 10초 → 15초
```

### 3️⃣ **품질 향상**

```yaml
# HD 품질 사용
ai_image:
  quality: "hd"  # standard → hd
  style: "vivid"  # natural → vivid
```

---

## 🐛 **문제 해결**

### **OpenAI API 오류**

```bash
# API 키 확인
echo $OPENAI_API_KEY

# 키 테스트
python test_openai_key.py
```

### **메모리 부족**

```bash
# 장면 수 줄이기 (config.yaml)
max_scene_duration: 15  # 10 → 15초
```

### **렌더링 느림**

```bash
# 병렬 처리 증가 (config.yaml)
performance:
  max_workers: 8  # 4 → 8
```

---

## 📚 **관련 문서**

- [기본 사용법](README.md)
- [API 키 설정](OPENAI_SETUP_GUIDE.md)
- [문제 해결](API_KEY_TROUBLESHOOTING.md)
- [설정 가이드](config/config.yaml)

---

## 🎉 **성공 사례**

```bash
# 실제 생성된 비디오
ls -lh data/videos/

# 출력:
# -rw-r--r-- 1 user user 280K  test_banana_1_*.mp4  (20초)
# -rw-r--r-- 1 user user 257K  quick_test_*.mp4     (20초)
# -rw-r--r-- 1 user user 445K  shorts_1_*.mp4       (20초)
```

---

## 🚀 **다음 단계**

1. **OpenAI API 키 발급** → [가이드](OPENAI_SETUP_GUIDE.md)
2. **첫 비디오 생성** → `python banana_autopilot.py --topic "테스트" --preset quick`
3. **AutoPilot 활성화** → `config/config.yaml`에서 설정
4. **대량 생성** → 스케줄러 설정

---

## 💬 **문의 및 지원**

- 이슈: [GitHub Issues](https://github.com/yourusername/economic-shorts-automation/issues)
- 문서: [Wiki](https://github.com/yourusername/economic-shorts-automation/wiki)

---

**🍌 Banana 모드로 영상 제작을 혁신하세요!**
