#!/usr/bin/env python3
"""
음악 파일 업로드 도우미 스크립트

Windows 로컬 폴더의 음악 파일을 서버로 복사하는 방법을 안내합니다.
"""

import os
import sys
from pathlib import Path
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("logs/audio_upload.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AudioUploadHelper:
    """음악 파일 업로드 도우미"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.bgm_dir = self.project_root / "data" / "audio" / "bgm"
        self.sfx_dir = self.project_root / "data" / "audio" / "sfx"
        
    def check_directories(self):
        """디렉토리 확인"""
        print("=" * 70)
        print("🎵 음악 파일 업로드 도우미")
        print("=" * 70)
        print()
        
        print("📁 프로젝트 구조 확인:")
        print(f"  프로젝트 루트: {self.project_root}")
        print(f"  BGM 디렉토리: {self.bgm_dir} {'✅' if self.bgm_dir.exists() else '❌ (없음)'}")
        print(f"  SFX 디렉토리: {self.sfx_dir} {'✅' if self.sfx_dir.exists() else '❌ (없음)'}")
        print()
        
        # 디렉토리 생성
        if not self.bgm_dir.exists():
            self.bgm_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"BGM 디렉토리 생성: {self.bgm_dir}")
        
        if not self.sfx_dir.exists():
            self.sfx_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"SFX 디렉토리 생성: {self.sfx_dir}")
            
        # SFX 카테고리 폴더 생성
        sfx_categories = ['intro', 'hook', 'key_point', 'chart_reveal', 'conclusion', 'cta', 'outro', 'events']
        for category in sfx_categories:
            cat_dir = self.sfx_dir / category
            if not cat_dir.exists():
                cat_dir.mkdir(exist_ok=True)
                logger.info(f"SFX 카테고리 생성: {category}")
    
    def scan_existing_files(self):
        """현재 업로드된 파일 스캔"""
        print("📂 현재 업로드된 파일:")
        print()
        
        # BGM 파일
        print("  [배경음악 (BGM)]")
        bgm_files = list(self.bgm_dir.glob('*.mp3')) + list(self.bgm_dir.glob('*.wav'))
        if bgm_files:
            for f in bgm_files:
                size = f.stat().st_size / 1024 / 1024  # MB
                print(f"    ✓ {f.name} ({size:.1f} MB)")
        else:
            print("    ❌ BGM 파일 없음")
        
        print()
        
        # SFX 파일 (카테고리별)
        print("  [효과음 (SFX)]")
        sfx_categories = ['intro', 'hook', 'key_point', 'chart_reveal', 'conclusion', 'cta', 'outro', 'events']
        total_sfx = 0
        
        for category in sfx_categories:
            cat_dir = self.sfx_dir / category
            if cat_dir.exists():
                sfx_files = list(cat_dir.glob('*.mp3')) + list(cat_dir.glob('*.wav'))
                if sfx_files:
                    print(f"\n    [{category}]")
                    for f in sfx_files:
                        size = f.stat().st_size / 1024  # KB
                        print(f"      ✓ {f.name} ({size:.0f} KB)")
                        total_sfx += 1
        
        if total_sfx == 0:
            print("    ❌ 효과음 파일 없음")
        
        print()
        print(f"총 {len(bgm_files)}개 BGM, {total_sfx}개 효과음 파일")
        print()
    
    def show_upload_instructions(self):
        """업로드 방법 안내"""
        print("=" * 70)
        print("📤 파일 업로드 방법")
        print("=" * 70)
        print()
        
        print("Windows 로컬 폴더:")
        print("  C:\\Users\\user\\Desktop\\economic_shorts\\assets\\audio\\")
        print("    ├── bgm/       (배경음악)")
        print("    └── sfx/       (효과음)")
        print()
        
        print("서버 대상 폴더:")
        print(f"  {self.bgm_dir.absolute()}")
        print(f"  {self.sfx_dir.absolute()}")
        print()
        
        print("🔧 업로드 옵션:")
        print()
        
        print("1️⃣  SCP/SFTP로 전송 (권장)")
        print("   # BGM 파일 전송")
        print(f"   scp C:\\Users\\user\\Desktop\\economic_shorts\\assets\\audio\\bgm\\*.mp3 \\")
        print(f"       user@server:{self.bgm_dir.absolute()}/")
        print()
        print("   # SFX 파일 전송")
        print(f"   scp -r C:\\Users\\user\\Desktop\\economic_shorts\\assets\\audio\\sfx\\* \\")
        print(f"       user@server:{self.sfx_dir.absolute()}/")
        print()
        
        print("2️⃣  SFTP 클라이언트 사용")
        print("   - FileZilla, WinSCP 등 설치")
        print("   - 서버 연결 후 드래그 앤 드롭으로 업로드")
        print()
        
        print("3️⃣  클라우드 스토리지 경유")
        print("   # Windows에서 구글 드라이브에 업로드")
        print("   # 서버에서 다운로드")
        print("   cd /home/user/webapp/data/audio")
        print("   gdown [구글 드라이브 공유 링크]")
        print()
        
        print("4️⃣  Git LFS (대용량 파일)")
        print("   git lfs install")
        print("   git lfs track \"data/audio/**/*.mp3\"")
        print("   git add data/audio/")
        print("   git commit -m \"Add audio files\"")
        print("   git push")
        print()
    
    def verify_config(self):
        """설정 파일 확인"""
        print("=" * 70)
        print("⚙️  설정 확인")
        print("=" * 70)
        print()
        
        config_path = self.project_root / "config" / "config.yaml"
        if config_path.exists():
            print(f"✅ config.yaml 발견: {config_path}")
            
            # 설정 파일 읽기
            try:
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                audio_config = config.get('video', {}).get('audio', {})
                
                # BGM 설정
                bgm = audio_config.get('background_music', {})
                print()
                print("  [배경음악 설정]")
                print(f"    사용: {'✅' if bgm.get('enabled') else '❌'}")
                print(f"    소스: {bgm.get('source', 'auto')}")
                print(f"    경로: {bgm.get('file_path', 'N/A')}")
                print(f"    볼륨: {bgm.get('volume', 0.15)}")
                
                if bgm.get('source') != 'file':
                    print()
                    print("    ⚠️  주의: source가 'file'이 아닙니다!")
                    print("    → config.yaml에서 'source: file'로 변경하세요")
                
                # SFX 설정
                sfx = audio_config.get('sound_effects', {})
                print()
                print("  [효과음 설정]")
                print(f"    사용: {'✅' if sfx.get('enabled') else '❌'}")
                print(f"    경로: {sfx.get('library_path', 'data/audio/sfx/')}")
                print(f"    볼륨: {sfx.get('volume', 0.4)}")
                print(f"    AI 생성: {'✅' if sfx.get('auto_generate', {}).get('enabled') else '❌'}")
                
                if sfx.get('auto_generate', {}).get('enabled'):
                    print()
                    print("    💡 팁: 로컬 파일이 없으면 AI로 생성됩니다")
                
            except Exception as e:
                print(f"❌ 설정 파일 읽기 실패: {e}")
        else:
            print(f"❌ config.yaml을 찾을 수 없음: {config_path}")
        
        print()
    
    def test_sound_system(self):
        """사운드 시스템 테스트"""
        print("=" * 70)
        print("🧪 사운드 시스템 테스트")
        print("=" * 70)
        print()
        
        try:
            from src.video_generation.sound_effects import SoundEffectManager
            
            manager = SoundEffectManager()
            
            print("✅ SoundEffectManager 초기화 성공")
            print()
            
            # BGM 테스트
            print("  [BGM 테스트]")
            bgm = manager.get_background_music(60)
            if bgm:
                print(f"    ✅ BGM 선택: {bgm}")
            else:
                print("    ⚠️  BGM 없음 (파일 업로드 필요)")
            
            print()
            
            # SFX 테스트
            print("  [SFX 테스트]")
            test_effects = [
                ('whoosh', 'intro'),
                ('impact', 'hook'),
                ('pop', 'key_point'),
                ('reveal', 'chart_reveal'),
            ]
            
            for effect, category in test_effects:
                sfx = manager.get_sound_effect(effect, 0.0, category)
                if sfx:
                    print(f"    ✅ {category}/{effect}: {sfx['path']}")
                else:
                    print(f"    ⚠️  {category}/{effect}: 없음")
            
            print()
            print("💡 파일이 없는 효과음은 자동 생성되거나 건너뛰어집니다")
            
        except Exception as e:
            print(f"❌ 테스트 실패: {e}")
            logger.error(f"사운드 시스템 테스트 실패: {e}")
        
        print()
    
    def run(self):
        """메인 실행"""
        self.check_directories()
        self.scan_existing_files()
        self.show_upload_instructions()
        self.verify_config()
        self.test_sound_system()
        
        print("=" * 70)
        print("✅ 준비 완료!")
        print("=" * 70)
        print()
        print("다음 단계:")
        print("  1. Windows 로컬 파일을 서버로 업로드")
        print("  2. python upload_audio_helper.py 다시 실행하여 확인")
        print("  3. python main.py --mode single --preset quick 로 테스트")
        print()
        print("📖 자세한 가이드: UPLOAD_AUDIO.md 참조")
        print()


if __name__ == "__main__":
    helper = AudioUploadHelper()
    helper.run()
