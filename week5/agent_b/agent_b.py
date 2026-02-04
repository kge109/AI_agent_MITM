from fastapi import FastAPI
from pydantic import BaseModel
import requests
import urllib3

# SSL 경고 메시지(verify=False로 인한)가 터미널을 도배하지 않도록 설정합니다.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()


class PromptRequest(BaseModel):
    trace_id: str
    stage: str
    prompt: str


@app.post("/prompt")
async def handle_prompt(request: PromptRequest):
    print(f"✅ [Agent B] 프롬프트 분석 중: {request.prompt}")

    # 1단계: 규칙 기반 처리 - 'file' 키워드가 있으면 파일 읽기 도구 선택
    tool = "read_file" if "file" in request.prompt else "echo"

    # 2단계: Tool Server 호출을 위한 데이터 구성
    tool_payload = {
        "trace_id": request.trace_id,
        "stage": "tool-call",
        "tool": tool,
        "args": {"text": request.prompt}
    }

    # 3단계: Burp Suite 프록시 설정
    # host.docker.internal은 컨테이너 밖(가은님의 맥북)에서 떠 있는 Burp를 가리킵니다.
    proxies = {
        "http": "http://host.docker.internal:8080",
        "https": "http://host.docker.internal:8080",
    }

    try:
        # 4단계: Tool Server 호출 (Burp Suite 경유)
        # verify=False를 넣어야 Burp의 가짜 인증서를 만나도 에러 없이 통과합니다.
        response = requests.post(
            "http://tool_server:8001/tool",
            json=tool_payload,
            proxies=proxies,
            verify=False,
            timeout=100  # 통신이 무한 대기하지 않도록 타임아웃 추가
        )
        return response.json()

    except Exception as e:
        print(f"❌ [Agent B] 통신 에러 발생: {str(e)}")
        return {"error": "Connection to Tool Server failed via Proxy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)