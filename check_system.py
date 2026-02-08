#!/usr/bin/env python3
"""
시스템 상태 및 설정 확인 스크립트
"""
import os
import sys
from pathlib import Path
import yaml
from dotenv import load_dotenv

def check_python_version():
    """Python 버전 확인"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("  ⚠️  Python 3.9 이상을 권장합니다")
        return False
    return True

def check_dependencies():
    """필수 패키지 확인"""
    required_packages = [
        'openai', 'requests', 'beautifulsoup4', 'yfinance',
        'moviepy', 'pillow', 'yaml', 'loguru', 'schedule'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (누락)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  누락된 패키지: {', '.join(missing)}")
        print("   pip install -r requirements.txt 실행")
        return False
    return True

def check_ffmpeg():
    """FFmpeg 확인"""
    import shutil
    if shutil.which('ffmpeg'):
        print("✓ FFmpeg 설치됨")
        return True
    else:
        print("✗ FFmpeg 설치 필요")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  macOS: brew install ffmpeg")
        return False

def check_env_file():
    """환경변수 파일 확인"""
    if not Path('.env').exists():
        print("✗ .env 파일 없음")
        print("  .env.example을 복사하여 .env 생성 필요")
        return False
    
    load_dotenv()
    
    required_keys = {
        'OPENAI_API_KEY': 'OpenAI API (스크립트 생성)',
        'YOUTUBE_API_KEY': 'YouTube API (업로드)',
    }
    
    missing_keys = []
    for key, description in required_keys.items():
        value = os.getenv(key)
        if value and value != f'your_{key.lower()}':
            print(f"✓ {key} 설정됨")
        else:
            print(f"✗ {key} 미설정 ({description})")
            missing_keys.append(key)
    
    if missing_keys:
        print(f"\n⚠️  .env 파일에서 다음 키를 설정하세요:")
        for key in missing_keys:
            print(f"   - {key}")
        return False
    return True

def check_config():
    """설정 파일 확인"""
    config_path = Path('config/config.yaml')
    if not config_path.exists():
        print("✗ config/config.yaml 없음")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print("✓ config.yaml 로드 성공")
        
        # 주요 설정 확인
        print(f"  - 비디오 길이: {config['video']['duration']}초")
        print(f"  - TTS 제공자: {config['tts']['provider']}")
        print(f"  - 자동 업로드: {config['youtube']['auto_upload']}")
        print(f"  - 스케줄러: {config['scheduler']['enabled']}")
        
        return True
    except Exception as e:
        print(f"✗ config.yaml 오류: {e}")
        return False

def check_directories():
    """디렉토리 구조 확인"""
    required_dirs = [
        'data/raw', 'data/processed', 'data/scripts',
        'data/audio', 'data/videos', 'logs', 'config'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ {dir_path}/ 없음")
            all_exist = False
    
    if not all_exist:
        print("\n  mkdir -p {data/{raw,processed,scripts,audio,videos},logs,config}")
    
    return all_exist

def check_disk_space():
    """디스크 공간 확인"""
    import shutil
    total, used, free = shutil.disk_usage('/')
    
    free_gb = free // (2**30)
    print(f"✓ 여유 공간: {free_gb} GB")
    
    if free_gb < 5:
        print("  ⚠️  디스크 공간이 부족합니다 (5GB 이상 권장)")
        return False
    return True

def main():
    print("=" * 60)
    print("경제 유튜브 Shorts 자동화 시스템 - 상태 확인")
    print("=" * 60)
    print()
    
    checks = {
        "Python 버전": check_python_version,
        "필수 패키지": check_dependencies,
        "FFmpeg": check_ffmpeg,
        "환경변수": check_env_file,
        "설정 파일": check_config,
        "디렉토리": check_directories,
        "디스크 공간": check_disk_space,
    }
    
    results = {}
    
    for name, check_func in checks.items():
        print(f"\n[{name} 확인]")
        results[name] = check_func()
    
    print("\n" + "=" * 60)
    print("확인 결과 요약")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for name, result in results.items():
        status = "✅ 통과" if result else "❌ 실패"
        print(f"{name:20} {status}")
    
    print(f"\n{passed}/{total} 항목 통과")
    
    if passed == total:
        print("\n🎉 모든 확인 완료! 시스템을 사용할 준비가 되었습니다.")
        print("\n다음 명령어로 시작하세요:")
        print("  python main.py --mode single")
    else:
        print("\n⚠️  일부 항목을 수정해주세요.")
        print("\n도움말:")
        print("  - 설치: ./setup.sh")
        print("  - 설정: vi .env")
        print("  - 문서: README.md, QUICKSTART.md")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
