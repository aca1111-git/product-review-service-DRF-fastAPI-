from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Recommendation Server (Deploy)")

@app.get("/")
def root():
    return {"message": "AI server is running"}

class EmbeddingRequest(BaseModel):
    texts: list[str]

class SimilarityRequest(BaseModel):
    text1: str
    text2: str

@app.post("/api/v1/recommend/embed")
def embed_texts(payload: EmbeddingRequest):
    # 배포용 더미 응답 (실제 임베딩 없음)
    dummy = [[0.0] * 128 for _ in payload.texts]
    return {"embeddings": dummy}

@app.post("/api/v1/recommend/similarity")
def similarity(payload: SimilarityRequest):
    # 배포용 더미 응답
    return {"similarity": 0.5}
