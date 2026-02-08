"""
비디오 생성 모듈 - Shorts 영상 자동 제작
"""
import os
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np
from moviepy.editor import (
    VideoFileClip, ImageClip, AudioFileClip, TextClip,
    CompositeVideoClip, concatenate_videoclips, ColorClip
)
from moviepy.video.fx.all import resize, fadein, fadeout
from PIL import Image, ImageDraw, ImageFont
import yaml
from loguru import logger


class VideoCreator:
    """유튜브 Shorts 비디오 생성기"""
    
    def __init__(self, config_path='config/config.yaml'):
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            self.video_config = config['video']
            self.subtitle_config = config['subtitles']
            self.background_config = config['background']
        
        # 해상도 파싱 (1080x1920)
        width, height = map(int, self.video_config['resolution'].split('x'))
        self.width = width
        self.height = height
        self.fps = self.video_config['fps']
    
    def create_shorts_video(
        self,
        audio_path: str,
        script_text: str,
        output_path: str,
        background_type: str = 'gradient',
        title_text: Optional[str] = None,
        chart_image: Optional[str] = None,
        show_disclaimer: bool = True,
        add_sound_effects: bool = True
    ) -> bool:
        """
        Shorts 비디오 생성
        
        Args:
            audio_path: 오디오 파일 경로
            script_text: 자막으로 표시할 스크립트
            output_path: 출력 비디오 경로
            background_type: 배경 타입 (gradient, image, video)
            title_text: 제목 텍스트
            chart_image: 차트 이미지 경로 (선택)
            show_disclaimer: 투자 책임 문구 표시 여부 (기본: True)
            add_sound_effects: 효과음 및 배경음악 추가 여부 (기본: True)
        
        Returns:
            성공 여부
        """
        try:
            # 1. 오디오 로드 (나레이션)
            narration = AudioFileClip(audio_path)
            duration = narration.duration
            
            logger.info(f"비디오 생성 시작 (길이: {duration:.2f}초)")
            
            # 2. 배경 생성
            background = self._create_background(duration, background_type)
            
            # 3. 자막 생성
            subtitles = self._create_subtitles(script_text, duration)
            
            # 4. 제목 추가 (선택)
            clips = [background]
            
            if title_text:
                title = self._create_title(title_text, duration)
                clips.append(title)
            
            # 5. 차트 추가 (선택)
            if chart_image and os.path.exists(chart_image):
                chart = self._add_chart_image(chart_image, duration)
                clips.append(chart)
            
            # 6. 자막 추가
            clips.extend(subtitles)
            
            # 7. 투자 책임 문구 추가
            disclaimer_enabled = self.video_config.get('disclaimer', {}).get('enabled', True)
            if show_disclaimer and disclaimer_enabled:
                disclaimer = self._create_disclaimer(duration)
                clips.append(disclaimer)
            
            # 8. 합성
            final_video = CompositeVideoClip(clips, size=(self.width, self.height))
            
            # 9. 오디오 믹싱 (나레이션 + 배경음악 + 효과음)
            final_audio = self._mix_audio(
                narration, 
                duration, 
                script_text, 
                add_sound_effects
            )
            
            final_video = final_video.set_audio(final_audio)
            final_video = final_video.set_duration(duration)
            
            # 10. 출력
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec=self.video_config['codec'],
                audio_codec=self.video_config['audio_codec'],
                threads=4,
                preset='medium'
            )
            
            logger.info(f"비디오 생성 완료: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"비디오 생성 실패: {e}")
            return False
    
    def _mix_audio(
        self,
        narration: AudioFileClip,
        duration: float,
        script_text: str,
        add_sfx: bool = True
    ) -> AudioFileClip:
        """
        나레이션, 배경음악, 효과음 믹싱
        
        Args:
            narration: 나레이션 오디오
            duration: 비디오 길이
            script_text: 스크립트 (효과음 타이밍 판단용)
            add_sfx: 효과음 추가 여부
        
        Returns:
            믹싱된 최종 오디오
        """
        try:
            from src.video_generation.sound_effects import SoundEffectManager
            from moviepy.editor import CompositeAudioClip
            
            audio_clips = [narration]
            
            if not add_sfx:
                return narration
            
            sfx_manager = SoundEffectManager()
            
            # 1. 배경음악 추가
            bgm_path = sfx_manager.get_background_music(duration)
            if bgm_path and os.path.exists(bgm_path):
                bgm = AudioFileClip(bgm_path)
                
                # 길이 조정
                if bgm.duration < duration:
                    # 루프
                    bgm = bgm.audio_loop(duration=duration)
                elif bgm.duration > duration:
                    # 자르기
                    bgm = bgm.subclip(0, duration)
                
                # 볼륨 조정
                bgm_config = self.video_config['audio']['background_music']
                bgm = bgm.volumex(bgm_config['volume'])
                
                # 페이드 인/아웃
                bgm = bgm.audio_fadein(bgm_config['fade_in'])
                bgm = bgm.audio_fadeout(bgm_config['fade_out'])
                
                audio_clips.append(bgm)
                logger.info("배경음악 추가 완료")
            
            # 2. 효과음 추가
            sfx_timings = sfx_manager.get_script_sfx_timings(script_text, duration)
            
            for sfx_info in sfx_timings:
                sfx = sfx_manager.get_sound_effect(
                    sfx_info['effect'],
                    sfx_info['timing']
                )
                
                if sfx and os.path.exists(sfx['path']):
                    sfx_clip = AudioFileClip(sfx['path'])
                    sfx_clip = sfx_clip.volumex(sfx['volume'])
                    sfx_clip = sfx_clip.set_start(sfx['timing'])
                    audio_clips.append(sfx_clip)
            
            if len(audio_clips) > 1:
                logger.info(f"오디오 믹싱: 나레이션 + BGM + {len(sfx_timings)}개 효과음")
                return CompositeAudioClip(audio_clips)
            else:
                return narration
                
        except Exception as e:
            logger.error(f"오디오 믹싱 실패: {e}, 나레이션만 사용")
            return narration
    
    def _create_background(self, duration: float, bg_type: str = 'gradient') -> ColorClip:
        """배경 생성"""
        if bg_type == 'gradient':
            # 그라데이션 배경
            colors = self.background_config['gradient']['colors']
            # 간단한 그라데이션 (실제로는 더 복잡한 구현 필요)
            color = tuple(int(colors[0][i:i+2], 16) for i in (1, 3, 5))
            bg = ColorClip(size=(self.width, self.height), color=color, duration=duration)
            
        elif bg_type == 'image':
            # 이미지 배경
            bg = ColorClip(size=(self.width, self.height), color=(26, 26, 46), duration=duration)
            
        else:  # 기본: 단색
            bg = ColorClip(size=(self.width, self.height), color=(26, 26, 46), duration=duration)
        
        return bg
    
    def _create_subtitles(self, text: str, duration: float) -> List[TextClip]:
        """자막 생성 (단어별 애니메이션)"""
        subtitles = []
        
        # 문장 분할
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # 각 문장의 표시 시간 계산
        time_per_sentence = duration / len(sentences) if sentences else duration
        
        for i, sentence in enumerate(sentences):
            if not sentence:
                continue
            
            start_time = i * time_per_sentence
            end_time = start_time + time_per_sentence
            
            # 텍스트 클립 생성
            txt_clip = TextClip(
                sentence,
                fontsize=self.subtitle_config['font_size'],
                color=self.subtitle_config['font_color'],
                font='NanumGothic-Bold',  # 한글 폰트
                method='caption',
                size=(self.width - 100, None),
                align='center'
            )
            
            # 위치 설정 (중앙)
            txt_clip = txt_clip.set_position(('center', 'center'))
            txt_clip = txt_clip.set_start(start_time)
            txt_clip = txt_clip.set_duration(end_time - start_time)
            
            # 페이드 효과
            txt_clip = fadein(txt_clip, 0.3)
            txt_clip = fadeout(txt_clip, 0.3)
            
            subtitles.append(txt_clip)
        
        logger.info(f"{len(subtitles)}개 자막 생성")
        return subtitles
    
    def _create_title(self, title_text: str, duration: float) -> TextClip:
        """제목 텍스트 생성"""
        title = TextClip(
            title_text,
            fontsize=70,
            color='white',
            font='NanumGothic-Bold',
            method='caption',
            size=(self.width - 100, None),
            align='center',
            bg_color='rgba(0,0,0,0.5)'
        )
        
        # 상단에 배치
        title = title.set_position(('center', 100))
        title = title.set_duration(min(5, duration))  # 처음 5초만 표시
        title = fadein(title, 0.5)
        title = fadeout(title, 0.5)
        
        return title
    
    def _add_chart_image(self, chart_path: str, duration: float) -> ImageClip:
        """차트 이미지 추가"""
        chart = ImageClip(chart_path)
        
        # 크기 조정 (화면의 60% 크기)
        chart = resize(chart, width=int(self.width * 0.6))
        
        # 하단 중앙에 배치
        chart = chart.set_position(('center', int(self.height * 0.6)))
        chart = chart.set_duration(duration)
        
        # 3초 후에 나타나서 끝까지 표시
        chart = chart.set_start(3)
        chart = fadein(chart, 0.5)
        
        return chart
    
    def _create_disclaimer(self, duration: float) -> TextClip:
        """투자 책임 문구 생성 (하단 고정)"""
        # config에서 설정 읽기
        disclaimer_config = self.video_config.get('disclaimer', {})
        
        disclaimer_text = disclaimer_config.get(
            'text',
            "본 영상은 투자 참고용이며\n투자 책임은 본인에게 있습니다"
        )
        
        fontsize = disclaimer_config.get('fontsize', 24)
        color = disclaimer_config.get('color', '#cccccc')
        bg_color = disclaimer_config.get('bg_color', 'rgba(0,0,0,0.7)')
        margin = disclaimer_config.get('margin', 40)
        
        disclaimer = TextClip(
            disclaimer_text,
            fontsize=fontsize,
            color=color,
            font='NanumGothic-Bold',
            method='caption',
            size=(self.width - 80, None),
            align='center',
            bg_color=bg_color
        )
        
        # 하단에 고정 배치
        disclaimer = disclaimer.set_position(('center', self.height - disclaimer.h - margin))
        disclaimer = disclaimer.set_duration(duration)
        
        # 처음과 끝에 페이드 효과
        disclaimer = fadein(disclaimer, 0.5)
        disclaimer = fadeout(disclaimer, 0.5)
        
        logger.info("투자 책임 문구 추가")
        return disclaimer
    
    def create_thumbnail(self, text: str, output_path: str) -> bool:
        """썸네일 이미지 생성"""
        try:
            # 이미지 생성
            img = Image.new('RGB', (1280, 720), color='#1a1a2e')
            draw = ImageDraw.Draw(img)
            
            # 폰트 (시스템에 따라 경로 조정 필요)
            try:
                font = ImageFont.truetype('/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf', 80)
            except:
                font = ImageFont.load_default()
            
            # 텍스트 중앙 배치
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            position = ((1280 - text_width) // 2, (720 - text_height) // 2)
            
            # 텍스트 그리기 (테두리 효과)
            for adj in range(-3, 4):
                for adj2 in range(-3, 4):
                    draw.text((position[0]+adj, position[1]+adj2), text, font=font, fill='black')
            
            draw.text(position, text, font=font, fill='#eef2f7')
            
            # 저장
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path, quality=95)
            
            logger.info(f"썸네일 생성 완료: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"썸네일 생성 실패: {e}")
            return False


# 테스트 코드
if __name__ == "__main__":
    logger.add("logs/video_creator.log", rotation="1 day")
    
    creator = VideoCreator()
    
    # 테스트용 더미 데이터
    test_audio = "data/audio/test_output.mp3"
    test_script = "비트코인이 하루만에 10% 급등했습니다. 현재 가격은 5천850만원입니다. 미국 ETF 자금이 대규모 유입되고 있습니다."
    output_video = "data/videos/test_shorts.mp4"
    
    if os.path.exists(test_audio):
        print("비디오 생성 테스트 시작...")
        success = creator.create_shorts_video(
            audio_path=test_audio,
            script_text=test_script,
            output_path=output_video,
            title_text="비트코인 10% 급등"
        )
        
        if success:
            print(f"✅ 비디오 생성 완료: {output_video}")
        else:
            print("❌ 비디오 생성 실패")
    else:
        print(f"오디오 파일이 없습니다: {test_audio}")
