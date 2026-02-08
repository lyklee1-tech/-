# 🍌 Banana 스타일 업그레이드 계획

## 📊 현재 vs 목표

### ✅ 이미 완성된 기능
- [x] 경제 뉴스 자동 수집
- [x] AI 스크립트 생성 (OpenAI GPT-4)
- [x] TTS 음성 생성 (gTTS, ElevenLabs 지원)
- [x] 배경음악 자동 선택 (4곡)
- [x] 효과음 시스템 (6개 타이밍)
- [x] 자막 자동 생성 및 동기화
- [x] 투자 책임 문구 자동 삽입
- [x] 비디오 길이 조절 (20-170초)
- [x] YouTube 자동 업로드
- [x] 스케줄러 자동화

### 🎯 Banana 스타일로 추가할 기능

## Phase 1: 시각적 콘텐츠 강화

### 1.1 AI 이미지 생성 통합
**목표**: 각 장면에 맞는 이미지 자동 생성

**구현 방법**:
```python
# DALL-E 3 통합
from openai import OpenAI

def generate_scene_image(scene_description):
    """장면 설명 → AI 이미지 생성"""
    client = OpenAI()
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"Financial news illustration: {scene_description}",
        size="1024x1792",  # Vertical for Shorts
        quality="standard",
        n=1,
    )
    
    return response.data[0].url
```

**비용**: $0.04 per image (DALL-E 3)

### 1.2 스톡 이미지/비디오 통합
**대안**: Unsplash, Pexels API (무료!)

```python
def get_stock_image(keyword):
    """키워드 → 무료 스톡 이미지"""
    import requests
    
    # Unsplash API
    response = requests.get(
        f"https://api.unsplash.com/photos/random",
        params={
            "query": keyword,
            "orientation": "portrait"
        }
    )
    
    return response.json()['urls']['regular']
```

### 1.3 차트 자동 생성
**이미 구현됨!** 하지만 개선 가능:

```python
# 현재: matplotlib 기본 차트
# 업그레이드: Plotly (더 예쁜 차트)

import plotly.graph_objects as go

def create_animated_chart(data):
    """애니메이션 차트 생성"""
    fig = go.Figure(
        data=[go.Scatter(x=data['date'], y=data['price'])],
        layout=go.Layout(
            updatemenus=[dict(type="buttons", direction="left")]
        )
    )
    
    fig.write_image("chart.png")
```

## Phase 2: 장면 분할 시스템

### 2.1 스크립트 자동 분할
**목표**: 긴 스크립트를 논리적 장면으로 분할

```python
def split_script_into_scenes(script):
    """스크립트 → 장면 리스트"""
    from openai import OpenAI
    
    client = OpenAI()
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": "스크립트를 논리적 장면으로 분할하세요. 각 장면은 5-10초 분량."
        }, {
            "role": "user",
            "content": script
        }]
    )
    
    # Response: JSON array of scenes
    return parse_scenes(response.choices[0].message.content)
```

### 2.2 장면별 비주얼 매칭
```python
def generate_scene_visuals(scenes):
    """각 장면에 맞는 비주얼 생성"""
    visuals = []
    
    for scene in scenes:
        # 키워드 추출
        keywords = extract_keywords(scene['text'])
        
        # 비주얼 타입 결정
        visual_type = determine_visual_type(keywords)
        
        if visual_type == 'chart':
            visuals.append(create_chart(scene['data']))
        elif visual_type == 'image':
            visuals.append(get_stock_image(keywords[0]))
        elif visual_type == 'ai_generated':
            visuals.append(generate_scene_image(scene['description']))
    
    return visuals
```

## Phase 3: AutoPilot 모드

### 3.1 원클릭 자동화
```python
def autopilot_mode(topic, style='professional'):
    """토픽 → 완성된 비디오 (원클릭)"""
    
    # 1. 뉴스 수집
    news = collect_news(topic)
    
    # 2. 스크립트 생성
    script = generate_script(news, style)
    
    # 3. 장면 분할
    scenes = split_script_into_scenes(script)
    
    # 4. 각 장면 처리
    for scene in scenes:
        scene['audio'] = generate_tts(scene['text'])
        scene['visual'] = generate_scene_visuals([scene])[0]
        scene['duration'] = calculate_duration(scene['audio'])
    
    # 5. 비디오 합성
    video = composite_video(scenes)
    
    # 6. BGM & SFX 추가
    final_video = add_audio_mixing(video, scenes)
    
    # 7. 자막 추가
    final_video = add_subtitles(final_video, script)
    
    # 8. 썸네일 생성
    thumbnail = generate_thumbnail(script, scenes[0]['visual'])
    
    return {
        'video': final_video,
        'thumbnail': thumbnail,
        'script': script
    }
```

### 3.2 스타일 프리셋
```yaml
# config/styles.yaml

styles:
  professional:
    visual_style: "clean, modern, corporate"
    color_scheme: "blue, white"
    font: "NanumGothicBold"
    bgm_genre: "corporate"
    
  energetic:
    visual_style: "dynamic, colorful, bold"
    color_scheme: "red, yellow"
    font: "NanumSquareRoundEB"
    bgm_genre: "upbeat"
    
  minimalist:
    visual_style: "simple, elegant, zen"
    color_scheme: "black, white"
    font: "NanumMyeongjo"
    bgm_genre: "ambient"
```

## Phase 4: 썸네일 생성

### 4.1 AI 썸네일 디자인
```python
def generate_thumbnail(title, main_image):
    """제목 + 이미지 → YouTube 썸네일"""
    from PIL import Image, ImageDraw, ImageFont
    
    # 배경 이미지
    thumbnail = Image.new('RGB', (1280, 720), color='#1a1a2e')
    
    # 메인 이미지 합성
    main_img = Image.open(main_image).resize((800, 720))
    thumbnail.paste(main_img, (0, 0))
    
    # 텍스트 오버레이
    draw = ImageDraw.Draw(thumbnail)
    font = ImageFont.truetype('NanumGothicBold.ttf', 80)
    
    # 제목 추가 (자동 줄바꿈)
    lines = wrap_text(title, 20)
    y = 50
    for line in lines:
        draw.text((50, y), line, font=font, fill='#ffffff',
                  stroke_width=4, stroke_fill='#000000')
        y += 100
    
    return thumbnail
```

## Phase 5: 고급 기능

### 5.1 모션 그래픽
```python
# MoviePy 애니메이션
def add_motion_effects(clip):
    """이미지에 모션 효과 추가"""
    return clip.resize(lambda t: 1 + 0.05*t)  # Zoom in
```

### 5.2 트랜지션 효과
```python
def add_transitions(scenes):
    """장면 간 트랜지션 추가"""
    from moviepy.editor import *
    
    clips = []
    for i, scene in enumerate(scenes):
        clip = ImageClip(scene['visual']).set_duration(scene['duration'])
        
        if i < len(scenes) - 1:
            # Fade transition
            clip = clip.crossfadeout(0.5)
        
        clips.append(clip)
    
    return concatenate_videoclips(clips)
```

### 5.3 텍스트 애니메이션
```python
def animate_text(text, duration):
    """텍스트 타이핑 애니메이션"""
    from moviepy.editor import TextClip
    
    def make_frame(t):
        # 점진적 표시
        chars_visible = int(len(text) * t / duration)
        return TextClip(text[:chars_visible], font='NanumGothic', 
                        fontsize=60, color='white').get_frame(0)
    
    return VideoClip(make_frame, duration=duration)
```

## 🚀 구현 우선순위

### Tier 1 (즉시 가능, 무료)
1. ✅ **스톡 이미지 통합** (Unsplash/Pexels API)
2. ✅ **차트 개선** (Plotly)
3. ✅ **썸네일 생성** (PIL)
4. ✅ **스크립트 장면 분할** (GPT-4)

### Tier 2 (OpenAI 필요)
1. ⏳ **AI 이미지 생성** (DALL-E 3, $0.04/image)
2. ⏳ **AutoPilot 모드**
3. ⏳ **스타일 프리셋**

### Tier 3 (고급 기능)
1. 🔮 **모션 그래픽**
2. 🔮 **트랜지션 효과**
3. 🔮 **텍스트 애니메이션**

## 💰 비용 분석

### Banana 플랫폼 가격
- 미확인 (SaaS 구독 모델로 추정)

### 우리 시스템 비용
- **현재**: $0 (OpenAI API 제외)
- **OpenAI 추가 시**:
  - 스크립트: $0.002/video
  - DALL-E 3: $0.04/image (장면당)
  - 총: ~$0.10-0.20/video

### 무료 대안
- Unsplash/Pexels: 무료
- 차트: 무료 (matplotlib/plotly)
- 썸네일: 무료 (PIL)

## 📅 개발 로드맵

### Week 1: 시각적 콘텐츠
- [ ] Unsplash API 통합
- [ ] 스톡 이미지 자동 선택
- [ ] 차트 스타일 개선

### Week 2: 장면 관리
- [ ] 스크립트 자동 분할
- [ ] 장면별 비주얼 매칭
- [ ] 타이밍 자동 조정

### Week 3: AutoPilot
- [ ] 원클릭 워크플로우
- [ ] 스타일 프리셋
- [ ] 에러 핸들링

### Week 4: 썸네일 & 고급 기능
- [ ] 썸네일 자동 생성
- [ ] 모션 효과
- [ ] 트랜지션

## 🎯 최종 목표

**"경제 뉴스 토픽 입력 → 완성된 YouTube Shorts + 썸네일 (원클릭)"**

```python
# 최종 사용 예시
result = autopilot_mode(
    topic="비트코인 급등",
    style="professional",
    duration=60
)

print(f"✅ 비디오: {result['video']}")
print(f"✅ 썸네일: {result['thumbnail']}")
print(f"✅ 스크립트: {result['script']}")
```

---

**현재 시스템도 훌륭하지만, 이 업그레이드를 통해 Banana 수준의 자동화를 달성할 수 있습니다!**
