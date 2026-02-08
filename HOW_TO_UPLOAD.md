# 🎵 음악 파일 업로드 방법 (실전 가이드)

## 📍 현재 상황

- **Windows 로컬**: `C:\Users\user\Desktop\economic_shorts\assets\audio\`
- **서버 대상**: `/home/user/webapp/data/audio/`

## 🚀 업로드 방법 (3가지)

---

## 방법 1: 파일 업로드 도구 사용 (가장 쉬움) ⭐ 추천

이 대화에서 **파일 첨부 기능**을 사용하세요!

### 단계:

1. **Windows 탐색기에서 파일 선택**
   ```
   C:\Users\user\Desktop\economic_shorts\assets\audio\bgm\
   → track1.mp3, track2.mp3 등 선택
   ```

2. **채팅창에 파일 드래그 & 드롭** 또는 첨부 버튼 클릭
   - 파일을 이 대화창으로 끌어다 놓기
   - 또는 📎 버튼으로 파일 선택

3. **업로드된 파일을 서버로 복사**
   - 업로드하면 AI가 자동으로 서버 경로로 복사해줍니다
   - 또는 직접 명령:
   ```bash
   # BGM 파일
   cp /path/to/uploaded/file.mp3 /home/user/webapp/data/audio/bgm/
   
   # SFX 파일
   cp /path/to/uploaded/sfx.mp3 /home/user/webapp/data/audio/sfx/intro/
   ```

---

## 방법 2: 구글 드라이브 경유 (중간 용량)

### 단계:

1. **Windows에서 구글 드라이브에 업로드**
   - 브라우저에서 https://drive.google.com 접속
   - `economic_shorts_audio` 폴더 생성
   - 모든 BGM과 SFX 파일 업로드

2. **공유 링크 생성**
   - 폴더 우클릭 → "공유" → "링크가 있는 모든 사용자"
   - 링크 복사 (예: https://drive.google.com/file/d/1ABC.../view)

3. **서버에서 다운로드**
   ```bash
   cd /home/user/webapp/data/audio
   
   # gdown 설치 (한 번만)
   pip install gdown
   
   # 파일 다운로드
   gdown [구글 드라이브 링크] -O bgm/track1.mp3
   
   # 또는 폴더 전체 다운로드
   gdown --folder [폴더 공유 링크]
   ```

---

## 방법 3: GitHub에 커밋 (소용량만)

⚠️ **주의**: MP3 파일이 크면 Git LFS 필요

### 단계:

1. **Windows에서 WSL 또는 Git Bash 열기**

2. **프로젝트 클론 (처음만)**
   ```bash
   git clone [저장소 URL]
   cd economic-youtube-automation
   ```

3. **음악 파일 복사**
   ```bash
   # Windows 폴더에서 프로젝트로 복사
   cp -r C:/Users/user/Desktop/economic_shorts/assets/audio/* data/audio/
   ```

4. **Git LFS 설정 (대용량 파일용)**
   ```bash
   git lfs install
   git lfs track "data/audio/**/*.mp3"
   git lfs track "data/audio/**/*.wav"
   git add .gitattributes
   ```

5. **커밋 및 푸시**
   ```bash
   git add data/audio/
   git commit -m "Add audio files (BGM and SFX)"
   git push
   ```

6. **서버에서 풀**
   ```bash
   cd /home/user/webapp
   git pull origin main
   ```

---

## 🎯 실전 추천: 방법 1 (채팅 업로드)

가장 빠르고 쉬운 방법입니다!

### 예시:

**사용자**: (파일 첨부)
```
📎 track1.mp3
📎 whoosh.mp3
📎 impact.mp3
```

**AI 응답**: 
"파일을 받았습니다! 서버로 복사하겠습니다..."
```bash
cp /tmp/track1.mp3 /home/user/webapp/data/audio/bgm/
cp /tmp/whoosh.mp3 /home/user/webapp/data/audio/sfx/intro/
cp /tmp/impact.mp3 /home/user/webapp/data/audio/sfx/hook/
```

---

## 📋 업로드 체크리스트

업로드할 파일 목록:

### BGM (배경음악) - 2~5개 권장
```
□ track1.mp3 (Corporate 스타일)
□ track2.mp3 (Minimal Tech)
□ track3.mp3 (Ambient)
```

### SFX (효과음) - 카테고리별

**intro/** (인트로)
```
□ whoosh.mp3
□ pop.mp3
```

**hook/** (후킹)
```
□ impact.mp3
□ ding.mp3
□ alert.mp3
```

**key_point/** (핵심 포인트)
```
□ pop.mp3
□ click.mp3
□ beep.mp3
```

**chart_reveal/** (차트 등장)
```
□ reveal.mp3
□ growth.mp3
□ rising.mp3
```

**conclusion/** (결론)
```
□ success.mp3
□ complete.mp3
```

**cta/** (CTA)
```
□ button.mp3
□ like.mp3
□ subscribe.mp3
```

---

## 🧪 업로드 후 확인

### 1. 파일 확인
```bash
python upload_audio_helper.py
```

### 2. 테스트 비디오 생성
```bash
python main.py --mode single --preset quick
```

### 3. 결과 확인
```bash
ls -lh data/videos/
# 생성된 비디오 재생하여 음향 확인
```

---

## 💡 팁

### 파일명 규칙
- ✅ 영어 소문자: `track1.mp3`, `whoosh.mp3`
- ✅ 언더스코어: `corporate_minimal.mp3`
- ❌ 공백 금지: `track 1.mp3` (X)
- ❌ 한글 금지: `배경음악1.mp3` (X)

### 파일 크기
- BGM: 2~5MB (2~3분 길이)
- SFX: 10~100KB (0.1~2초)

### 형식
- MP3 (권장): 압축률 좋음
- WAV: 고품질, 파일 큼

---

## ❓ 자주 묻는 질문

**Q: 파일을 어디에 업로드해야 하나요?**  
A: 이 채팅창에 파일을 첨부하시면 됩니다! AI가 자동으로 서버 경로로 복사해드립니다.

**Q: 한 번에 여러 파일을 올릴 수 있나요?**  
A: 네! 여러 파일을 선택해서 한 번에 첨부하세요.

**Q: ZIP으로 압축해서 올려도 되나요?**  
A: 네! ZIP 파일을 올리시면 AI가 자동으로 압축을 풀어드립니다.

**Q: 파일이 너무 많으면 어떻게 하나요?**  
A: 구글 드라이브 방법(방법 2)을 사용하시면 편합니다.

---

## 🎉 준비되셨나요?

**지금 바로 파일을 첨부해주세요!**

예시:
```
"BGM 파일 3개와 SFX 파일 10개를 업로드합니다"
[파일 첨부]
```

AI가 자동으로:
1. 파일을 받아서
2. 적절한 폴더에 복사하고
3. 확인 메시지를 보내드립니다!

---

**다음 단계**: 파일 업로드 → 테스트 → 자동화 시작 🚀
