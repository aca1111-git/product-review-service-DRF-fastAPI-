from rest_framework import serializers
from .models import (
    ReviewLike,
    ReviewBookmark,
    ReviewComment,
    ReviewReport,
)


class ReviewLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewLike
        fields = [
            "id",
            "user",
            "review",
            "created_at",
        ]

        # 클라이언트가 수정할 수 없는 필드
        read_only_fields = [
            "id",
            "user",        # 보통 request.user로 자동 설정
            "created_at",
        ]



        
class ReviewBookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewBookmark
        fields = [
            "id",
            "user",
            "review",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]



        
class ReviewCommentSerializer(serializers.ModelSerializer):
    # 댓글 작성자의 username을 추가로 보여주기 위한 필드
    username = serializers.CharField(
        source="user.username",  # user 모델의 username 필드를 참조
        read_only=True           # 읽기 전용 (클라이언트가 입력하지 않음)
    )


    class Meta:
        model = ReviewComment
        fields = [
            "id",
            "user",
            "username",    # 작성자 username (표시용)
            "review",
            "content",
            "created_at",
            "updated_at",  # 댓글 수정 시간
        ]
        
        
        read_only_fields = [
            "id",
            "user",        # request.user로 설정
            "username",    # user.username에서 자동 생성
            "review",      # 보통 URL에서 전달
            "created_at",
            "updated_at",
        ]



class ReviewReportSerializer(serializers.ModelSerializer):
    # 신고한 사용자 이름 표시
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = ReviewReport
        fields = [
            "id",
            "user",
            "username",    # 신고자 username
            "review",
            "reason",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "user",        # request.user 자동 설정
            "username",
            "review",      # URL 또는 View에서 설정
            "created_at",
        ]