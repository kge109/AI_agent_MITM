from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()


class PromptRequest(BaseModel):
    trace_id: str
    stage: str
    prompt: str


@app.post("/prompt")
async def handle_prompt(request: PromptRequest):
    print(f"✅ [Agent B] 프롬프트 분석 중: {request.prompt}")

    # 규칙 기반 처리: 'file' 키워드 여부 확인
    tool = "read_file" if "file" in request.prompt else "echo"

    # 2단계: Tool Server 호출 (tool-call)
    tool_payload = {
        "trace_id": request.trace_id,
        "stage": "tool-call",
        "tool": tool,
        "args": {"text": request.prompt}
    }

    response = requests.post("http://tool_server:8001/tool", json=tool_payload)
    return response.json()