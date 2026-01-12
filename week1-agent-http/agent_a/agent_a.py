import requests
import time

time.sleep(5)  # 서버(B)가 켜질 때까지 기다림
url = "http://agent_b:8000/tool"
payload = {"tool": "read_file", "args": {"path": "/hello.txt"}}

print("🚀 [Agent A] 서버로 요청 전송 시작!")
try:
    response = requests.post(url, json=payload)
    print(f"📡 서버 응답: {response.json()}")
except Exception as e:
    print(f"❌ 에러 발생: {e}")