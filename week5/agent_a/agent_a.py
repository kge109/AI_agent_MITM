import requests
import os
import uuid
import time

# 환경변수에서 프롬프트 가져오기 (기본값: read file)
PROMPT = os.getenv("PROMPT", "read file")


def main():
    time.sleep(5)  # 다른 서버들 부팅 대기
    trace_id = str(uuid.uuid4())

    # 1단계: 프롬프트 전달
    payload = {
        "trace_id": trace_id,
        "stage": "prompt",
        "prompt": PROMPT
    }

    print(f"🚀 [Agent A] 프롬프트 전송: {PROMPT}")
    try:
        response = requests.post("http://agent_b:8000/prompt", json=payload)
        print(f"📡 최종 응답 수신: {response.json()}")
    except Exception as e:
        print(f"❌ 에러 발생: {e}")


if __name__ == "__main__":
    main()