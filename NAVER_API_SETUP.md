# 네이버 API 설정 가이드

## 1. API 키 발급 받기

**네이버 개발자 센터**: https://developers.naver.com/

1. 로그인
2. Application → 애플리케이션 등록
3. 애플리케이션 이름: `경제 뉴스 자동화`
4. 사용 API: `검색` 선택
5. 비로그인 오픈 API 서비스 환경: `WEB 설정`
6. 웹 서비스 URL: `http://localhost`
7. 등록 완료 → Client ID와 Client Secret 복사

## 2. .env 파일 생성/수정

```bash
# /home/user/webapp/.env 파일에 추가

# 네이버 검색 API
NAVER_CLIENT_ID=발급받은_Client_ID_여기에_붙여넣기
NAVER_CLIENT_SECRET=발급받은_Client_Secret_여기에_붙여넣기

# YouTube Data API (선택사항)
YOUTUBE_API_KEY=발급받은_YouTube_API_키_여기에_붙여넣기
```

## 3. 서버 재시작

```bash
cd /home/user/webapp
python web_dashboard.py
```

## 4. 테스트

웹 대시보드에서 "🔄 새로고침" 버튼을 클릭하여 실시간 트렌드를 확인하세요!

## 참고사항

- **무료 할당량**: 일일 25,000 호출
- **API 키 없이도 동작**: 샘플 데이터 사용
- **실시간 트렌드**: API 키 설정 시 활성화

## 문제 해결

### Client ID/Secret이 보이지 않는 경우
- Application 페이지에서 생성한 애플리케이션 클릭
- "상세 정보" 확인

### API 호출 실패
- Client ID/Secret이 정확한지 확인
- .env 파일 경로 확인
- 서버 재시작 여부 확인

