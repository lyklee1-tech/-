"""
효과음 및 배경음악 관리 모듈
"""
import os
from pathlib import Path
from typing import Dict, List, Optional
import yaml
from loguru import logger
import random


class SoundEffectManager:
    """효과음 및 배경음악 관리자"""
    
    def __init__(self, config_path='config/config.yaml'):
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            self.audio_config = config['video']['audio']
        
        # 효과음 라이브러리 경로
        self.sfx_library = Path('data/audio/sfx')
        self.bgm_library = Path('data/audio/bgm')
        
        # 디렉토리 생성
        self.sfx_library.mkdir(parents=True, exist_ok=True)
        self.bgm_library.mkdir(parents=True, exist_ok=True)
        
        # 효과음 매핑 (파일명 또는 생성 프롬프트)
        self.sound_map = {
            # 인트로/아웃트로
            'whoosh': 'quick whoosh sound effect',
            'pop': 'short pop sound',
            'notification': 'notification ping sound',
            
            # 강조
            'impact': 'impact hit sound',
            'ding': 'pleasant ding sound',
            'alert': 'attention alert sound',
            
            # 트랜지션
            'swipe': 'smooth swipe transition',
            'slide': 'slide transition sound',
            'click': 'modern UI click',
            
            # 차트/데이터
            'reveal': 'data reveal whoosh',
            'growth': 'upward growth tone',
            'rising': 'rising pitch sound',
            'rising-tone': 'ascending musical tone',
            'falling-tone': 'descending musical tone',
            
            # 결론/완료
            'success': 'success completion sound',
            'complete': 'task complete chime',
            'finish': 'positive finish sound',
            'success-chime': 'success notification chime',
            
            # CTA
            'button': 'button press sound',
            'like': 'like button sound',
            'subscribe': 'subscribe bell sound',
            
            # 기타
            'beep': 'modern beep sound',
            'warning': 'warning alert',
            'tick': 'clock tick sound',
            'soft-click': 'soft subtle click'
        }
    
    def get_background_music(self, duration: float) -> Optional[str]:
        """
        배경음악 가져오기 또는 생성
        
        Args:
            duration: 필요한 음악 길이 (초)
        
        Returns:
            BGM 파일 경로
        """
        if not self.audio_config['background_music']['enabled']:
            return None
        
        bgm_config = self.audio_config['background_music']
        
        if bgm_config['source'] == 'file':
            # 파일에서 랜덤 선택
            bgm_path = Path(bgm_config['file_path'])
            if bgm_path.exists():
                bgm_files = list(bgm_path.glob('*.mp3')) + list(bgm_path.glob('*.wav'))
                if bgm_files:
                    selected = random.choice(bgm_files)
                    logger.info(f"배경음악 선택: {selected}")
                    return str(selected)
        
        # AI 생성
        logger.info(f"배경음악 AI 생성 (스타일: {bgm_config['style']}, {duration}초)")
        return self._generate_background_music(duration, bgm_config)
    
    def _generate_background_music(self, duration: float, config: Dict) -> Optional[str]:
        """AI로 배경음악 생성"""
        try:
            # ElevenLabs Music 또는 CassetteAI 사용
            from src.tts.tts_generator import TTSGenerator
            
            output_path = self.bgm_library / f'bgm_{int(duration)}s.mp3'
            
            # 이미 생성된 파일이 있으면 재사용
            if output_path.exists():
                logger.info(f"기존 BGM 재사용: {output_path}")
                return str(output_path)
            
            # 음악 생성 프롬프트
            style = config.get('style', 'corporate-minimal')
            mood = config.get('mood', 'professional')
            
            prompt = f"Background music for economic news video, {style} style, {mood} mood, "
            prompt += f"instrumental only, no vocals, modern and clean sound, {int(duration)} seconds"
            
            logger.info(f"BGM 생성 중... (프롬프트: {prompt[:100]}...)")
            
            # TODO: 실제 음악 생성 API 호출
            # 여기서는 플레이스홀더로 None 반환
            logger.warning("BGM 자동 생성은 API 키 설정 후 사용 가능합니다")
            return None
            
        except Exception as e:
            logger.error(f"BGM 생성 실패: {e}")
            return None
    
    def get_sound_effect(self, effect_name: str, timing: float = 0.0) -> Optional[Dict]:
        """
        효과음 가져오기 또는 생성
        
        Args:
            effect_name: 효과음 이름
            timing: 재생 시작 시점 (초)
        
        Returns:
            {'path': 파일경로, 'timing': 시작시점, 'volume': 볼륨}
        """
        if not self.audio_config['sound_effects']['enabled']:
            return None
        
        sfx_config = self.audio_config['sound_effects']
        
        # 효과음 파일 경로
        effect_file = self.sfx_library / f'{effect_name}.mp3'
        
        # 파일이 없으면 생성
        if not effect_file.exists():
            logger.info(f"효과음 '{effect_name}' 생성 중...")
            self._generate_sound_effect(effect_name, effect_file)
        
        if effect_file.exists():
            return {
                'path': str(effect_file),
                'timing': timing,
                'volume': sfx_config['volume']
            }
        
        return None
    
    def _generate_sound_effect(self, effect_name: str, output_path: Path) -> bool:
        """AI로 효과음 생성"""
        try:
            if effect_name not in self.sound_map:
                logger.warning(f"알 수 없는 효과음: {effect_name}")
                return False
            
            sfx_config = self.audio_config['sound_effects']
            
            if not sfx_config.get('auto_generate', {}).get('enabled', False):
                logger.info("효과음 자동 생성이 비활성화되어 있습니다")
                return False
            
            prompt = self.sound_map[effect_name]
            
            logger.info(f"효과음 생성: {effect_name} (프롬프트: {prompt})")
            
            # TODO: ElevenLabs Sound Effects API 사용
            # 또는 로컬 효과음 라이브러리 사용
            
            # 플레이스홀더: 간단한 사인파 생성 (테스트용)
            self._create_simple_tone(output_path, effect_name)
            
            return output_path.exists()
            
        except Exception as e:
            logger.error(f"효과음 생성 실패 ({effect_name}): {e}")
            return False
    
    def _create_simple_tone(self, output_path: Path, effect_name: str):
        """간단한 톤 생성 (테스트용 플레이스홀더)"""
        try:
            import numpy as np
            from scipy.io import wavfile
            
            # 효과음 타입별 주파수 설정
            tone_map = {
                'pop': (800, 0.1),
                'ding': (1200, 0.2),
                'beep': (600, 0.15),
                'rising-tone': (400, 0.3),
                'falling-tone': (1000, 0.3),
                'click': (2000, 0.05),
                'whoosh': (200, 0.3),
            }
            
            freq, duration = tone_map.get(effect_name, (800, 0.2))
            sample_rate = 44100
            
            t = np.linspace(0, duration, int(sample_rate * duration))
            
            if 'rising' in effect_name:
                # 상승 톤
                freq_array = np.linspace(freq, freq * 2, len(t))
                audio = np.sin(2 * np.pi * freq_array * t)
            elif 'falling' in effect_name:
                # 하강 톤
                freq_array = np.linspace(freq, freq / 2, len(t))
                audio = np.sin(2 * np.pi * freq_array * t)
            else:
                # 일반 톤
                audio = np.sin(2 * np.pi * freq * t)
            
            # 페이드 인/아웃
            fade_samples = int(sample_rate * 0.01)
            audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
            audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            # 정규화
            audio = (audio * 32767).astype(np.int16)
            
            # WAV로 저장
            wav_path = output_path.with_suffix('.wav')
            wavfile.write(str(wav_path), sample_rate, audio)
            
            # MP3로 변환 (ffmpeg 필요)
            try:
                import subprocess
                subprocess.run([
                    'ffmpeg', '-i', str(wav_path), '-y',
                    '-acodec', 'libmp3lame', '-b:a', '128k',
                    str(output_path)
                ], check=True, capture_output=True)
                wav_path.unlink()  # WAV 파일 삭제
            except:
                # ffmpeg 실패 시 WAV 파일 유지
                logger.warning(f"MP3 변환 실패, WAV 파일 사용: {wav_path}")
            
            logger.info(f"테스트 효과음 생성: {output_path}")
            
        except Exception as e:
            logger.error(f"톤 생성 실패: {e}")
    
    def get_script_sfx_timings(self, script: str, duration: float) -> List[Dict]:
        """
        스크립트 분석하여 효과음 타이밍 자동 결정
        
        Args:
            script: 스크립트 텍스트
            duration: 비디오 길이
        
        Returns:
            효과음 리스트 [{'effect': 이름, 'timing': 시점}]
        """
        sfx_config = self.audio_config['sound_effects']
        timing_config = sfx_config.get('timing', {})
        
        sfx_list = []
        
        # 인트로 효과음
        if timing_config.get('intro', {}).get('enabled', True):
            sfx_list.append({
                'effect': timing_config['intro']['sound'],
                'timing': 0.0
            })
        
        # 후킹 멘트 (약 3초 지점)
        if timing_config.get('hook', {}).get('enabled', True):
            sfx_list.append({
                'effect': timing_config['hook']['sound'],
                'timing': 2.5
            })
        
        # 핵심 포인트 (중간 지점들)
        if timing_config.get('key_point', {}).get('enabled', True):
            # 스크립트에서 숫자나 강조 표현 찾기
            import re
            numbers = re.findall(r'\d+(?:\.\d+)?[%원만억조]', script)
            if numbers:
                # 중간 지점에 효과음 배치
                mid_timing = duration * 0.4
                sfx_list.append({
                    'effect': timing_config['key_point']['sound'],
                    'timing': mid_timing
                })
        
        # 차트 등장 (40% 지점)
        if timing_config.get('chart_reveal', {}).get('enabled', True):
            sfx_list.append({
                'effect': timing_config['chart_reveal']['sound'],
                'timing': duration * 0.4
            })
        
        # 결론 (70% 지점)
        if timing_config.get('conclusion', {}).get('enabled', True):
            sfx_list.append({
                'effect': timing_config['conclusion']['sound'],
                'timing': duration * 0.7
            })
        
        # CTA (90% 지점)
        if timing_config.get('cta', {}).get('enabled', True):
            if '구독' in script or '좋아요' in script:
                sfx_list.append({
                    'effect': timing_config['cta']['sound'],
                    'timing': duration * 0.9
                })
        
        logger.info(f"{len(sfx_list)}개 효과음 타이밍 생성")
        return sfx_list
    
    def get_event_sound(self, event_type: str) -> Optional[str]:
        """
        이벤트 타입에 따른 효과음 가져오기
        
        Args:
            event_type: 이벤트 타입 (price_up, price_down, alert 등)
        
        Returns:
            효과음 이름
        """
        events_config = self.audio_config['sound_effects'].get('events', {})
        return events_config.get(event_type)


# 테스트 코드
if __name__ == "__main__":
    logger.add("logs/sound_effects.log", rotation="1 day")
    
    manager = SoundEffectManager()
    
    print("=" * 60)
    print("효과음 관리 시스템 테스트")
    print("=" * 60)
    
    # 효과음 생성 테스트
    print("\n1. 효과음 생성 테스트")
    effects = ['pop', 'ding', 'rising-tone', 'falling-tone']
    for effect in effects:
        sfx = manager.get_sound_effect(effect, timing=0.0)
        if sfx:
            print(f"  ✓ {effect}: {sfx['path']}")
    
    # 스크립트 기반 타이밍 생성
    print("\n2. 스크립트 분석 테스트")
    test_script = "비트코인이 10% 급등했습니다! 현재 가격은 5천850만원입니다. 구독과 좋아요 부탁드립니다."
    timings = manager.get_script_sfx_timings(test_script, 60)
    for sfx in timings:
        print(f"  {sfx['timing']:.1f}초: {sfx['effect']}")
    
    # 이벤트 사운드
    print("\n3. 이벤트 사운드 테스트")
    events = ['price_up', 'price_down', 'alert', 'positive']
    for event in events:
        sound = manager.get_event_sound(event)
        print(f"  {event}: {sound}")
    
    print("\n✅ 테스트 완료!")
