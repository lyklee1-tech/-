"""
캐릭터 일관성 관리 시스템
한 번 생성된 캐릭터를 계속 일관성 있게 유지
"""
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
from loguru import logger


class CharacterManager:
    """캐릭터 일관성 관리 클래스"""
    
    def __init__(self, storage_dir: str = 'data/characters'):
        """
        초기화
        
        Args:
            storage_dir: 캐릭터 데이터 저장 디렉토리
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.characters_file = self.storage_dir / 'characters.json'
        
        # 캐릭터 데이터 로드
        self.characters = self._load_characters()
        
        logger.info(f"캐릭터 관리자 초기화 완료: {len(self.characters)}개 캐릭터 로드됨")
    
    def _load_characters(self) -> Dict:
        """저장된 캐릭터 데이터 로드"""
        if self.characters_file.exists():
            try:
                with open(self.characters_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"캐릭터 데이터 로드 실패: {e}")
                return {}
        return {}
    
    def _save_characters(self):
        """캐릭터 데이터 저장"""
        try:
            with open(self.characters_file, 'w', encoding='utf-8') as f:
                json.dump(self.characters, f, ensure_ascii=False, indent=2)
            logger.info("캐릭터 데이터 저장 완료")
        except Exception as e:
            logger.error(f"캐릭터 데이터 저장 실패: {e}")
    
    def create_character(self, 
                        user_id: str, 
                        character_name: str,
                        style: str = 'professional',
                        voice: str = 'male_young',
                        appearance_prompt: Optional[str] = None,
                        character_image: Optional[str] = None) -> Dict:
        """
        새 캐릭터 생성
        
        Args:
            user_id: 사용자 ID (세션 ID 등)
            character_name: 캐릭터 이름
            style: 비디오 스타일
            voice: 목소리 프리셋
            appearance_prompt: 외모 프롬프트 (GenSpark AI용)
            character_image: 캐릭터 이미지 경로 (업로드된 경우)
        
        Returns:
            생성된 캐릭터 정보
        """
        character_id = f"{user_id}_{character_name}_{int(datetime.now().timestamp())}"
        
        # 이미지가 있으면 이미지 기반, 없으면 텍스트 기반 프롬프트
        if character_image:
            # 이미지 기반 일관성
            appearance_prompt = f"Character from reference image, maintaining exact appearance and features, {style} style"
        elif not appearance_prompt:
            # 기본 외모 프롬프트 생성
            appearance_prompt = self._generate_appearance_prompt(style, character_name)
        
        character_data = {
            'character_id': character_id,
            'user_id': user_id,
            'character_name': character_name,
            'style': style,
            'voice': voice,
            'appearance_prompt': appearance_prompt,
            'character_image': character_image,  # 이미지 경로 저장
            'created_at': datetime.now().isoformat(),
            'last_used': datetime.now().isoformat(),
            'usage_count': 0,
            'videos': []  # 이 캐릭터로 생성한 비디오 목록
        }
        
        self.characters[character_id] = character_data
        self._save_characters()
        
        logger.info(f"새 캐릭터 생성: {character_name} (ID: {character_id}, 이미지: {bool(character_image)})")
        return character_data
    
    def get_character(self, character_id: str) -> Optional[Dict]:
        """캐릭터 정보 가져오기"""
        return self.characters.get(character_id)
    
    def get_user_characters(self, user_id: str) -> list:
        """사용자의 모든 캐릭터 가져오기"""
        return [
            char for char in self.characters.values()
            if char['user_id'] == user_id
        ]
    
    def update_character_usage(self, character_id: str, video_info: Dict):
        """캐릭터 사용 기록 업데이트"""
        if character_id in self.characters:
            character = self.characters[character_id]
            character['last_used'] = datetime.now().isoformat()
            character['usage_count'] += 1
            character['videos'].append({
                'timestamp': datetime.now().isoformat(),
                'topic': video_info.get('topic'),
                'video_path': video_info.get('video_path')
            })
            self._save_characters()
            logger.info(f"캐릭터 사용 기록 업데이트: {character_id}")
    
    def get_consistent_prompt(self, character_id: str, scene_description: str) -> str:
        """
        일관된 캐릭터로 장면 프롬프트 생성
        
        Args:
            character_id: 캐릭터 ID
            scene_description: 장면 설명
        
        Returns:
            일관성 있는 프롬프트
        """
        character = self.get_character(character_id)
        
        if not character:
            logger.warning(f"캐릭터를 찾을 수 없음: {character_id}")
            return scene_description
        
        # 캐릭터 외모 + 장면 설명 결합
        consistent_prompt = f"{character['appearance_prompt']}, {scene_description}"
        
        # 일관성 키워드 추가
        consistent_prompt += ", consistent character, same person, character continuity, maintaining appearance"
        
        return consistent_prompt
    
    def _generate_appearance_prompt(self, style: str, character_name: str) -> str:
        """
        스타일에 맞는 기본 외모 프롬프트 생성
        
        Args:
            style: 비디오 스타일
            character_name: 캐릭터 이름
        
        Returns:
            외모 프롬프트
        """
        # 스타일별 기본 외모
        style_prompts = {
            'professional': 'Professional business person in formal suit, confident expression, modern office background',
            'stickman': 'Simple stick figure character with expressive poses, minimalist design',
            'japanese_anime': 'Anime character with big eyes, colorful hair, manga style illustration',
            'cinematic': 'Cinematic character with dramatic lighting, professional actor appearance',
            '3d': '3D rendered character, realistic textures, modern CGI style',
            'documentary': 'Real person documentary style, natural lighting, authentic appearance',
            'performance_metrics': 'Business analyst with charts and graphs, professional attire',
            'office_scene': 'Office worker in business casual, desk environment, professional setting'
        }
        
        base_prompt = style_prompts.get(style, 'Professional character')
        
        # 이름 기반 특성 추가
        if '남' in character_name or 'male' in character_name.lower():
            base_prompt += ', male character'
        elif '여' in character_name or 'female' in character_name.lower():
            base_prompt += ', female character'
        
        return base_prompt
    
    def delete_character(self, character_id: str) -> bool:
        """캐릭터 삭제"""
        if character_id in self.characters:
            del self.characters[character_id]
            self._save_characters()
            logger.info(f"캐릭터 삭제: {character_id}")
            return True
        return False
    
    def get_character_stats(self, character_id: str) -> Optional[Dict]:
        """캐릭터 통계 정보"""
        character = self.get_character(character_id)
        if not character:
            return None
        
        return {
            'character_name': character['character_name'],
            'usage_count': character['usage_count'],
            'created_at': character['created_at'],
            'last_used': character['last_used'],
            'total_videos': len(character['videos']),
            'style': character['style'],
            'voice': character['voice']
        }


def main():
    """테스트 실행"""
    manager = CharacterManager()
    
    # 테스트 캐릭터 생성
    character = manager.create_character(
        user_id='test_user_001',
        character_name='경제 앵커',
        style='professional',
        voice='female_professional'
    )
    
    print(f"✅ 캐릭터 생성: {character['character_name']}")
    print(f"   ID: {character['character_id']}")
    print(f"   외모: {character['appearance_prompt']}")
    
    # 일관성 있는 프롬프트 생성
    scene_prompt = manager.get_consistent_prompt(
        character['character_id'],
        "discussing stock market trends with charts in background"
    )
    
    print(f"\n일관성 프롬프트:")
    print(f"   {scene_prompt}")
    
    # 사용 기록 업데이트
    manager.update_character_usage(
        character['character_id'],
        {'topic': '비트코인 급등', 'video_path': 'test.mp4'}
    )
    
    # 통계 조회
    stats = manager.get_character_stats(character['character_id'])
    print(f"\n캐릭터 통계:")
    print(f"   사용 횟수: {stats['usage_count']}")
    print(f"   비디오 수: {stats['total_videos']}")


if __name__ == '__main__':
    main()
