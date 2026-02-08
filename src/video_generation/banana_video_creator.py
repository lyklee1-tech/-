"""
Banana 모드 비디오 생성기 - AI 이미지 자동 생성 + 장면 분할 + 루프 지원
영상 길이: 20초 ~ 30분
"""
import os
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np
from moviepy.editor import (
    VideoFileClip, ImageClip, AudioFileClip, TextClip,
    CompositeVideoClip, concatenate_videoclips, ColorClip
)
from moviepy.video.fx.all import resize, fadein, fadeout, crop
import yaml
from loguru import logger
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO


class BananaVideoCreator:
    """Banana 스타일 비디오 생성기 - 완전 자동화"""
    
    def __init__(self, config_path='config/config.yaml'):
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            self.video_config = config['video']
            self.subtitle_config = config['subtitles']
            self.background_config = config['background']
            self.banana_config = config.get('banana_mode', {})
        
        # OpenAI API 초기화
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None
        
        # 해상도 설정
        width, height = map(int, self.video_config['resolution'].split('x'))
        self.width = width
        self.height = height
        self.fps = self.video_config['fps']
        
        logger.info("🍌 Banana 모드 비디오 생성기 초기화 완료")
    
    def create_banana_video(
        self,
        topic: str,
        script_text: str,
        audio_path: str,
        output_path: str,
        target_duration: Optional[int] = None,
        style: str = 'professional'
    ) -> bool:
        """
        Banana 스타일 비디오 생성 (AutoPilot 모드)
        
        Args:
            topic: 비디오 토픽/주제
            script_text: 전체 스크립트
            audio_path: TTS 오디오 경로
            output_path: 출력 비디오 경로
            target_duration: 목표 길이 (초, None이면 오디오 길이 사용)
            style: 스타일 템플릿 (professional, cinematic, anime, 3d)
        
        Returns:
            성공 여부
        """
        try:
            logger.info(f"🍌 Banana 모드 시작 - 토픽: {topic}")
            
            # 1. 오디오 로드
            narration = AudioFileClip(audio_path)
            audio_duration = narration.duration
            
            if target_duration is None:
                target_duration = int(audio_duration)
            
            logger.info(f"📏 목표 영상 길이: {target_duration}초 ({target_duration // 60}분 {target_duration % 60}초)")
            
            # 2. 스크립트 장면 분할
            scenes = self._segment_script(script_text, target_duration)
            logger.info(f"🎬 총 {len(scenes)}개 장면 생성")
            
            # 3. 각 장면별 AI 이미지 생성
            scene_clips = []
            for i, scene in enumerate(scenes):
                logger.info(f"🎨 장면 {i+1}/{len(scenes)} 이미지 생성 중...")
                scene_clip = self._create_scene_with_ai_image(
                    scene, topic, style
                )
                scene_clips.append(scene_clip)
            
            # 4. 장면 연결
            logger.info("🔗 장면 연결 중...")
            video = concatenate_videoclips(scene_clips, method="compose")
            
            # 5. 자막 추가
            logger.info("📝 자막 생성 중...")
            subtitles = self._create_subtitles(script_text, video.duration)
            
            # 6. 합성
            final_clips = [video] + subtitles
            
            # 7. 투자 책임 문구 추가
            if self.video_config.get('disclaimer', {}).get('enabled', True):
                disclaimer = self._create_disclaimer(video.duration)
                final_clips.append(disclaimer)
            
            final_video = CompositeVideoClip(final_clips, size=(self.width, self.height))
            
            # 8. 오디오 믹싱
            final_audio = self._mix_audio(narration, video.duration)
            final_video = final_video.set_audio(final_audio)
            
            # 9. 비디오 출력
            logger.info(f"💾 비디오 렌더링 중... ({output_path})")
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec=self.video_config['codec'],
                audio_codec=self.video_config['audio_codec'],
                preset='medium',
                threads=4,
                logger=None
            )
            
            # 리소스 정리
            final_video.close()
            for clip in scene_clips:
                clip.close()
            narration.close()
            
            logger.info(f"✅ Banana 모드 비디오 생성 완료: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Banana 모드 비디오 생성 실패: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def _segment_script(self, script: str, target_duration: int) -> List[Dict]:
        """
        스크립트를 장면별로 자동 분할
        
        Args:
            script: 전체 스크립트
            target_duration: 목표 영상 길이 (초)
        
        Returns:
            장면 리스트 [{'text': str, 'duration': float, 'description': str}, ...]
        """
        # 문장 단위로 분할
        sentences = [s.strip() for s in script.split('.') if s.strip()]
        
        # 장면 설정
        scene_config = self.banana_config.get('scene_segmentation', {})
        min_duration = scene_config.get('min_scene_duration', 3)
        max_duration = scene_config.get('max_scene_duration', 10)
        
        # 평균 장면 길이 계산
        num_scenes = max(1, len(sentences))
        avg_duration = target_duration / num_scenes
        
        # 장면 생성
        scenes = []
        for i, sentence in enumerate(sentences):
            # 각 장면의 길이를 균등하게 분배
            duration = min(max_duration, max(min_duration, avg_duration))
            
            scenes.append({
                'text': sentence,
                'duration': duration,
                'description': self._generate_scene_description(sentence),
                'index': i
            })
        
        return scenes
    
    def _generate_scene_description(self, text: str) -> str:
        """
        텍스트에서 AI 이미지 생성용 프롬프트 추출
        
        Args:
            text: 장면 텍스트
        
        Returns:
            이미지 생성 프롬프트
        """
        # 키워드 추출 (간단한 버전)
        keywords = {
            '비트코인': 'Bitcoin cryptocurrency chart',
            '주식': 'stock market trading floor',
            '경제': 'modern financial district',
            '투자': 'investment portfolio dashboard',
            '급등': 'rising green chart arrow',
            '급락': 'falling red chart',
            '환율': 'currency exchange rates',
            '금리': 'interest rate graph',
            '시장': 'bustling stock exchange',
            '기업': 'modern office building',
        }
        
        # 키워드 매칭
        for keyword, description in keywords.items():
            if keyword in text:
                return description
        
        # 기본 설명
        return 'professional business background with financial elements'
    
    def _create_scene_with_ai_image(
        self,
        scene: Dict,
        topic: str,
        style: str
    ) -> ImageClip:
        """
        AI 이미지로 장면 생성
        
        Args:
            scene: 장면 정보
            topic: 비디오 토픽
            style: 스타일 템플릿
        
        Returns:
            ImageClip
        """
        try:
            # AI 이미지 생성 설정
            ai_config = self.background_config.get('ai_image', {})
            
            if not ai_config.get('enabled', False) or not self.openai_client:
                # AI 생성 비활성화 시 기본 배경 사용
                logger.warning("⚠️ AI 이미지 생성 비활성화 - 기본 배경 사용")
                return self._create_default_background(scene['duration'])
            
            # 프롬프트 생성
            prompt_template = ai_config.get('prompt_template', '')
            prompt = prompt_template.format(
                style=style,
                description=scene['description']
            )
            
            logger.info(f"🎨 AI 이미지 생성 프롬프트: {prompt[:100]}...")
            
            # DALL-E 3로 이미지 생성 (OpenAI v1.0+ API)
            response = self.openai_client.images.generate(
                model=ai_config.get('model', 'dall-e-3'),
                prompt=prompt,
                size=ai_config.get('size', '1024x1792'),
                quality=ai_config.get('quality', 'hd'),
                style=ai_config.get('style', 'vivid'),
                n=1
            )
            
            # 이미지 다운로드
            image_url = response.data[0].url
            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))
            
            # 임시 저장
            temp_dir = Path('data/temp/ai_images')
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = int(time.time() * 1000)
            img_path = temp_dir / f"scene_{scene['index']}_{timestamp}.png"
            img.save(img_path)
            
            logger.info(f"✅ AI 이미지 생성 완료: {img_path}")
            
            # ImageClip 생성
            clip = ImageClip(str(img_path)).set_duration(scene['duration'])
            
            # Ken Burns 효과 (줌 애니메이션)
            anim_config = ai_config.get('animation', {})
            if anim_config.get('enabled', True):
                clip = self._apply_ken_burns_effect(
                    clip,
                    zoom_factor=anim_config.get('zoom_factor', 1.2)
                )
            
            # 화면 크기에 맞게 조정
            clip = clip.resize((self.width, self.height))
            
            return clip
            
        except Exception as e:
            logger.error(f"❌ AI 이미지 생성 실패: {e}")
            # 폴백: 기본 배경 사용
            return self._create_default_background(scene['duration'])
    
    def _create_default_background(self, duration: float) -> ColorClip:
        """기본 그라데이션 배경 생성"""
        gradient_colors = self.background_config.get('gradient', {}).get('colors', ['#0f2027', '#203a43', '#2c5364'])
        color = gradient_colors[0]
        return ColorClip(
            size=(self.width, self.height),
            color=self._hex_to_rgb(color)
        ).set_duration(duration)
    
    def _apply_ken_burns_effect(self, clip: ImageClip, zoom_factor: float = 1.2) -> ImageClip:
        """
        Ken Burns 효과 (줌 + 팬 애니메이션)
        
        Args:
            clip: 원본 클립
            zoom_factor: 줌 배율
        
        Returns:
            애니메이션 적용된 클립
        """
        def zoom(t):
            # 시간에 따라 줌 비율 증가
            progress = t / clip.duration
            current_zoom = 1 + (zoom_factor - 1) * progress
            return current_zoom
        
        return clip.resize(lambda t: zoom(t))
    
    def _create_subtitles(self, text: str, duration: float) -> List[TextClip]:
        """자막 생성 (단어 단위 애니메이션)"""
        subtitles = []
        words = text.split()
        
        if not words:
            return subtitles
        
        # 타이밍 계산
        words_per_second = self.subtitle_config['timing'].get('words_per_second', 3)
        word_duration = 1.0 / words_per_second
        
        # 자막 스타일
        font = self.subtitle_config.get('font', 'Arial-Bold')
        fontsize = self.subtitle_config.get('font_size', 60)
        color = self.subtitle_config.get('font_color', 'white')
        
        current_time = 0
        for i, word in enumerate(words):
            if current_time >= duration:
                break
            
            # 텍스트 클립 생성
            txt_clip = TextClip(
                word,
                fontsize=fontsize,
                font=font,
                color=color,
                stroke_color=self.subtitle_config.get('outline_color', 'black'),
                stroke_width=self.subtitle_config.get('outline_width', 3)
            ).set_position('center').set_start(current_time).set_duration(word_duration * 1.5)
            
            subtitles.append(txt_clip)
            current_time += word_duration
        
        return subtitles
    
    def _create_disclaimer(self, duration: float) -> TextClip:
        """투자 책임 문구 생성"""
        disclaimer_config = self.video_config.get('disclaimer', {})
        
        text = disclaimer_config.get('text', '본 영상은 투자 참고용이며\n투자 책임은 본인에게 있습니다')
        fontsize = disclaimer_config.get('fontsize', 24)
        color = disclaimer_config.get('color', '#cccccc')
        
        txt_clip = TextClip(
            text,
            fontsize=fontsize,
            font=self.subtitle_config.get('font', 'Arial-Bold'),
            color=color,
            method='caption',
            size=(self.width - 100, None),
            align='center'
        ).set_position(('center', self.height - 150)).set_duration(duration)
        
        return txt_clip
    
    def _mix_audio(self, narration: AudioFileClip, video_duration: float) -> AudioFileClip:
        """오디오 믹싱 (나레이션 + BGM + SFX)"""
        # 간단 버전: 나레이션만 반환
        # TODO: BGM 및 SFX 추가
        return narration
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """HEX 색상을 RGB 튜플로 변환"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_thumbnail(self, topic: str, output_path: str) -> bool:
        """
        AI 썸네일 자동 생성
        
        Args:
            topic: 비디오 토픽
            output_path: 썸네일 저장 경로
        
        Returns:
            성공 여부
        """
        try:
            thumbnail_config = self.banana_config.get('thumbnail_generation', {})
            
            if not thumbnail_config.get('enabled', False) or not self.openai_client:
                logger.warning("⚠️ AI 썸네일 생성 비활성화")
                return False
            
            # 썸네일 프롬프트 생성
            prompt = f"YouTube thumbnail for video about {topic}. Eye-catching, professional, high contrast, bold text overlay. 16:9 aspect ratio."
            
            logger.info(f"🎨 AI 썸네일 생성 중... (토픽: {topic})")
            
            # DALL-E 3로 썸네일 생성 (OpenAI v1.0+ API)
            response = self.openai_client.images.generate(
                model='dall-e-3',
                prompt=prompt,
                size='1792x1024',  # 16:9 비율
                quality='hd',
                n=1
            )
            
            # 이미지 다운로드 및 저장
            image_url = response.data[0].url
            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))
            
            # 썸네일 크기 조정 (YouTube 권장 크기)
            thumb_width = self.video_config['thumbnail']['width']
            thumb_height = self.video_config['thumbnail']['height']
            img = img.resize((thumb_width, thumb_height), Image.LANCZOS)
            
            img.save(output_path)
            
            logger.info(f"✅ AI 썸네일 생성 완료: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ AI 썸네일 생성 실패: {e}")
            return False
