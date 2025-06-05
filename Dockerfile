FROM python:3.10-slim

# 시스템 패키지 최소화
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 파이썬 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV JAVA_OPTS="-Xmx256m"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers=1", "--threads=4", "--timeout=120", "--max-requests=1000", "--max-requests-jitter=50"]
