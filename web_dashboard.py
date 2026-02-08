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
from pathlib import Path
from datetime import datetime
from loguru import logger

# 트렌드 분석기 임포트
sys.path.insert(0, str(Path(__file__).parent))
from src.data_collection.trend_analyzer import TrendAnalyzer

app = Flask(__name__)
CORS(app)

# 트렌드 분석기 초기화
trend_analyzer = TrendAnalyzer()

# 경로 설정
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
AUDIO_DIR = DATA_DIR / 'audio'
SCENES_DIR = DATA_DIR / 'scenes'
VIDEOS_DIR = DATA_DIR / 'videos'

# 디렉토리 생성
for dir_path in [DATA_DIR, AUDIO_DIR, SCENES_DIR, VIDEOS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


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


@app.route('/')
def index():
    """메인 대시보드 페이지"""
    return render_template('dashboard.html', 
                         styles=STYLE_TEMPLATES,
                         durations=DURATION_PRESETS)


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
        style = data.get('style', 'professional')
        custom_script = data.get('script')
        
        if not topic:
            return jsonify({'success': False, 'error': '토픽을 입력해주세요!'}), 400
        
        logger.info(f"🎬 비디오 생성 시작: {topic} ({duration}초, {style} 스타일)")
        
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
            'style': style,
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


if __name__ == '__main__':
    logger.info("=" * 80)
    logger.info("🎨 GenSpark AI 비디오 생성기 웹 대시보드")
    logger.info("=" * 80)
    logger.info("🌐 URL: http://localhost:5000")
    logger.info("📝 Docs: http://localhost:5000/api/status")
    logger.info("=" * 80)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
