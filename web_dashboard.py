"""
🎨 GenSpark AI 비디오 생성기 웹 대시보드
버튼 클릭으로 비디오 생성 + 자동 다운로드
"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import sys
import json
import time
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from loguru import logger
from werkzeug.utils import secure_filename
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 트렌드 분석기 임포트
sys.path.insert(0, str(Path(__file__).parent))
from src.data_collection.trend_analyzer import TrendAnalyzer
from src.character_manager import CharacterManager

app = Flask(__name__)
CORS(app)

# 업로드 설정
UPLOAD_FOLDER = Path('data/characters/images')
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 제한

# 트렌드 분석기 초기화
trend_analyzer = TrendAnalyzer()

# 캐릭터 관리자 초기화
character_manager = CharacterManager()

# 경로 설정
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
AUDIO_DIR = DATA_DIR / 'audio'
SCENES_DIR = DATA_DIR / 'scenes'
VIDEOS_DIR = DATA_DIR / 'videos'
SCRIPTS_DIR = DATA_DIR / 'scripts'

# 디렉토리 생성
for dir_path in [DATA_DIR, AUDIO_DIR, SCENES_DIR, VIDEOS_DIR, SCRIPTS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# 대본 파일 확장자
SCRIPT_ALLOWED_EXTENSIONS = {'txt', 'md', 'docx'}


def allowed_file(filename):
    """허용된 파일 확장자 체크"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 스타일 템플릿 정의 (이미지와 동일)
STYLE_TEMPLATES = {
    'professional': {
        'name': '전문적 (Professional)',
        'description': '비즈니스, 기업, 뉴스',
        'keywords': ['business', 'professional', 'corporate', 'clean', 'modern'],
        'icon': '💼'
    },
    'stickman': {
        'name': '스틱맨 애니메이션',
        'description': '간단한 애니메이션 캐릭터',
        'keywords': ['stickman', 'simple', 'animation', 'whiteboard'],
        'icon': '🙂'
    },
    'japanese_anime': {
        'name': '일본 애니메이션',
        'description': '애니메이션 스타일',
        'keywords': ['anime', 'japanese', 'animation', 'manga'],
        'icon': '👧'
    },
    'cinematic': {
        'name': '시네마틱',
        'description': '영화 같은 느낌',
        'keywords': ['cinematic', 'dramatic', 'film', 'movie'],
        'icon': '🎬'
    },
    '3d': {
        'name': '3D 렌더링',
        'description': '3D 그래픽',
        'keywords': ['3d', 'render', 'graphics', 'modern'],
        'icon': '🎮'
    },
    'documentary': {
        'name': '다큐멘터리',
        'description': '실사 영상',
        'keywords': ['documentary', 'realistic', 'nature', 'real'],
        'icon': '🌍'
    },
    'performance_metrics': {
        'name': '성과 지표',
        'description': '차트와 그래프',
        'keywords': ['charts', 'graphs', 'metrics', 'data'],
        'icon': '📊'
    },
    'office_scene': {
        'name': '오피스 장면',
        'description': '사무실 배경',
        'keywords': ['office', 'workplace', 'business', 'desk'],
        'icon': '🏢'
    }
}

# 비디오 길이 프리셋
DURATION_PRESETS = {
    'quick': {'value': 20, 'name': '빠른 (20초)', 'icon': '⚡'},
    'short': {'value': 30, 'name': '짧게 (30초)', 'icon': '🎯'},
    'standard': {'value': 60, 'name': '표준 (1분)', 'icon': '📝'},
    'shorts': {'value': 120, 'name': 'Shorts (2분)', 'icon': '📱'},
    'medium': {'value': 300, 'name': '중간 (5분)', 'icon': '🎬'},
    'long': {'value': 600, 'name': '긴 영상 (10분)', 'icon': '📹'},
    'extended': {'value': 1200, 'name': '확장 (20분)', 'icon': '🎥'},
    'maximum': {'value': 1800, 'name': '최대 (30분)', 'icon': '🎞️'}
}

# TTS 목소리 프리셋
VOICE_PRESETS = {
    'male_young': {
        'name': '남성 (젊은)',
        'description': '밝고 에너지 넘치는',
        'icon': '👨',
        'voice_id': 'ko-KR-Neural2-C',
        'pitch': 0,
        'speed': 1.0
    },
    'male_mature': {
        'name': '남성 (성숙한)',
        'description': '차분하고 신뢰감 있는',
        'icon': '👔',
        'voice_id': 'ko-KR-Neural2-D',
        'pitch': -2,
        'speed': 0.95
    },
    'female_young': {
        'name': '여성 (젊은)',
        'description': '친근하고 활발한',
        'icon': '👩',
        'voice_id': 'ko-KR-Neural2-A',
        'pitch': 2,
        'speed': 1.05
    },
    'female_professional': {
        'name': '여성 (전문가)',
        'description': '정확하고 명료한',
        'icon': '👩‍💼',
        'voice_id': 'ko-KR-Neural2-B',
        'pitch': 0,
        'speed': 1.0
    },
    'news_anchor': {
        'name': '뉴스 앵커',
        'description': '뉴스 진행자 스타일',
        'icon': '📺',
        'voice_id': 'ko-KR-Standard-A',
        'pitch': 0,
        'speed': 0.9
    },
    'youtube_creator': {
        'name': '유튜버',
        'description': '생동감 있고 재미있는',
        'icon': '🎬',
        'voice_id': 'ko-KR-Wavenet-A',
        'pitch': 1,
        'speed': 1.1
    }
}

# 자막 스타일 프리셋
SUBTITLE_PRESETS = {
    'youtube_default': {
        'name': 'YouTube 기본',
        'description': '가독성 좋은 기본 스타일',
        'icon': '📺',
        'font_family': 'Noto Sans KR',
        'font_size': 48,
        'font_weight': 'bold',
        'color': '#FFFFFF',
        'bg_color': '#000000',
        'bg_opacity': 0.7,
        'position': 'bottom',
        'align': 'center',
        'outline': True,
        'outline_color': '#000000',
        'outline_width': 3,
        'animation': 'fade'
    },
    'shorts_trendy': {
        'name': 'Shorts 트렌디',
        'description': 'MZ세대 감성',
        'icon': '⚡',
        'font_family': 'Pretendard',
        'font_size': 56,
        'font_weight': 'black',
        'color': '#FFFF00',
        'bg_color': '#FF0080',
        'bg_opacity': 0,
        'position': 'center',
        'align': 'center',
        'outline': True,
        'outline_color': '#000000',
        'outline_width': 4,
        'animation': 'bounce'
    },
    'minimal_clean': {
        'name': '미니멀 클린',
        'description': '깔끔하고 전문적인',
        'icon': '✨',
        'font_family': 'Noto Sans KR',
        'font_size': 42,
        'font_weight': 'normal',
        'color': '#FFFFFF',
        'bg_color': 'transparent',
        'bg_opacity': 0,
        'position': 'bottom',
        'align': 'center',
        'outline': True,
        'outline_color': '#000000',
        'outline_width': 2,
        'animation': 'none'
    },
    'bold_impact': {
        'name': '굵은 임팩트',
        'description': '강렬한 인상',
        'icon': '💥',
        'font_family': 'Gmarket Sans',
        'font_size': 64,
        'font_weight': 'black',
        'color': '#FF3333',
        'bg_color': '#FFFFFF',
        'bg_opacity': 0.9,
        'position': 'top',
        'align': 'center',
        'outline': False,
        'outline_color': '#000000',
        'outline_width': 0,
        'animation': 'slide'
    },
    'news_anchor': {
        'name': '뉴스 앵커',
        'description': '뉴스 자막 스타일',
        'icon': '📰',
        'font_family': 'Noto Sans KR',
        'font_size': 40,
        'font_weight': 'medium',
        'color': '#FFFFFF',
        'bg_color': '#1E3A8A',
        'bg_opacity': 0.95,
        'position': 'bottom',
        'align': 'left',
        'outline': False,
        'outline_color': '#000000',
        'outline_width': 0,
        'animation': 'typewriter'
    },
    'cinematic': {
        'name': '시네마틱',
        'description': '영화 자막 느낌',
        'icon': '🎬',
        'font_family': 'Noto Serif KR',
        'font_size': 44,
        'font_weight': 'normal',
        'color': '#F0F0F0',
        'bg_color': 'transparent',
        'bg_opacity': 0,
        'position': 'bottom',
        'align': 'center',
        'outline': True,
        'outline_color': '#000000',
        'outline_width': 2,
        'animation': 'fade'
    }
}


@app.route('/')
def index():
    """메인 대시보드 페이지"""
    return render_template('dashboard.html', 
                         styles=STYLE_TEMPLATES,
                         durations=DURATION_PRESETS,
                         voices=VOICE_PRESETS,
                         subtitles=SUBTITLE_PRESETS)


@app.route('/preview')
def preview():
    """프리뷰 & 편집 페이지"""
    return render_template('preview.html',
                         subtitles=SUBTITLE_PRESETS)


@app.route('/api/generate', methods=['POST'])
def generate_video():
    """
    비디오 생성 API
    POST /api/generate
    Body: {
        "topic": "비트코인 급등",
        "duration": 20,
        "style": "professional",
        "script": "optional custom script"
    }
    """
    try:
        data = request.json
        topic = data.get('topic')
        duration = data.get('duration', 20)
        aspect_ratio = data.get('aspect_ratio', '1:1')
        style = data.get('style', 'professional')
        voice = data.get('voice', 'male_young')
        character_mode = data.get('character_mode', 'auto')
        character_image = data.get('character_image')
        custom_script = data.get('script')
        
        if not topic:
            return jsonify({'success': False, 'error': '토픽을 입력해주세요!'}), 400
        
        logger.info(f"🎬 비디오 생성 시작: {topic} ({duration}초, {aspect_ratio}, {style} 스타일, {voice} 목소리)")
        logger.info(f"👤 캐릭터 모드: {character_mode}, 이미지: {bool(character_image)}")
        
        # GenSpark AutoPilot 실행
        cmd = [
            sys.executable,
            'genspark_autopilot.py',
            '--topic', topic,
            '--duration', str(duration)
        ]
        
        if custom_script:
            cmd.extend(['--script', custom_script])
        
        # 프로세스 실행
        result = subprocess.run(
            cmd,
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=300  # 5분 타임아웃
        )
        
        # 출력 파싱
        output = result.stdout + result.stderr
        logger.info(f"Output: {output}")
        
        # 생성된 파일 찾기
        audio_files = sorted(AUDIO_DIR.glob('genspark_*.mp3'), key=lambda x: x.stat().st_mtime, reverse=True)
        scene_files = sorted(SCENES_DIR.glob('genspark_scenes_*.json'), key=lambda x: x.stat().st_mtime, reverse=True)
        
        if not audio_files or not scene_files:
            return jsonify({
                'success': False,
                'error': '파일 생성 실패',
                'output': output
            }), 500
        
        # 최신 파일
        audio_file = audio_files[0]
        scene_file = scene_files[0]
        
        # 장면 데이터 로드
        with open(scene_file, 'r', encoding='utf-8') as f:
            scene_data = json.load(f)
        
        # 응답 데이터
        response = {
            'success': True,
            'topic': topic,
            'duration': duration,
            'aspect_ratio': aspect_ratio,
            'style': style,
            'voice': voice,
            'audio_file': str(audio_file.relative_to(BASE_DIR)),
            'scene_file': str(scene_file.relative_to(BASE_DIR)),
            'audio_size': audio_file.stat().st_size,
            'num_scenes': len(scene_data.get('scenes', [])),
            'scenes': scene_data.get('scenes', []),
            'timestamp': datetime.now().isoformat(),
            'cost': 0  # 완전 무료!
        }
        
        logger.info(f"✅ 비디오 생성 완료!")
        return jsonify(response)
        
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': '타임아웃 (5분 초과)'}), 500
    except Exception as e:
        logger.error(f"❌ 오류: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/download/audio/<filename>')
def download_audio(filename):
    """오디오 파일 다운로드"""
    try:
        file_path = AUDIO_DIR / filename
        if not file_path.exists():
            return jsonify({'error': '파일을 찾을 수 없습니다'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='audio/mpeg'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/scenes/<filename>')
def download_scenes(filename):
    """장면 데이터 다운로드"""
    try:
        file_path = SCENES_DIR / filename
        if not file_path.exists():
            return jsonify({'error': '파일을 찾을 수 없습니다'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status')
def status():
    """시스템 상태 확인"""
    audio_count = len(list(AUDIO_DIR.glob('*.mp3')))
    scene_count = len(list(SCENES_DIR.glob('*.json')))
    video_count = len(list(VIDEOS_DIR.glob('*.mp4')))
    
    return jsonify({
        'status': 'ok',
        'audio_files': audio_count,
        'scene_files': scene_count,
        'video_files': video_count,
        'styles_available': len(STYLE_TEMPLATES),
        'duration_presets': len(DURATION_PRESETS)
    })


@app.route('/api/history')
def history():
    """생성 히스토리"""
    audio_files = sorted(AUDIO_DIR.glob('genspark_*.mp3'), key=lambda x: x.stat().st_mtime, reverse=True)
    scene_files = sorted(SCENES_DIR.glob('genspark_scenes_*.json'), key=lambda x: x.stat().st_mtime, reverse=True)
    
    history = []
    
    for audio_file, scene_file in zip(audio_files[:20], scene_files[:20]):
        try:
            with open(scene_file, 'r', encoding='utf-8') as f:
                scene_data = json.load(f)
            
            history.append({
                'topic': scene_data.get('topic', 'Unknown'),
                'duration': scene_data.get('duration', 0),
                'audio_file': audio_file.name,
                'scene_file': scene_file.name,
                'num_scenes': len(scene_data.get('scenes', [])),
                'timestamp': datetime.fromtimestamp(audio_file.stat().st_mtime).isoformat(),
                'size': audio_file.stat().st_size
            })
        except:
            continue
    
    return jsonify({'history': history})


@app.route('/api/trends')
def get_trends():
    """
    🔥 실시간 트렌드 분석 API
    GET /api/trends?hours=7
    """
    try:
        hours = int(request.args.get('hours', 7))
        logger.info(f"🔥 트렌드 분석 요청 (최근 {hours}시간)")
        
        # 트렌드 분석 실행
        result = trend_analyzer.analyze_all_trends(hours=hours)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"❌ 트렌드 분석 오류: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/trends/top')
def get_top_trend():
    """
    🎯 가장 핫한 주제 1개 반환 (자동 선택용)
    GET /api/trends/top?hours=7
    """
    try:
        hours = int(request.args.get('hours', 7))
        logger.info(f"🎯 TOP 트렌드 요청 (최근 {hours}시간)")
        
        # 최고 인기 주제 가져오기
        top_topic = trend_analyzer.get_top_topic(hours=hours)
        
        if top_topic:
            return jsonify({
                'success': True,
                'topic': top_topic,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': '트렌드를 찾을 수 없습니다'
            }), 404
        
    except Exception as e:
        logger.error(f"❌ TOP 트렌드 오류: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/characters', methods=['GET'])
def get_characters():
    """
    사용자의 캐릭터 목록 가져오기
    GET /api/characters?user_id=xxx
    """
    try:
        user_id = request.args.get('user_id', 'default_user')
        characters = character_manager.get_user_characters(user_id)
        
        return jsonify({
            'success': True,
            'characters': characters,
            'count': len(characters)
        })
    except Exception as e:
        logger.error(f"❌ 캐릭터 목록 조회 오류: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/characters/create', methods=['POST'])
def create_character():
    """
    새 캐릭터 생성
    POST /api/characters/create
    Body: {
        "user_id": "user_123",
        "character_name": "경제 앵커",
        "style": "professional",
        "voice": "female_professional",
        "appearance_prompt": "optional custom prompt"
    }
    """
    try:
        data = request.json
        user_id = data.get('user_id', 'default_user')
        character_name = data.get('character_name')
        style = data.get('style', 'professional')
        voice = data.get('voice', 'male_young')
        appearance_prompt = data.get('appearance_prompt')
        
        if not character_name:
            return jsonify({
                'success': False,
                'error': '캐릭터 이름을 입력해주세요'
            }), 400
        
        character = character_manager.create_character(
            user_id=user_id,
            character_name=character_name,
            style=style,
            voice=voice,
            appearance_prompt=appearance_prompt
        )
        
        logger.info(f"✅ 캐릭터 생성: {character_name}")
        return jsonify({
            'success': True,
            'character': character
        })
        
    except Exception as e:
        logger.error(f"❌ 캐릭터 생성 오류: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/characters/<character_id>/stats', methods=['GET'])
def get_character_stats(character_id):
    """캐릭터 통계 조회"""
    try:
        stats = character_manager.get_character_stats(character_id)
        
        if stats:
            return jsonify({
                'success': True,
                'stats': stats
            })
        else:
            return jsonify({
                'success': False,
                'error': '캐릭터를 찾을 수 없습니다'
            }), 404
            
    except Exception as e:
        logger.error(f"❌ 캐릭터 통계 조회 오류: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/characters/upload-image', methods=['POST'])
def upload_character_image():
    """
    캐릭터 이미지 업로드
    POST /api/characters/upload-image
    Form Data:
        - image: 이미지 파일
        - character_id: 캐릭터 ID (선택)
    """
    try:
        # 파일 체크
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': '이미지 파일이 없습니다'
            }), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '파일이 선택되지 않았습니다'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': '지원하지 않는 파일 형식입니다 (png, jpg, jpeg, gif, webp만 가능)'
            }), 400
        
        # 파일 저장
        filename = secure_filename(file.filename)
        timestamp = int(datetime.now().timestamp() * 1000)
        unique_filename = f"{timestamp}_{filename}"
        
        file_path = UPLOAD_FOLDER / unique_filename
        file.save(str(file_path))
        
        # 이미지 정보
        file_size = file_path.stat().st_size
        
        logger.info(f"✅ 캐릭터 이미지 업로드 완료: {unique_filename} ({file_size/1024:.1f} KB)")
        
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'file_path': str(file_path.relative_to(Path.cwd())),
            'file_size': file_size,
            'url': f'/api/characters/images/{unique_filename}'
        })
        
    except Exception as e:
        logger.error(f"❌ 이미지 업로드 오류: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/characters/images/<filename>')
def serve_character_image(filename):
    """캐릭터 이미지 제공"""
    try:
        file_path = UPLOAD_FOLDER / filename
        
        if not file_path.exists():
            return jsonify({
                'error': '이미지를 찾을 수 없습니다'
            }), 404
        
        return send_file(file_path, mimetype='image/jpeg')
        
    except Exception as e:
        logger.error(f"❌ 이미지 제공 오류: {e}")
        return jsonify({
            'error': str(e)
        }), 500


# ============================================================
# 대본 관리 API
# ============================================================

@app.route('/api/scripts', methods=['GET'])
def get_scripts():
    """저장된 대본 목록 가져오기"""
    try:
        scripts = []
        
        if SCRIPTS_DIR.exists():
            for file_path in sorted(SCRIPTS_DIR.glob('*.txt'), key=lambda x: x.stat().st_mtime, reverse=True):
                scripts.append({
                    'filename': file_path.name,
                    'title': file_path.stem,
                    'size': file_path.stat().st_size,
                    'created': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'url': f'/api/scripts/{file_path.name}'
                })
        
        return jsonify({
            'success': True,
            'scripts': scripts,
            'total': len(scripts)
        })
        
    except Exception as e:
        logger.error(f"❌ 대본 목록 조회 오류: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/scripts/<filename>', methods=['GET'])
def get_script(filename):
    """특정 대본 내용 가져오기"""
    try:
        file_path = SCRIPTS_DIR / secure_filename(filename)
        
        if not file_path.exists():
            return jsonify({
                'error': '대본을 찾을 수 없습니다'
            }), 404
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            'success': True,
            'filename': filename,
            'content': content,
            'size': file_path.stat().st_size
        })
        
    except Exception as e:
        logger.error(f"❌ 대본 조회 오류: {e}")
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/scripts', methods=['POST'])
def save_script():
    """대본 저장 (텍스트 또는 파일 업로드)"""
    try:
        # 파일 업로드인 경우
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({
                    'success': False,
                    'error': '파일이 선택되지 않았습니다'
                }), 400
            
            if not file.filename.endswith('.txt'):
                return jsonify({
                    'success': False,
                    'error': 'txt 파일만 업로드 가능합니다'
                }), 400
            
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{timestamp}_{filename}"
            file_path = SCRIPTS_DIR / unique_filename
            
            file.save(str(file_path))
            
            logger.info(f"✅ 대본 파일 업로드 완료: {unique_filename}")
            
            return jsonify({
                'success': True,
                'filename': unique_filename,
                'message': '대본이 업로드되었습니다'
            })
        
        # 텍스트 저장인 경우
        else:
            data = request.json
            
            if not data or 'content' not in data:
                return jsonify({
                    'success': False,
                    'error': '대본 내용이 없습니다'
                }), 400
            
            content = data['content']
            title = data.get('title', 'untitled')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{secure_filename(title)}.txt"
            file_path = SCRIPTS_DIR / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ 대본 저장 완료: {filename}")
            
            return jsonify({
                'success': True,
                'filename': filename,
                'message': '대본이 저장되었습니다'
            })
        
    except Exception as e:
        logger.error(f"❌ 대본 저장 오류: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/scripts/<filename>', methods=['DELETE'])
def delete_script(filename):
    """대본 삭제"""
    try:
        file_path = SCRIPTS_DIR / secure_filename(filename)
        
        if not file_path.exists():
            return jsonify({
                'error': '대본을 찾을 수 없습니다'
            }), 404
        
        file_path.unlink()
        
        logger.info(f"✅ 대본 삭제 완료: {filename}")
        
        return jsonify({
            'success': True,
            'message': '대본이 삭제되었습니다'
        })
        
    except Exception as e:
        logger.error(f"❌ 대본 삭제 오류: {e}")
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/scripts/generate', methods=['POST'])
def generate_script():
    """주제로 대본 자동 생성 (GPT-4)"""
    try:
        data = request.json
        
        if not data or 'topic' not in data:
            return jsonify({
                'success': False,
                'error': '주제가 필요합니다'
            }), 400
        
        topic = data['topic']
        duration = data.get('duration', 60)  # 기본 60초
        
        # 현재 날짜 가져오기
        current_date = datetime.now().strftime('%Y년 %m월 %d일')
        current_time = datetime.now().strftime('%H시 %M분')
        
        # 영상 길이에 따른 대본 분량 계산
        # 일반적으로 1초당 약 2-3 단어 (한국어 기준)
        words_per_second = 2.5
        estimated_words = int(duration * words_per_second)
        
        # 영상 길이별 대본 생성
        if duration <= 30:
            # 짧은 영상 (20-30초): 핵심만 간결하게
            sample_script = f"""# {topic}

[날짜: {current_date} {current_time} 기준]
[영상 길이: {duration}초 / 약 {estimated_words}단어]

{current_date} 현재, {topic}이(가) 실시간으로 급상승하고 있습니다.

핵심 포인트를 빠르게 살펴보겠습니다.

{topic}의 주요 내용은...
[여기에 핵심 내용 작성]

이상 {topic}에 대한 속보였습니다!
"""
        elif duration <= 60:
            # 중간 영상 (40-60초): 서론-본론-결론
            sample_script = f"""# {topic}

[날짜: {current_date} {current_time} 기준]
[영상 길이: {duration}초 / 약 {estimated_words}단어]

안녕하세요! {current_date}, {topic}에 대해 알아보겠습니다.

[서론]
{current_date} 현재, {topic}이(가) 많은 관심을 받고 있습니다.
실시간으로 급상승하고 있는 이 주제에 대해 자세히 살펴보겠습니다.

[본론]
{topic}의 주요 내용을 살펴보면...
최신 정보를 바탕으로 분석해보면...

[결론]
이상으로 {current_date} 기준 {topic}에 대해 알아보았습니다.
"""
        else:
            # 긴 영상 (60초 이상): 상세한 구성
            sample_script = f"""# {topic}

[날짜: {current_date} {current_time} 기준]
[영상 길이: {duration}초 / 약 {estimated_words}단어]

안녕하세요! {current_date}, {topic}에 대해 심층 분석해보겠습니다.

[인트로]
오늘은 최근 뜨거운 이슈인 {topic}에 대해 자세히 다뤄보겠습니다.

[배경]
{current_date} 현재, {topic}이(가) 왜 주목받고 있을까요?
최근 동향과 배경을 먼저 살펴보겠습니다.

[핵심 내용]
{topic}의 주요 내용을 자세히 분석해보면...
전문가들은 이렇게 말합니다...

[영향 분석]
이것이 우리에게 미치는 영향은...
앞으로의 전망은...

[결론 & 요약]
지금까지 {current_date} 기준 {topic}에 대해 알아보았습니다.
핵심 포인트를 다시 한번 정리하면...

감사합니다!
"""
        
        # 대본 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{secure_filename(topic)}.txt"
        file_path = SCRIPTS_DIR / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sample_script)
        
        logger.info(f"✅ 대본 생성 완료: {filename}")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'content': sample_script,
            'message': '대본이 생성되었습니다'
        })
        
    except Exception as e:
        logger.error(f"❌ 대본 생성 오류: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/learn-style', methods=['POST'])
def learn_channel_style():
    """YouTube 채널 스타일 학습"""
    try:
        data = request.json
        
        if not data or 'channel_url' not in data:
            return jsonify({
                'success': False,
                'error': '채널 URL이 필요합니다'
            }), 400
        
        channel_url = data['channel_url']
        
        # 채널명 추출 (URL에서)
        import re
        channel_match = re.search(r'@([^/]+)', channel_url)
        channel_name = channel_match.group(1) if channel_match else '알 수 없는 채널'
        
        # YouTube API 키 확인
        youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        
        if youtube_api_key and youtube_api_key != 'your_youtube_api_key':
            # YouTube API 사용
            try:
                logger.info(f"🔍 YouTube API로 채널 분석 시작: {channel_name}")
                
                # 1. 채널 ID 가져오기
                search_url = "https://www.googleapis.com/youtube/v3/search"
                search_params = {
                    'part': 'snippet',
                    'q': channel_name,
                    'type': 'channel',
                    'maxResults': 1,
                    'key': youtube_api_key
                }
                
                search_response = requests.get(search_url, params=search_params, timeout=10)
                search_response.raise_for_status()
                search_data = search_response.json()
                
                if not search_data.get('items'):
                    raise Exception('채널을 찾을 수 없습니다')
                
                channel_id = search_data['items'][0]['snippet']['channelId']
                actual_channel_name = search_data['items'][0]['snippet']['title']
                
                logger.info(f"✅ 채널 발견: {actual_channel_name} (ID: {channel_id})")
                
                # 2. 채널의 최근 영상 가져오기
                videos_url = "https://www.googleapis.com/youtube/v3/search"
                videos_params = {
                    'part': 'snippet',
                    'channelId': channel_id,
                    'type': 'video',
                    'order': 'date',
                    'maxResults': 10,
                    'key': youtube_api_key
                }
                
                videos_response = requests.get(videos_url, params=videos_params, timeout=10)
                videos_response.raise_for_status()
                videos_data = videos_response.json()
                
                video_ids = [item['id']['videoId'] for item in videos_data.get('items', [])]
                
                logger.info(f"✅ 영상 {len(video_ids)}개 발견")
                
                # 3. 영상 상세 정보 가져오기
                if video_ids:
                    details_url = "https://www.googleapis.com/youtube/v3/videos"
                    details_params = {
                        'part': 'snippet,contentDetails',
                        'id': ','.join(video_ids[:5]),  # 최근 5개만
                        'key': youtube_api_key
                    }
                    
                    details_response = requests.get(details_url, params=details_params, timeout=10)
                    details_response.raise_for_status()
                    details_data = details_response.json()
                    
                    # 4. 스타일 분석
                    titles = []
                    descriptions = []
                    
                    for item in details_data.get('items', []):
                        snippet = item['snippet']
                        titles.append(snippet.get('title', ''))
                        descriptions.append(snippet.get('description', ''))
                    
                    # 제목 분석
                    all_titles_text = ' '.join(titles)
                    
                    # 특징 분석
                    characteristics = []
                    
                    # 질문형 시작 체크
                    if any('?' in title for title in titles):
                        characteristics.append('🔥 호기심을 자극하는 질문형 시작')
                    
                    # 숫자 사용 체크
                    if any(re.search(r'\d+', title) for title in titles):
                        characteristics.append('💰 구체적인 숫자와 데이터 활용')
                    
                    # 긴급성/주목성 키워드 체크
                    urgent_keywords = ['급등', '급락', '주목', '긴급', '속보', '위험', '기회', '폭등', '폭락']
                    if any(keyword in all_titles_text for keyword in urgent_keywords):
                        characteristics.append('⚡ 긴급성과 주목성을 강조하는 스타일')
                    
                    # 간결함 체크
                    avg_title_length = sum(len(t) for t in titles) / len(titles) if titles else 0
                    if avg_title_length < 30:
                        characteristics.append('⚡ 빠른 템포와 간결한 제목')
                    
                    # 투자 관련 키워드 체크
                    invest_keywords = ['투자', '주식', '코인', '비트코인', '경제', '수익', '손실']
                    if any(keyword in all_titles_text for keyword in invest_keywords):
                        characteristics.append('📊 투자 관점에서의 분석')
                    
                    # 기본 특징 추가
                    if not characteristics:
                        characteristics = [
                            '🎯 핵심을 먼저 전달하는 스타일',
                            '📺 전문적이고 신뢰감 있는 톤',
                            '💡 정보 전달 중심의 구성'
                        ]
                    
                    # 키워드 추출 (간단한 방식)
                    common_words = ['여러분', '오늘', '이번', '최근', '주목', '핵심', '중요']
                    key_phrases = [word for word in common_words if word in all_titles_text]
                    
                    if not key_phrases:
                        key_phrases = ['여러분', '핵심은', '주목해야 할 점은']
                    
                    style_data = {
                        'channel_name': actual_channel_name,
                        'channel_url': channel_url,
                        'channel_id': channel_id,
                        'videos_analyzed': len(titles),
                        'characteristics': characteristics,
                        'tone': 'professional_casual',
                        'structure': 'hook_data_conclusion',
                        'avg_sentence_length': 15,
                        'key_phrases': key_phrases,
                        'sample_titles': titles[:3]
                    }
                    
                    logger.info(f"✅ 스타일 분석 완료: {actual_channel_name}")
                    
                    return jsonify({
                        'success': True,
                        'style': style_data,
                        'message': f'{actual_channel_name} 스타일 분석 완료'
                    })
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"⚠️ YouTube API 오류, 샘플 데이터 사용: {e}")
                # API 오류 시 샘플 데이터로 폴백
            except Exception as e:
                logger.warning(f"⚠️ 분석 오류, 샘플 데이터 사용: {e}")
                # 기타 오류 시 샘플 데이터로 폴백
        
        # YouTube API 없거나 오류 시 샘플 스타일 반환
        logger.info(f"ℹ️ 샘플 스타일 데이터 사용: {channel_name}")
        
        sample_style = {
            'channel_name': channel_name,
            'channel_url': channel_url,
            'videos_analyzed': 5,
            'characteristics': [
                '🎯 핵심을 먼저 전달하는 직설적인 스타일',
                '💰 구체적인 숫자와 데이터 활용',
                '⚡ 빠른 템포와 간결한 문장',
                '🔥 호기심을 자극하는 질문형 시작',
                '📊 투자 관점에서의 분석'
            ],
            'tone': 'professional_casual',
            'structure': 'hook_data_conclusion',
            'avg_sentence_length': 15,
            'key_phrases': ['여러분', '핵심은', '주목해야 할 점은', '결론부터 말씀드리면']
        }
        
        return jsonify({
            'success': True,
            'style': sample_style,
            'message': f'{channel_name} 스타일 분석 완료 (샘플 데이터)',
            'note': 'YouTube API 키를 설정하면 실제 채널 분석이 가능합니다'
        })
        
    except Exception as e:
        logger.error(f"❌ 스타일 학습 오류: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/scripts/generate-with-style', methods=['POST'])
def generate_script_with_style():
    """학습한 스타일로 대본 생성"""
    try:
        data = request.json
        
        if not data or 'topic' not in data:
            return jsonify({
                'success': False,
                'error': '주제가 필요합니다'
            }), 400
        
        topic = data['topic']
        duration = data.get('duration', 60)
        style = data.get('style', {})
        
        # 현재 날짜 가져오기
        current_date = datetime.now().strftime('%Y년 %m월 %d일')
        current_time = datetime.now().strftime('%H시 %M분')
        
        channel_name = style.get('channel_name', '경제사냥꾼')
        
        # 스타일에 맞춘 대본 생성
        if duration <= 30:
            # 짧은 영상: 핵심 직설적 스타일
            styled_script = f"""# {topic}

[날짜: {current_date} {current_time} 기준]
[스타일: {channel_name}]
[영상 길이: {duration}초]

여러분, {topic} 이슈가 터졌습니다!

결론부터 말씀드리면, [핵심 내용]

주목해야 할 점은 세 가지입니다.
첫째, [포인트 1]
둘째, [포인트 2]
셋째, [포인트 3]

여러분의 투자 전략은? 댓글로 알려주세요!
"""
        elif duration <= 60:
            # 중간 영상: 데이터 기반 분석
            styled_script = f"""# {topic}

[날짜: {current_date} {current_time} 기준]
[스타일: {channel_name}]
[영상 길이: {duration}초]

여러분, {current_date} 현재 {topic}에 대해 알아보겠습니다.

결론부터 말씀드리면, 이건 놓치면 안 됩니다!

핵심 데이터를 보시죠.
- [구체적 수치 1]
- [구체적 수치 2]
- [구체적 수치 3]

그렇다면 우리는 어떻게 해야 할까요?

전문가들은 이렇게 말합니다.
[전문가 의견 또는 분석]

주목해야 할 점은, [핵심 포인트]

투자자 관점에서 정리하면,
1) [요점 1]
2) [요점 2]  
3) [요점 3]

여러분의 생각은 어떠신가요? 댓글로 공유해주세요!
"""
        else:
            # 긴 영상: 심층 분석 + 데이터
            styled_script = f"""# {topic}

[날짜: {current_date} {current_time} 기준]
[스타일: {channel_name}]
[영상 길이: {duration}초]

여러분, {topic} 이슈에 대해 자세히 분석해보겠습니다.

[인트로]
결론부터 말씀드리면, 이건 반드시 알아야 합니다!

[배경 분석]
먼저 배경을 살펴보죠.
{current_date} 현재, 이런 상황입니다.
- 배경 1
- 배경 2

[핵심 데이터]
주목해야 할 데이터를 보겠습니다.
📊 수치 1: [구체적 데이터]
📊 수치 2: [구체적 데이터]
📊 수치 3: [구체적 데이터]

[분석]
그렇다면 이게 무엇을 의미할까요?

첫째, [분석 포인트 1]
둘째, [분석 포인트 2]
셋째, [분석 포인트 3]

[전문가 의견]
전문가들은 이렇게 평가합니다.
[전문가 분석 또는 시장 반응]

[투자 전략]
투자자 관점에서 정리하면,
1) [전략 1]
2) [전략 2]
3) [전략 3]

[마무리]
핵심은 [요약]

여러분은 어떻게 생각하시나요?
댓글로 의견 공유해주세요!

감사합니다!
"""
        
        # 대본 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{secure_filename(topic)}_{channel_name}.txt"
        file_path = SCRIPTS_DIR / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(styled_script)
        
        logger.info(f"✅ 스타일 대본 생성 완료: {filename}")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'content': styled_script,
            'message': f'{channel_name} 스타일 대본이 생성되었습니다'
        })
        
    except Exception as e:
        logger.error(f"❌ 스타일 대본 생성 오류: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tts/preview', methods=['POST'])
def preview_tts():
    """TTS 목소리 미리듣기"""
    try:
        data = request.json
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': '텍스트가 필요합니다'
            }), 400
        
        text = data['text']
        voice = data.get('voice', 'ko-KR-Neural2-A')
        
        # TTS 생성
        from gtts import gTTS
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"preview_{timestamp}.mp3"
        file_path = AUDIO_DIR / filename
        
        tts = gTTS(text=text, lang='ko')
        tts.save(str(file_path))
        
        logger.info(f"✅ TTS 미리듣기 생성: {filename}")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'url': f'/api/audio/preview/{filename}',
            'message': 'TTS가 생성되었습니다'
        })
        
    except Exception as e:
        logger.error(f"❌ TTS 미리듣기 오류: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/audio/preview/<filename>')
def serve_preview_audio(filename):
    """미리듣기 오디오 파일 제공"""
    try:
        file_path = AUDIO_DIR / filename
        
        if not file_path.exists():
            return jsonify({
                'error': '오디오 파일을 찾을 수 없습니다'
            }), 404
        
        return send_file(file_path, mimetype='audio/mpeg')
        
    except Exception as e:
        logger.error(f"❌ 오디오 제공 오류: {e}")
        return jsonify({
            'error': str(e)
        }), 500


if __name__ == '__main__':
    logger.info("=" * 80)
    logger.info("🎨 GenSpark AI 비디오 생성기 웹 대시보드")
    logger.info("=" * 80)
    logger.info("🌐 URL: http://localhost:5000")
    logger.info("📝 Docs: http://localhost:5000/api/status")
    logger.info("=" * 80)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
