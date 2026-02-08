# 📚 사용 예제 및 튜토리얼

실제 사용 예제와 고급 활용법을 소개합니다.

## 📑 목차
1. [기본 사용 예제](#기본-사용-예제)
2. [고급 커스터마이징](#고급-커스터마이징)
3. [데이터 수집 예제](#데이터-수집-예제)
4. [스크립트 생성 예제](#스크립트-생성-예제)
5. [비디오 제작 예제](#비디오-제작-예제)
6. [배치 작업 예제](#배치-작업-예제)

---

## 기본 사용 예제

### 예제 1: 비트코인 급등 Shorts 만들기

```python
from src.data_collection.stock_api import StockDataCollector
from src.script_generation.gpt_script import ScriptGenerator
from src.tts.tts_generator import TTSGenerator
from src.video_generation.video_creator import VideoCreator

# 1. 비트코인 데이터 수집
collector = StockDataCollector()
btc_data = collector.get_current_price('BTC-USD')

# 2. 스크립트 생성
generator = ScriptGenerator()
script = generator.generate_script(
    topic=f"비트코인 {btc_data['change_percent']:+.1f}% 변동",
    data=btc_data
)

# 3. 음성 생성
tts = TTSGenerator()
tts.generate_audio(
    text=script['script'],
    output_path='data/audio/btc_shorts.mp3'
)

# 4. 비디오 생성
creator = VideoCreator()
creator.create_shorts_video(
    audio_path='data/audio/btc_shorts.mp3',
    script_text=script['script'],
    output_path='data/videos/btc_shorts.mp4',
    title_text=script['hook']
)

print(f"✅ 완성! {script['title']}")
```

### 예제 2: 시장 요약 Shorts 만들기

```python
from src.data_collection.stock_api import StockDataCollector
from src.script_generation.gpt_script import ScriptGenerator

# 시장 데이터 수집
collector = StockDataCollector()
market_summary = collector.get_market_summary()

# 흥미로운 이슈 찾기
stories = collector.get_interesting_stories()

if stories:
    story = stories[0]
    
    # 스크립트 생성
    generator = ScriptGenerator()
    script = generator.generate_script(
        topic=story['title'],
        data=story['data']
    )
    
    print(f"제목: {script['title']}")
    print(f"스크립트: {script['script']}")
```

---

## 고급 커스터마이징

### 예제 3: 특정 스타일의 스크립트 생성

```python
from src.script_generation.gpt_script import ScriptGenerator
import yaml

# 설정 파일 수정
config = {
    'script': {
        'style': '경제분석가',
        'tone': '전문적이고 날카로운 분석',
        'target_audience': '40-50대 투자자',
        'min_length': 180,
        'max_length': 220
    }
}

# 임시 설정 파일 저장
with open('config/custom_config.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(config, f, allow_unicode=True)

# 커스텀 설정으로 생성
generator = ScriptGenerator('config/custom_config.yaml')
script = generator.generate_script(
    topic="삼성전자 실적 발표",
    data={'revenue': 68000000000000, 'profit': 5000000000000}
)
```

### 예제 4: 다중 언어 TTS

```python
from src.tts.tts_generator import TTSGenerator

tts = TTSGenerator()

# 한국어 음성
tts.generate_audio(
    text="비트코인이 10% 상승했습니다.",
    output_path='data/audio/korean.mp3',
    provider='google'
)

# 영어 음성 (ElevenLabs)
tts.generate_audio(
    text="Bitcoin surged by 10% today.",
    output_path='data/audio/english.mp3',
    provider='elevenlabs'
)
```

---

## 데이터 수집 예제

### 예제 5: 특정 종목 추적

```python
from src.data_collection.stock_api import StockDataCollector
import json
from datetime import datetime

collector = StockDataCollector()

# 추적할 종목 리스트
watchlist = ['005930.KS', 'AAPL', 'TSLA', 'BTC-USD']

results = {}
for symbol in watchlist:
    data = collector.get_current_price(symbol)
    if data:
        results[symbol] = data
        print(f"{symbol}: {data['current_price']:,.2f} ({data['change_percent']:+.2f}%)")

# 저장
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
with open(f'data/processed/watchlist_{timestamp}.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

### 예제 6: 뉴스 키워드 필터링

```python
from src.data_collection.news_scraper import NewsScraper

scraper = NewsScraper()
news = scraper.fetch_all_news()

# 특정 키워드로 필터링
keywords = ['반도체', 'AI', '전기차']

filtered = []
for article in news:
    text = article['title'] + ' ' + article['summary']
    if any(keyword in text for keyword in keywords):
        filtered.append(article)

print(f"총 {len(filtered)}개 관련 뉴스 발견")
for n in filtered[:5]:
    print(f"- [{n['source']}] {n['title']}")
```

---

## 스크립트 생성 예제

### 예제 7: 여러 버전의 스크립트 생성

```python
from src.script_generation.gpt_script import ScriptGenerator

generator = ScriptGenerator()

topic = "환율 1,400원 돌파"
data = {'usd_krw': 1405, 'change': 15}

# 3가지 버전 생성
scripts = []
for i in range(3):
    script = generator.generate_script(topic, data)
    scripts.append(script)
    print(f"\n버전 {i+1}: {script['title']}")
    print(script['script'][:100] + "...")

# 가장 마음에 드는 버전 선택
best = scripts[0]  # 또는 수동 선택
```

### 예제 8: 스크립트 개선하기

```python
from src.script_generation.gpt_script import ScriptGenerator

generator = ScriptGenerator()

original_script = """
비트코인이 올랐습니다. 
많이 올랐어요.
이유는 ETF 때문입니다.
"""

# 스크립트 개선
improved = generator.refine_script(
    script=original_script,
    feedback="""
- 구체적인 숫자 추가
- 더 흥미진진하게
- 후킹 멘트 강화
- 전문 용어를 쉽게 설명
"""
)

print("개선된 스크립트:")
print(improved)
```

---

## 비디오 제작 예제

### 예제 9: 차트 포함 비디오

```python
from src.video_generation.chart_generator import ChartGenerator
from src.video_generation.video_creator import VideoCreator

# 1. 차트 생성
chart_gen = ChartGenerator()
chart_gen.create_price_change_visual(
    symbol='비트코인',
    current_price=58500000,
    change_percent=10.5,
    output_path='data/charts/btc_chart.png'
)

# 2. 차트 포함 비디오 생성
creator = VideoCreator()
creator.create_shorts_video(
    audio_path='data/audio/btc_audio.mp3',
    script_text='비트코인이 10% 급등했습니다...',
    output_path='data/videos/btc_with_chart.mp4',
    chart_image='data/charts/btc_chart.png'  # 차트 추가
)
```

### 예제 10: 커스텀 썸네일과 투자 책임 문구

```python
from src.video_generation.video_creator import VideoCreator
from PIL import Image, ImageDraw, ImageFont

creator = VideoCreator()

# 투자 책임 문구 포함 비디오 생성 (기본: 활성화)
creator.create_shorts_video(
    audio_path='data/audio/btc_audio.mp3',
    script_text='비트코인이 10% 급등했습니다...',
    output_path='data/videos/btc_with_disclaimer.mp4',
    show_disclaimer=True  # 투자 책임 문구 표시 (기본값)
)

# 투자 책임 문구 없이 생성
creator.create_shorts_video(
    audio_path='data/audio/news_audio.mp3',
    script_text='오늘의 경제 뉴스입니다...',
    output_path='data/videos/news_without_disclaimer.mp4',
    show_disclaimer=False  # 투자 책임 문구 제거
)

# 간단한 썸네일
creator.create_thumbnail(
    text='비트코인 급등',
    output_path='data/videos/thumbnail1.jpg'
)

# 고급 커스텀 썸네일
img = Image.new('RGB', (1280, 720), color='#1a1a2e')
draw = ImageDraw.Draw(img)

# 텍스트 추가
font = ImageFont.truetype('/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf', 100)
draw.text((640, 300), '10% 급등!', font=font, fill='#00ff88', anchor='mm')
draw.text((640, 450), '지금 확인하세요', font=ImageFont.truetype(font.path, 50), fill='white', anchor='mm')

img.save('data/videos/custom_thumbnail.jpg', quality=95)
```

---

## 배치 작업 예제

### 예제 11: 한 번에 여러 Shorts 생성

```python
from src.data_collection.stock_api import StockDataCollector
from main import EconomicShortsAutomation

# 자동화 시스템 초기화
automation = EconomicShortsAutomation()

# 1. 데이터 수집
data = automation.collect_data()

# 2. 상위 5개 이슈에 대한 스크립트 생성
collector = StockDataCollector()
stories = collector.get_interesting_stories()

topics_data = []
for story in stories[:5]:
    topics_data.append({
        'topic': story['title'],
        'data': story['data']
    })

# 3. 스크립트 생성
scripts = automation.script_generator.generate_multiple_scripts(topics_data, count=5)

# 4. 비디오 제작
videos = automation.produce_videos(scripts)

print(f"✅ {len(videos)}개 비디오 생성 완료!")
for i, v in enumerate(videos, 1):
    print(f"{i}. {v['script']['title']}")
    print(f"   파일: {v['video_path']}")
```

### 예제 12: 특정 시간대 자동 게시

```python
from apscheduler.schedulers.blocking import BlockingScheduler
from main import EconomicShortsAutomation
from datetime import datetime

automation = EconomicShortsAutomation()
scheduler = BlockingScheduler()

def morning_job():
    """아침 시장 개장 전 게시"""
    print(f"[{datetime.now()}] 아침 Shorts 생성 시작")
    automation.run_single()

def evening_job():
    """저녁 시장 마감 후 게시"""
    print(f"[{datetime.now()}] 저녁 Shorts 생성 시작")
    automation.run_single()

# 평일 아침 8시 50분
scheduler.add_job(morning_job, 'cron', day_of_week='mon-fri', hour=8, minute=50)

# 평일 저녁 6시 10분
scheduler.add_job(evening_job, 'cron', day_of_week='mon-fri', hour=18, minute=10)

print("스케줄러 시작...")
scheduler.start()
```

---

## 🎓 학습 리소스

### Python 스크립트로 커스터마이징

프로젝트의 모든 모듈은 독립적으로 사용 가능합니다:

```python
# 각 모듈별 임포트
from src.data_collection.news_scraper import NewsScraper
from src.data_collection.stock_api import StockDataCollector
from src.script_generation.gpt_script import ScriptGenerator
from src.tts.tts_generator import TTSGenerator
from src.video_generation.video_creator import VideoCreator
from src.video_generation.chart_generator import ChartGenerator
from src.youtube_upload.uploader import YouTubeUploader

# 원하는 조합으로 사용 가능
```

### 설정 파일 활용

`config/config.yaml`의 모든 설정을 Python 코드에서 오버라이드 가능:

```python
import yaml

# 설정 로드
with open('config/config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 수정
config['video']['duration'] = 45
config['tts']['speed'] = 1.2

# 저장
with open('config/my_config.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(config, f, allow_unicode=True)

# 커스텀 설정으로 사용
automation = EconomicShortsAutomation('config/my_config.yaml')
```

---

## 🔗 더 많은 예제

더 많은 예제와 튜토리얼은 다음을 참고하세요:

- GitHub Repository: Examples 폴더
- 블로그 튜토리얼: (링크 추가)
- YouTube 튜토리얼: (링크 추가)

---

**질문이 있으신가요?**  
GitHub Issues 또는 Discussions에서 물어보세요!
