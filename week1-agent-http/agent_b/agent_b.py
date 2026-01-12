from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ToolRequest(BaseModel):
    tool: str
    args: dict

@app.post("/tool")
async def handle_tool(request: ToolRequest):
    print(f"✅ [Agent B] 수신 완료: {request.tool}")
    return {"status": "ok", "received": request.tool, "args": request.args}