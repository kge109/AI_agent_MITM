from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ToolCall(BaseModel):
    trace_id: str
    stage: str
    tool: str
    args: dict


@app.post("/tool")
async def handle_tool(request: ToolCall):
    print(f"🛠 [Tool Server] 작업 실행: {request.tool}")

    result = f"Executed {request.tool} successfully"
    if request.tool == "read_file":
        result = "Hello Week2! This is data/hello.txt content."

    return {
        "trace_id": request.trace_id,
        "stage": "tool-response",
        "status": "ok",
        "result": result
    }