from fastapi import FastAPI
from pydantic import BaseModel
from tag_recommender import TagRecommenderService

app = FastAPI()
recommender = TagRecommenderService()

class ContentRequest(BaseModel):
    contents: str

@app.post("/tag/recommendations")
def recommend_tags(request: ContentRequest):
    tags = recommender.recommend_tags(request.contents)
    return {"tags": tags}
