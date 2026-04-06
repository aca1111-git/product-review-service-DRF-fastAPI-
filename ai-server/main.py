from fastapi import FastAPI
from api.recommend import router as recommend_router

# FastAPI 앱 생성
app = FastAPI(title="AI Recommendation Server")

# 라우터 연결
app.include_router(recommend_router)

# 기본 테스트 API
@app.get("/")
def root():
    return {"message": "AI server is running"}
