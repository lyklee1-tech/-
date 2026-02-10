# 🎥 YouTube Data API v3 설정 가이드

## 📌 현재 상태
- **프로젝트 ID**: `gen-lang-client-0392884733`
- **API 키**: 아직 발급되지 않음
- **필요한 API**: YouTube Data API v3

---

## 🚀 API 키 발급 단계별 가이드

### 1️⃣ Google Cloud Console 접속
```
https://console.cloud.google.com/
```

### 2️⃣ 프로젝트 선택
- 좌측 상단에서 프로젝트 선택
- `gen-lang-client-0392884733` 선택 (또는 새 프로젝트 생성)

### 3️⃣ YouTube Data API v3 활성화
1. 좌측 메뉴에서 **"API 및 서비스"** → **"라이브러리"** 클릭
2. 검색창에 `YouTube Data API v3` 입력
3. **"YouTube Data API v3"** 선택
4. **"사용 설정"** 버튼 클릭

### 4️⃣ API 키 생성
1. 좌측 메뉴에서 **"API 및 서비스"** → **"사용자 인증 정보"** 클릭
2. 상단의 **"+ 사용자 인증 정보 만들기"** 버튼 클릭
3. **"API 키"** 선택
4. API 키가 생성됨 (예: `AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
5. **복사** 버튼으로 API 키 복사

### 5️⃣ API 키 제한 설정 (선택사항)
- **"키 제한"** 클릭
- **애플리케이션 제한사항**: "없음" 또는 "HTTP 리퍼러"
- **API 제한사항**: "키 제한" → "YouTube Data API v3" 선택
- **저장** 클릭

---

## 🔧 프로젝트에 API 키 적용

### 방법 1: .env 파일 수정
```bash
# /home/user/webapp/.env 파일 열기
nano /home/user/webapp/.env

# 다음 라인 수정:
YOUTUBE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 저장 후 서버 재시작
cd /home/user/webapp
python web_dashboard.py
```

### 방법 2: 환경 변수로 직접 설정
```bash
export YOUTUBE_API_KEY="AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
cd /home/user/webapp
python web_dashboard.py
```

---

## ✅ API 키 테스트

API 키를 설정한 후 다음 명령으로 테스트:

```bash
cd /home/user/webapp
python verify_youtube_api.py
```

**성공 시 출력:**
```
✅ YouTube API 키가 유효합니다!
테스트 검색 결과: 1개

🔍 '경제사냥꾼' 채널 검색 중...

📋 검색된 채널: 1개
1. 경제사냥꾼
   채널 ID: UCxxxxxxxxxxxxxxxxxx
```

---

## 🎯 사용 가능한 기능 (API 키 설정 후)

### 1. YouTube 채널 스타일 학습
- 채널 URL 입력 → 실제 영상 분석
- 최신 영상 10개 자동 수집
- 제목/설명/길이 분석
- 스타일 패턴 추출

### 2. 맞춤형 대본 생성
- 분석된 스타일로 대본 자동 생성
- 키프레이즈 반영
- 톤 & 구조 적용

---

## 📊 API 할당량 정보

**YouTube Data API v3 무료 할당량:**
- 하루 10,000 쿼터 유닛
- 검색 요청: 100 유닛
- 영상 정보 요청: 1 유닛

**예상 사용량:**
- 채널 검색: 100 유닛
- 영상 10개 조회: 10 유닛
- **총 110 유닛 / 채널 분석**
- **하루 약 90회 채널 분석 가능**

---

## 🆘 문제 해결

### ❌ "API key not valid" 오류
**원인:**
- 잘못된 API 키
- YouTube Data API v3가 활성화되지 않음
- API 키 제한 설정 문제

**해결:**
1. API 키를 다시 복사하여 붙여넣기
2. YouTube Data API v3 활성화 확인
3. API 키 제한을 "없음"으로 설정

### ❌ "Quota exceeded" 오류
**원인:**
- 일일 할당량 초과 (10,000 유닛)

**해결:**
- 다음 날까지 대기
- 또는 결제를 활성화하여 할당량 증가

### ❌ 채널을 찾을 수 없음
**원인:**
- 채널 이름이 정확하지 않음
- 채널이 비공개 또는 삭제됨

**해결:**
- 정확한 채널 이름 또는 URL 사용
- 채널 ID로 직접 검색

---

## 📝 참고 링크

- **Google Cloud Console**: https://console.cloud.google.com/
- **YouTube Data API v3 문서**: https://developers.google.com/youtube/v3
- **API 키 관리**: https://console.cloud.google.com/apis/credentials
- **할당량 확인**: https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas

---

## 🎉 완료 후

API 키를 설정하면 다음 기능을 사용할 수 있습니다:

1. **실시간 채널 분석**: 경제사냥꾼 등 모든 YouTube 채널
2. **스타일 자동 학습**: 제목, 설명, 길이, 톤, 구조 분석
3. **맞춤 대본 생성**: 분석된 스타일로 자동 생성
4. **다양한 채널 지원**: 경제, 뉴스, 교육, 엔터테인먼트 등

---

**현재 상태**: API 키 없이도 샘플 데이터로 모든 기능 테스트 가능합니다! 🎨
