from fastapi import FastAPI
from pydantic import BaseModel
import os  # 파일 존재 여부를 확인하기 위해 추가가 필요합니다.

app = FastAPI()


class ToolCall(BaseModel):
    trace_id: str
    stage: str
    tool: str
    args: dict


@app.post("/tool")
async def handle_tool(request: ToolCall):
    print(f"🛠 [Tool Server] 작업 실행: {request.tool}")

    # 기본 응답 메시지
    result = f"Executed {request.tool} successfully"

    if request.tool == "read_file":
        # 요청(args)에서 path 값을 가져옵니다.
        # 가은님이 Repeater에서 보낼 {"path": "/data/hello.txt"} 형식을 처리합니다.
        file_path = request.args.get("path")

        # 만약 path가 없고 에이전트가 보낸 text만 있다면 기본 경로를 설정합니다.
        if not file_path and "text" in request.args:
            file_path = "/data/hello.txt"

        # 실제로 파일이 있는지 확인하고 내용을 읽어옵니다.
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    result = f.read().strip()  # 가은님이 수정한 "HELLO!!!!!!"를 여기서 읽습니다.
            except Exception as e:
                result = f"Error reading file: {str(e)}"
        else:
            result = f"File not found: {file_path}"

    return {
        "trace_id": request.trace_id,
        "stage": "tool-response",
        "status": "ok",
        "result": result
    }