"""
유튜브 자동 업로드 모듈
"""
import os
import pickle
from pathlib import Path
from typing import Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from loguru import logger
import yaml


class YouTubeUploader:
    """유튜브 비디오 자동 업로드"""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self, config_path='config/config.yaml'):
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            self.youtube_config = config['youtube']
        
        self.youtube = None
        self._authenticate()
    
    def _authenticate(self):
        """유튜브 API 인증"""
        creds = None
        token_path = 'config/youtube_token.pickle'
        
        # 저장된 토큰 로드
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # 토큰이 없거나 만료된 경우
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # OAuth 2.0 인증 플로우
                client_secrets_path = 'config/client_secrets.json'
                
                if not os.path.exists(client_secrets_path):
                    logger.error(f"클라이언트 시크릿 파일이 없습니다: {client_secrets_path}")
                    logger.info("Google Cloud Console에서 OAuth 2.0 클라이언트 ID를 생성하고 다운로드하세요.")
                    return
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # 토큰 저장
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        # YouTube API 클라이언트 생성
        self.youtube = build('youtube', 'v3', credentials=creds)
        logger.info("유튜브 API 인증 완료")
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list,
        category_id: str = '25',
        privacy_status: str = 'public',
        thumbnail_path: Optional[str] = None
    ) -> Optional[str]:
        """
        비디오 업로드
        
        Args:
            video_path: 비디오 파일 경로
            title: 비디오 제목
            description: 비디오 설명
            tags: 태그 리스트
            category_id: 카테고리 ID (25 = News & Politics)
            privacy_status: 공개 상태 (public, private, unlisted)
            thumbnail_path: 썸네일 이미지 경로 (선택)
        
        Returns:
            업로드된 비디오 ID
        """
        if not self.youtube:
            logger.error("유튜브 API가 인증되지 않았습니다")
            return None
        
        if not os.path.exists(video_path):
            logger.error(f"비디오 파일이 없습니다: {video_path}")
            return None
        
        try:
            # 비디오 메타데이터
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # 미디어 파일
            media = MediaFileUpload(
                video_path,
                chunksize=-1,
                resumable=True
            )
            
            # 업로드 요청
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            logger.info(f"비디오 업로드 시작: {title}")
            
            # 업로드 실행
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"업로드 진행: {progress}%")
            
            video_id = response['id']
            logger.info(f"비디오 업로드 완료! ID: {video_id}")
            logger.info(f"링크: https://www.youtube.com/watch?v={video_id}")
            
            # 썸네일 업로드 (선택)
            if thumbnail_path and os.path.exists(thumbnail_path):
                self.upload_thumbnail(video_id, thumbnail_path)
            
            return video_id
            
        except Exception as e:
            logger.error(f"비디오 업로드 실패: {e}")
            return None
    
    def upload_thumbnail(self, video_id: str, thumbnail_path: str) -> bool:
        """썸네일 업로드"""
        try:
            request = self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            )
            response = request.execute()
            logger.info(f"썸네일 업로드 완료: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"썸네일 업로드 실패: {e}")
            return False
    
    def generate_metadata(self, script_data: Dict) -> Dict:
        """
        스크립트 데이터로부터 업로드 메타데이터 생성
        
        Args:
            script_data: 스크립트 생성기의 출력
        
        Returns:
            업로드에 필요한 메타데이터
        """
        title = script_data.get('title', '경제 뉴스')
        
        # 설명 생성
        description = f"""
{script_data.get('script', '')}

#경제 #투자 #재테크 #경제뉴스 #shorts

━━━━━━━━━━━━━━━━━━━━

📊 더 많은 경제 정보가 궁금하다면?
👍 좋아요와 구독 부탁드립니다!
🔔 알림 설정하고 최신 소식을 받아보세요!

━━━━━━━━━━━━━━━━━━━━

⚠️ 본 콘텐츠는 정보 제공 목적이며, 투자 권유가 아닙니다.
   투자의 최종 책임은 투자자 본인에게 있습니다.

#경제사냥꾼 #shorts
"""
        
        # 태그
        tags = script_data.get('hashtags', [])
        tags.extend(self.youtube_config['default_tags'])
        tags = list(set(tags))[:15]  # 최대 15개
        
        return {
            'title': title[:100],  # 최대 100자
            'description': description[:5000],  # 최대 5000자
            'tags': tags,
            'category_id': self.youtube_config['category'],
            'privacy_status': self.youtube_config['visibility']
        }
    
    def upload_from_script(
        self,
        video_path: str,
        script_data: Dict,
        thumbnail_path: Optional[str] = None
    ) -> Optional[str]:
        """스크립트 데이터를 사용한 간편 업로드"""
        metadata = self.generate_metadata(script_data)
        
        return self.upload_video(
            video_path=video_path,
            title=metadata['title'],
            description=metadata['description'],
            tags=metadata['tags'],
            category_id=metadata['category_id'],
            privacy_status=metadata['privacy_status'],
            thumbnail_path=thumbnail_path
        )


# 테스트 코드
if __name__ == "__main__":
    logger.add("logs/youtube_uploader.log", rotation="1 day")
    
    # 테스트용 데이터
    test_script_data = {
        'title': '비트코인 10% 급등! 지금 무슨 일이?',
        'script': '비트코인이 하루만에 10% 넘게 급등했습니다. 현재 가격은 5천850만원을 돌파했는데요...',
        'hashtags': ['비트코인', '암호화폐', '투자', '급등']
    }
    
    print("=" * 60)
    print("유튜브 업로드 테스트")
    print("=" * 60)
    
    uploader = YouTubeUploader()
    
    # 메타데이터 생성 테스트
    metadata = uploader.generate_metadata(test_script_data)
    
    print(f"\n생성된 메타데이터:")
    print(f"제목: {metadata['title']}")
    print(f"태그: {', '.join(metadata['tags'])}")
    print(f"\n설명:\n{metadata['description'][:200]}...")
    
    print("\n⚠️ 실제 업로드를 하려면 다음이 필요합니다:")
    print("1. Google Cloud Console에서 OAuth 2.0 클라이언트 ID 생성")
    print("2. client_secrets.json 파일을 config/ 폴더에 저장")
    print("3. 비디오 파일 경로 지정")
