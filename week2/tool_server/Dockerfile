FROM python:3.9-slim
RUN pip install fastapi uvicorn
COPY . /app
WORKDIR /app
CMD ["uvicorn", "tool_server:app", "--host", "0.0.0.0", "--port", "8001"]
#포트 8001 사용