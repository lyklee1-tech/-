"""
차트 생성 모듈 - 경제 데이터 시각화
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path
import numpy as np
from typing import Dict, List
from loguru import logger


class ChartGenerator:
    """경제 데이터 차트 생성기"""
    
    def __init__(self):
        # 한글 폰트 설정
        try:
            # NanumGothic 폰트 사용
            font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
            if Path(font_path).exists():
                fm.fontManager.addfont(font_path)
                plt.rcParams['font.family'] = 'NanumGothic'
        except:
            logger.warning("한글 폰트 설정 실패. 기본 폰트 사용")
        
        # 마이너스 기호 깨짐 방지
        plt.rcParams['axes.unicode_minus'] = False
        
        # 다크 테마
        plt.style.use('dark_background')
    
    def create_line_chart(
        self,
        data: Dict[str, List[float]],
        title: str,
        output_path: str,
        xlabel: str = '날짜',
        ylabel: str = '가격'
    ) -> bool:
        """라인 차트 생성"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            for label, values in data.items():
                ax.plot(values, label=label, linewidth=2, marker='o')
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel(xlabel, fontsize=12)
            ax.set_ylabel(ylabel, fontsize=12)
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
            plt.close()
            
            logger.info(f"라인 차트 생성: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"라인 차트 생성 실패: {e}")
            return False
    
    def create_bar_chart(
        self,
        labels: List[str],
        values: List[float],
        title: str,
        output_path: str,
        colors: List[str] = None
    ) -> bool:
        """막대 차트 생성"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # 색상 설정 (양수/음수)
            if colors is None:
                colors = ['#00ff88' if v >= 0 else '#ff6b6b' for v in values]
            
            bars = ax.bar(labels, values, color=colors, alpha=0.8)
            
            # 값 표시
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.,
                    height,
                    f'{height:+.2f}%' if abs(height) < 100 else f'{height:+,.0f}',
                    ha='center',
                    va='bottom' if height >= 0 else 'top',
                    fontsize=10
                )
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.axhline(y=0, color='white', linestyle='-', linewidth=0.5)
            ax.grid(True, alpha=0.3, axis='y')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
            plt.close()
            
            logger.info(f"막대 차트 생성: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"막대 차트 생성 실패: {e}")
            return False
    
    def create_comparison_chart(
        self,
        categories: List[str],
        series1: List[float],
        series2: List[float],
        title: str,
        output_path: str,
        label1: str = '이전',
        label2: str = '현재'
    ) -> bool:
        """비교 차트 생성"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            x = np.arange(len(categories))
            width = 0.35
            
            bars1 = ax.bar(x - width/2, series1, width, label=label1, color='#4a90e2', alpha=0.8)
            bars2 = ax.bar(x + width/2, series2, width, label=label2, color='#00ff88', alpha=0.8)
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
            ax.set_xticks(x)
            ax.set_xticklabels(categories)
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3, axis='y')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
            plt.close()
            
            logger.info(f"비교 차트 생성: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"비교 차트 생성 실패: {e}")
            return False
    
    def create_price_change_visual(
        self,
        symbol: str,
        current_price: float,
        change_percent: float,
        output_path: str
    ) -> bool:
        """가격 변동 시각화"""
        try:
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # 배경
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')
            
            # 심볼
            ax.text(5, 8, symbol, fontsize=32, fontweight='bold',
                   ha='center', va='center')
            
            # 현재 가격
            price_text = f"₩{current_price:,.0f}" if current_price < 100000 else f"₩{current_price/10000:.1f}만"
            ax.text(5, 5.5, price_text, fontsize=48, fontweight='bold',
                   ha='center', va='center')
            
            # 변동률
            color = '#00ff88' if change_percent >= 0 else '#ff6b6b'
            sign = '+' if change_percent >= 0 else ''
            ax.text(5, 3, f"{sign}{change_percent:.2f}%", fontsize=36,
                   color=color, fontweight='bold', ha='center', va='center')
            
            # 화살표
            arrow = '▲' if change_percent >= 0 else '▼'
            ax.text(5, 1.5, arrow, fontsize=48, color=color,
                   ha='center', va='center')
            
            plt.tight_layout()
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=150, bbox_inches='tight',
                       facecolor='#1a1a2e', transparent=False)
            plt.close()
            
            logger.info(f"가격 변동 시각화 생성: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"가격 변동 시각화 실패: {e}")
            return False


# 테스트 코드
if __name__ == "__main__":
    logger.add("logs/chart_generator.log", rotation="1 day")
    
    generator = ChartGenerator()
    
    # 1. 라인 차트 테스트
    print("1. 라인 차트 생성...")
    line_data = {
        'KOSPI': [2500, 2520, 2480, 2550, 2580],
        'KOSDAQ': [850, 860, 845, 870, 880]
    }
    generator.create_line_chart(
        line_data,
        '주요 지수 추이',
        'data/charts/line_chart.png'
    )
    
    # 2. 막대 차트 테스트
    print("2. 막대 차트 생성...")
    generator.create_bar_chart(
        ['삼성전자', 'SK하이닉스', 'NAVER', '카카오', 'LG화학'],
        [3.5, -2.1, 5.2, -1.8, 4.3],
        '주요 종목 등락률',
        'data/charts/bar_chart.png'
    )
    
    # 3. 가격 변동 시각화 테스트
    print("3. 가격 변동 시각화 생성...")
    generator.create_price_change_visual(
        '비트코인',
        58500000,
        10.5,
        'data/charts/btc_change.png'
    )
    
    print("\n✅ 모든 차트 생성 완료!")
