# 🎵 음악 파일 업로드 상태

## 📁 폴더 구조 (생성 완료)

```
data/audio/
├── bgm/                    ✅ 배경음악 폴더
│   └── (음악 파일 업로드 대기중...)
│
└── sfx/                    ✅ 효과음 폴더
    ├── intro/              ✅ 인트로 효과음
    ├── hook/               ✅ 후킹 효과음
    ├── key_point/          ✅ 핵심 포인트 효과음
    ├── chart_reveal/       ✅ 차트 등장 효과음
    ├── conclusion/         ✅ 결론 효과음
    ├── cta/                ✅ CTA 효과음
    ├── outro/              ✅ 아웃트로 효과음
    └── events/             ✅ 이벤트 효과음
```

## 🔄 업로드 대기 중

### Windows 로컬 파일
```
C:\Users\user\Desktop\economic_shorts\assets\audio\
├── bgm\
│   ├── track1.mp3
│   ├── track2.mp3
│   └── ...
└── sfx\
    ├── intro\
    │   ├── whoosh.mp3
    │   └── ...
    ├── hook\
    │   ├── impact.mp3
    │   └── ...
    └── ...
```

### 서버 대상 경로
```
/home/user/webapp/data/audio/bgm/
/home/user/webapp/data/audio/sfx/{category}/
```

## 📤 업로드 방법

### 방법 1: 파일 업로드 (추천)
1. Windows 파일 선택
2. 서버 폴더로 복사/이동
3. 업로드 확인: `python upload_audio_helper.py`

### 방법 2: SCP 사용
```bash
# BGM 업로드
scp C:\Users\user\Desktop\economic_shorts\assets\audio\bgm\*.mp3 \
    user@server:/home/user/webapp/data/audio/bgm/

# SFX 업로드
scp -r C:\Users\user\Desktop\economic_shorts\assets\audio\sfx\* \
    user@server:/home/user/webapp/data/audio/sfx/
```

### 방법 3: 업로드 인터페이스 사용
- 웹 파일 관리자
- FTP/SFTP 클라이언트 (FileZilla, WinSCP)

## ✅ 업로드 후 확인

```bash
# 1. 업로드된 파일 확인
python upload_audio_helper.py

# 2. 테스트 비디오 생성
python main.py --mode single --preset quick

# 3. 생성된 비디오 확인
ls -lh data/videos/

# 4. 음향 품질 확인
# → 배경음악과 효과음이 적절히 믹싱되었는지 확인
```

## 🎯 시스템 설정 (완료)

- ✅ config.yaml: `source: file` 설정됨
- ✅ BGM 볼륨: 0.15 (나레이션 방해하지 않음)
- ✅ SFX 볼륨: 0.4 (명확하게 들림)
- ✅ AI 자동 생성: 비활성화 (로컬 파일 우선)
- ✅ 카테고리별 폴더: 지원됨

## 📝 참고 사항

### BGM 권장사항
- 형식: MP3, WAV
- 길이: 2-3분
- 스타일: Corporate, Minimal Tech, Ambient
- 여러 파일 → 랜덤 선택

### SFX 권장사항
- 형식: MP3, WAV
- 길이: 0.1-2초
- 카테고리별 정리
- 파일명: 영어 소문자, 언더스코어

## 🚀 다음 단계

1. ⏳ Windows 로컬 파일 → 서버 업로드
2. ✅ `python upload_audio_helper.py` 실행
3. ✅ `python main.py --mode single --preset quick` 테스트
4. ✅ 비디오 확인 및 음향 조정
5. ✅ `python main.py --mode auto --interval 2` 자동화 시작

---

**상태**: 시스템 준비 완료 ✅ | 파일 업로드 대기 중 ⏳
