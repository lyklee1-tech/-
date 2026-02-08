"""
AI 기반 Shorts 스크립트 자동 생성 모듈
"""
import os
from typing import Dict, List
from openai import OpenAI
from loguru import logger
import yaml
import json


class ScriptGenerator:
    """경제사냥꾼 스타일의 Shorts 스크립트 생성기"""
    
    def __init__(self, config_path='config/config.yaml'):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # 설정 로드
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            self.script_config = config['script']
    
    def generate_script(self, topic: str, data: Dict, style='경제사냥꾼') -> Dict:
        """
        주제와 데이터를 기반으로 Shorts 스크립트 생성
        
        Args:
            topic: 스크립트 주제 (예: "비트코인 급등")
            data: 관련 데이터 딕셔너리
            style: 스크립트 스타일
        
        Returns:
            생성된 스크립트 딕셔너리
        """
        
        system_prompt = f"""
당신은 '{style}' 채널의 전문 경제 콘텐츠 작가입니다.

# 채널 특성
- 타겟: 2030 투자 관심층
- 톤앤매너: 전문적이면서도 친근하고 이해하기 쉽게
- 특징: 충격적인 팩트, 구체적인 숫자, 명확한 인사이트

# 스크립트 구조 (총 150-200자, 30-60초)
1. HOOK (0-3초): 시청자의 관심을 확 끄는 질문이나 충격적인 팩트
2. 핵심 내용 (3-30초): 주요 정보와 데이터 전달
3. 데이터 설명 (30-45초): 구체적인 숫자와 차트 설명
4. 인사이트 (45-55초): 이것이 의미하는 바
5. CTA (55-60초): 구독/좋아요 유도

# 작성 규칙
- 첫 문장은 반드시 질문형 또는 충격적인 숫자로 시작
- 구체적인 숫자를 반드시 포함
- 전문 용어는 쉽게 풀어서 설명
- 말하듯이 자연스럽게 작성
- 이모지 사용 금지 (영상에서 추가됨)
"""
        
        user_prompt = f"""
다음 정보를 바탕으로 유튜브 Shorts 스크립트를 작성해주세요:

주제: {topic}

데이터:
{json.dumps(data, ensure_ascii=False, indent=2)}

요구사항:
- 정확히 {self.script_config['min_length']}-{self.script_config['max_length']}자 내외
- 첫 3초 안에 시청자의 시선을 사로잡을 것
- 구체적인 숫자와 팩트 포함
- 마지막에 구독 유도 멘트 자연스럽게 포함

JSON 형식으로 다음과 같이 반환:
{{
    "title": "영상 제목 (50자 이내)",
    "hook": "처음 3초 후킹 멘트",
    "script": "전체 스크립트 (150-200자)",
    "key_points": ["강조할 포인트 1", "강조할 포인트 2", "강조할 포인트 3"],
    "hashtags": ["태그1", "태그2", "태그3", "태그4", "태그5"],
    "thumbnail_text": "썸네일에 들어갈 텍스트 (15자 이내)"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.8,
                max_tokens=1000
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"스크립트 생성 완료: {result['title']}")
            
            return result
            
        except Exception as e:
            logger.error(f"스크립트 생성 실패: {e}")
            return None
    
    def generate_multiple_scripts(self, topics_data: List[Dict], count=3) -> List[Dict]:
        """여러 개의 스크립트를 생성"""
        scripts = []
        
        for i, item in enumerate(topics_data[:count], 1):
            logger.info(f"스크립트 {i}/{count} 생성 중...")
            script = self.generate_script(item['topic'], item['data'])
            
            if script:
                script['source_data'] = item
                scripts.append(script)
        
        logger.info(f"총 {len(scripts)}개 스크립트 생성 완료")
        return scripts
    
    def refine_script(self, script: str, feedback: str) -> str:
        """스크립트 개선"""
        
        prompt = f"""
다음 스크립트를 개선해주세요:

원본 스크립트:
{script}

개선 요청사항:
{feedback}

개선된 스크립트만 반환해주세요.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            refined = response.choices[0].message.content
            logger.info("스크립트 개선 완료")
            return refined
            
        except Exception as e:
            logger.error(f"스크립트 개선 실패: {e}")
            return script


# 테스트 코드
if __name__ == "__main__":
    logger.add("logs/script_generator.log", rotation="1 day")
    
    # 테스트 데이터
    test_data = {
        'topic': '비트코인 10% 급등',
        'data': {
            'asset': '비트코인',
            'current_price': 58500000,
            'change_percent': 10.5,
            'volume': 1500000000000,
            'reason': '미국 현물 ETF 순매수 증가',
            'timestamp': '2024-01-15 14:30'
        }
    }
    
    generator = ScriptGenerator()
    
    print("=" * 60)
    print("AI 스크립트 생성 테스트")
    print("=" * 60)
    
    result = generator.generate_script(test_data['topic'], test_data['data'])
    
    if result:
        print(f"\n제목: {result['title']}")
        print(f"\n후킹 멘트: {result['hook']}")
        print(f"\n스크립트:\n{result['script']}")
        print(f"\n강조 포인트:")
        for i, point in enumerate(result['key_points'], 1):
            print(f"  {i}. {point}")
        print(f"\n해시태그: {', '.join(result['hashtags'])}")
        print(f"\n썸네일 텍스트: {result['thumbnail_text']}")
