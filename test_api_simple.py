#!/usr/bin/env python3
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

print(f"🔑 테스트할 키: {api_key[:20]}...{api_key[-10:]}")
print(f"🔑 키 길이: {len(api_key)} 자")
print()

try:
    client = OpenAI(api_key=api_key)
    
    print("📡 API 요청 전송 중...")
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',  # 더 저렴한 모델로 테스트
        messages=[{'role': 'user', 'content': 'Hi'}],
        max_tokens=5
    )
    
    print("✅ 성공!")
    print(f"응답: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ 실패: {e}")
    print()
    print("가능한 원인:")
    print("1. 키가 아직 활성화 중 (5-10분 대기)")
    print("2. Organization 설정 문제")
    print("3. Project 권한 문제")
