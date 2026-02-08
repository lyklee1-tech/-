"""
TTS (Text-to-Speech) 음성 생성 모듈
"""
import os
from pathlib import Path
from typing import Optional
from loguru import logger
import yaml

# Google Cloud TTS
try:
    from google.cloud import texttospeech
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False
    logger.warning("Google Cloud TTS not available")

# ElevenLabs TTS
try:
    from elevenlabs import generate, save, voices, set_api_key
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    logger.warning("ElevenLabs TTS not available")

# Fallback: gTTS
from gtts import gTTS


class TTSGenerator:
    """다중 TTS 엔진을 지원하는 음성 생성기"""
    
    def __init__(self, config_path='config/config.yaml'):
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            self.tts_config = config['tts']
        
        self.provider = self.tts_config.get('provider', 'google')
        
        # API 키 설정
        if self.provider == 'elevenlabs' and ELEVENLABS_AVAILABLE:
            api_key = os.getenv('ELEVENLABS_API_KEY')
            if api_key:
                set_api_key(api_key)
    
    def generate_audio(self, text: str, output_path: str, provider: Optional[str] = None) -> bool:
        """
        텍스트를 음성으로 변환
        
        Args:
            text: 변환할 텍스트
            output_path: 저장 경로
            provider: TTS 제공자 (None이면 기본 설정 사용)
        
        Returns:
            성공 여부
        """
        provider = provider or self.provider
        
        # 출력 디렉토리 생성
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if provider == 'google' and GOOGLE_TTS_AVAILABLE:
                return self._generate_google_tts(text, output_path)
            
            elif provider == 'elevenlabs' and ELEVENLABS_AVAILABLE:
                return self._generate_elevenlabs_tts(text, output_path)
            
            else:
                # Fallback to gTTS
                logger.warning(f"{provider} 사용 불가, gTTS로 대체")
                return self._generate_gtts(text, output_path)
        
        except Exception as e:
            logger.error(f"TTS 생성 실패 ({provider}): {e}")
            # Fallback to gTTS
            try:
                return self._generate_gtts(text, output_path)
            except Exception as e2:
                logger.error(f"gTTS 생성도 실패: {e2}")
                return False
    
    def _generate_google_tts(self, text: str, output_path: str) -> bool:
        """Google Cloud TTS로 음성 생성"""
        try:
            client = texttospeech.TextToSpeechClient()
            
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=self.tts_config['language'],
                name=self.tts_config['voice']
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=self.tts_config['speed'],
                pitch=self.tts_config['pitch']
            )
            
            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            with open(output_path, 'wb') as out:
                out.write(response.audio_content)
            
            logger.info(f"Google TTS 생성 완료: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Google TTS 실패: {e}")
            return False
    
    def _generate_elevenlabs_tts(self, text: str, output_path: str) -> bool:
        """ElevenLabs TTS로 음성 생성 (고품질)"""
        try:
            config = self.tts_config.get('elevenlabs', {})
            
            audio = generate(
                text=text,
                voice=config.get('voice_id', 'EXAVITQu4vr4xnSDxMaL'),
                model=config.get('model', 'eleven_multilingual_v2')
            )
            
            save(audio, output_path)
            
            logger.info(f"ElevenLabs TTS 생성 완료: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"ElevenLabs TTS 실패: {e}")
            return False
    
    def _generate_gtts(self, text: str, output_path: str) -> bool:
        """gTTS로 음성 생성 (무료, 기본)"""
        try:
            tts = gTTS(
                text=text,
                lang='ko',
                slow=False
            )
            tts.save(output_path)
            
            logger.info(f"gTTS 생성 완료: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"gTTS 실패: {e}")
            return False
    
    def generate_with_timing(self, script_segments: list, output_dir: str) -> list:
        """
        스크립트 세그먼트별로 음성 생성하고 타이밍 정보 반환
        
        Args:
            script_segments: [{"text": "문장1", "start": 0}, ...]
            output_dir: 출력 디렉토리
        
        Returns:
            타이밍 정보가 포함된 오디오 파일 리스트
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        audio_files = []
        
        for i, segment in enumerate(script_segments):
            output_path = os.path.join(output_dir, f"segment_{i:03d}.mp3")
            
            if self.generate_audio(segment['text'], output_path):
                audio_files.append({
                    'file': output_path,
                    'text': segment['text'],
                    'start': segment.get('start', i),
                    'index': i
                })
        
        logger.info(f"{len(audio_files)}개 오디오 세그먼트 생성 완료")
        return audio_files


# 테스트 코드
if __name__ == "__main__":
    logger.add("logs/tts_generator.log", rotation="1 day")
    
    generator = TTSGenerator()
    
    test_text = """
    여러분, 비트코인이 하루 만에 10% 넘게 급등했습니다.
    현재 가격은 5천 8백 50만원을 돌파했는데요.
    미국 현물 ETF 자금이 대규모로 유입되면서 시장이 들썩이고 있습니다.
    이 추세가 계속될까요? 구독과 좋아요로 다음 소식도 받아보세요!
    """
    
    output_path = "data/audio/test_output.mp3"
    
    print("TTS 음성 생성 테스트...")
    success = generator.generate_audio(test_text, output_path)
    
    if success:
        print(f"✅ 음성 파일 생성 완료: {output_path}")
        
        # 파일 크기 확인
        size = Path(output_path).stat().st_size / 1024
        print(f"   파일 크기: {size:.2f} KB")
    else:
        print("❌ 음성 생성 실패")
