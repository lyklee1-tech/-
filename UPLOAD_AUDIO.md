# 🎵 음악 파일 업로드 가이드

경제 유튜브 Shorts 자동화 시스템에 사용할 배경음악(BGM)과 효과음(SFX)을 업로드하는 방법입니다.

## 📁 파일 구조

```
C:\Users\user\Desktop\economic_shorts\assets\audio\
├── bgm/          # 배경음악 파일들
│   ├── track1.mp3
│   ├── track2.mp3
│   └── ...
└── sfx/          # 효과음 파일들
    ├── intro/
    │   ├── whoosh.mp3
    │   ├── pop.mp3
    │   └── ...
    ├── hook/
    │   ├── impact.mp3
    │   ├── ding.mp3
    │   └── ...
    ├── key_point/
    ├── chart_reveal/
    ├── conclusion/
    ├── cta/
    └── outro/
```

## 🎼 배경음악 (BGM)

### 위치
```
data/audio/bgm/
```

### 권장 사양
- **형식**: MP3, WAV
- **길이**: 2-3분 (루프 가능)
- **스타일**: 
  - 경제 뉴스 어울리는 전문적 분위기
  - Corporate, Minimal Tech, Cinematic
  - 조용하고 깔끔한 배경음
- **볼륨**: 중간 레벨 (시스템에서 자동 조정)

### 추천 BGM 스타일
- ✅ 경제 뉴스 전용 Corporate BGM
- ✅ Minimal Tech (깔끔하고 현대적)
- ✅ Ambient/Atmospheric (차분한 분위기)
- ❌ 너무 시끄럽거나 멜로디가 강한 음악
- ❌ 가사가 있는 노래

### 업로드 방법
```bash
# 로컬 파일을 서버로 업로드
# (사용하는 방법에 따라 선택)

# 방법 1: SCP/SFTP 사용
scp C:\Users\user\Desktop\economic_shorts\assets\audio\bgm\*.mp3 user@server:/home/user/webapp/data/audio/bgm/

# 방법 2: 웹 인터페이스 업로드
# data/audio/bgm/ 폴더에 직접 업로드

# 방법 3: Git에 커밋 (작은 파일만)
# git add data/audio/bgm/*.mp3
# git commit -m "Add background music files"
```

## 🔔 효과음 (SFX)

### 위치
```
data/audio/sfx/
```

### 카테고리별 효과음

#### 1. 인트로 (intro/)
- **whoosh.mp3** - 빠른 휙 소리
- **pop.mp3** - 짧은 팝 소리
- **notification.mp3** - 알림음

**타이밍**: 0초 (영상 시작)

#### 2. 후킹 (hook/)
- **impact.mp3** - 임팩트 효과
- **ding.mp3** - 딩 소리
- **alert.mp3** - 주의 알림

**타이밍**: 2.5초 (후킹 멘트 시작)

#### 3. 핵심 포인트 (key_point/)
- **pop.mp3** - 강조 팝
- **click.mp3** - 클릭 소리
- **beep.mp3** - 비프음

**타이밍**: 중요 숫자 언급 시

#### 4. 차트 등장 (chart_reveal/)
- **reveal.mp3** - 데이터 공개 소리
- **growth.mp3** - 성장 톤
- **rising.mp3** - 상승 효과음

**타이밍**: 차트 표시 시점

#### 5. 결론 (conclusion/)
- **success.mp3** - 성공 완료
- **complete.mp3** - 완료 알림
- **finish.mp3** - 마무리 소리

**타이밍**: 결론 부분 (70% 지점)

#### 6. CTA (cta/)
- **button.mp3** - 버튼 클릭
- **like.mp3** - 좋아요 효과
- **subscribe.mp3** - 구독 벨 소리

**타이밍**: 구독 유도 멘트 (마지막 5초)

#### 7. 아웃트로 (outro/)
- **success-chime.mp3** - 종료 알림
- **soft-click.mp3** - 부드러운 종료

**타이밍**: 영상 마지막

### 효과음 권장 사양
- **형식**: MP3, WAV
- **길이**: 0.1 ~ 2초 (짧게!)
- **스타일**: 현대적 UI 사운드
- **볼륨**: 중간~높음 (명확하게 들려야 함)

### 이벤트 효과음 (events/)
특수 이벤트용 효과음

- **rising-tone.mp3** - 가격 상승
- **falling-tone.mp3** - 가격 하락
- **warning.mp3** - 경고음
- **tick.mp3** - 틱 소리 (카운트다운)

## 📤 업로드 방법

### 옵션 1: 직접 업로드 (권장)

1. **디렉토리 구조 확인**
```bash
cd /home/user/webapp
ls -la data/audio/
```

2. **파일 업로드**
   - FTP/SFTP 클라이언트 사용 (FileZilla, WinSCP 등)
   - 클라우드 스토리지 (Google Drive, Dropbox) → 서버로 다운로드
   - 웹 인터페이스를 통한 업로드

3. **파일 확인**
```bash
# BGM 확인
ls -lh data/audio/bgm/

# SFX 확인
ls -lh data/audio/sfx/
```

### 옵션 2: 샘플 다운로드 스크립트 사용

```bash
# 무료 음악 다운로드 예시
cd /home/user/webapp

# BGM 다운로드 (Pixabay/Freesound에서)
wget https://example.com/bgm_sample.mp3 -O data/audio/bgm/corporate_minimal.mp3

# SFX 다운로드
wget https://example.com/whoosh.mp3 -O data/audio/sfx/intro/whoosh.mp3
```

## ⚙️ 설정 확인

### config.yaml 설정
```yaml
video:
  audio:
    background_music:
      enabled: true
      source: "file"  # 파일 소스 사용
      file_path: "data/audio/bgm/"
    
    sound_effects:
      enabled: true
      library_path: "data/audio/sfx/"
      auto_generate:
        enabled: false  # AI 생성 비활성화
```

## 🧪 테스트

### 1. 파일 확인
```bash
cd /home/user/webapp
python -c "
import os
from pathlib import Path

bgm_path = Path('data/audio/bgm')
sfx_path = Path('data/audio/sfx')

print('=== BGM 파일 ===')
if bgm_path.exists():
    for f in bgm_path.glob('*.*'):
        print(f'  ✓ {f.name}')
else:
    print('  ❌ BGM 폴더 없음')

print('\n=== SFX 파일 ===')
if sfx_path.exists():
    for category in sfx_path.iterdir():
        if category.is_dir():
            print(f'\n  [{category.name}]')
            for f in category.glob('*.*'):
                print(f'    ✓ {f.name}')
else:
    print('  ❌ SFX 폴더 없음')
"
```

### 2. 음향 시스템 테스트
```bash
python src/video_generation/sound_effects.py
```

### 3. 비디오 생성 테스트
```bash
# 짧은 테스트 비디오 생성
python main.py --mode single --preset quick
```

## 📋 체크리스트

업로드 전 확인사항:

- [ ] BGM 파일이 `data/audio/bgm/`에 있음
- [ ] SFX 파일이 카테고리별 폴더에 정리됨
- [ ] 모든 파일이 MP3 또는 WAV 형식
- [ ] 파일명에 공백 없음 (언더스코어 사용)
- [ ] 파일 크기 적절 (BGM: 2-5MB, SFX: 10-100KB)
- [ ] 저작권 확인 (로열티 프리)
- [ ] config.yaml에서 `source: "file"` 확인
- [ ] `auto_generate: false` 확인

## 🎯 다음 단계

파일 업로드가 완료되면:

1. **시스템 재시작**
```bash
# 설정 다시 로드
python check_system.py
```

2. **테스트 비디오 생성**
```bash
python main.py --mode single --preset short
```

3. **결과 확인**
```bash
# 생성된 비디오 재생하여 음향 확인
ls -lh data/videos/
```

4. **자동화 시작**
```bash
# 만족스러우면 스케줄러 가동
python main.py --mode auto --interval 2
```

## 💡 팁

- **BGM 순환**: 여러 BGM 파일을 넣으면 랜덤 선택됩니다
- **볼륨 조정**: config.yaml에서 `volume` 값 조정 (0.0 ~ 1.0)
- **효과음 비활성화**: 특정 효과음 `enabled: false`로 끄기
- **테스트 주기**: 새 파일 추가 시 항상 짧은 테스트 먼저 실행

## ❓ 문제 해결

### BGM이 안 들림
- 파일 경로 확인: `data/audio/bgm/*.mp3`
- 볼륨 확인: config.yaml에서 `volume: 0.15` → `0.3`으로 증가
- 파일 형식 확인: MP3 또는 WAV만 지원

### 효과음이 안 들림
- 폴더 구조 확인: `data/audio/sfx/intro/whoosh.mp3`
- `enabled: true` 확인
- 효과음 볼륨 증가: `volume: 0.4` → `0.6`

### 특정 효과음 건너뛰기
```yaml
sound_effects:
  timing:
    hook:
      enabled: false  # 후킹 효과음 비활성화
```

## 📞 지원

문제가 있으면 GitHub Issues로 문의하세요!

---

**준비 완료?** 파일 업로드 후 `python check_system.py`로 시스템 확인! 🚀
