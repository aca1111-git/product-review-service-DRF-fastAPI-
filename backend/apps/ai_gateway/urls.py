from django.urls import path
from .views import (
    # SentimentAnalysisAPIView,  <-- 이 줄이 views.py에 없어서 에러가 납니다. 제거하거나 주석 처리하세요.
    # EmbeddingAPIView, 
    # SimilarityAPIView,
    ReviewAnalyzeAPIView,
)

urlpatterns = [
    # path("sentiment/", SentimentAnalysisAPIView.as_view()), <-- 위와 동일하게 제거 또는 주석 처리
    # path("embed/", EmbeddingAPIView.as_view(), name="ai-embed"),
    # path("similarity/", SimilarityAPIView.as_view(), name="ai-similarity"),
    path("reviews/<int:review_id>/analyze/", ReviewAnalyzeAPIView.as_view(), name="ai-review-analyze"),
]