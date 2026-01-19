FROM python:3.9-slim
RUN pip install fastapi uvicorn requests
COPY . /app
WORKDIR /app
CMD ["uvicorn", "agent_b:app", "--host", "0.0.0.0", "--port", "8000"]