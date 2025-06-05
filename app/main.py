from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services.tag_recommender import TagRecommenderService
import time
from typing import Dict
import gc

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 레이트 리미팅을 위한 간단한 메모리 저장소
request_store: Dict[str, float] = {}
RATE_LIMIT_SECONDS = 1  # 최소 요청 간격

class ContentRequest(BaseModel):
    contents: str

recommender = TagRecommenderService()

@app.post("/tag/recommendations")
async def recommend_tags(request: ContentRequest):
    try:
        # 요청 간격 체크
        current_time = time.time()
        if request_store.get("last_request_time", 0) + RATE_LIMIT_SECONDS > current_time:
            raise HTTPException(status_code=429, detail="Too many requests")
        request_store["last_request_time"] = current_time

        # 입력 텍스트 길이 제한
        if len(request.contents) > 1000:  # 1000자로 제한
            raise HTTPException(status_code=400, detail="Text too long")

        tags = recommender.recommend_tags(request.contents)
        
        # 메모리 정리
        gc.collect()
        
        return {"tags": tags}
    except Exception as e:
        # 에러 발생 시 메모리 정리
        gc.collect()
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )

# 서버 시작 시 메모리 정리
@app.on_event("startup")
async def startup_event():
    gc.collect()

# 주기적으로 메모리 정리
@app.middleware("http")
async def clean_memory(request, call_next):
    response = await call_next(request)
    if len(request_store) > 1000:  # 저장소가 너무 커지면 초기화
        request_store.clear()
    return response
