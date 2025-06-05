FROM python:3.10-slim

# 시스템 패키지 설치
RUN apt-get update && \
    apt-get install -y \
        mecab \
        libmecab-dev \
        mecab-ipadic-utf8 \
        gcc \
        g++ \
        curl \
        git \
        python3-dev \
        build-essential \
        default-jdk \
        fonts-nanum && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# FastAPI 실행 명령 (EC2/Fargate용)
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
