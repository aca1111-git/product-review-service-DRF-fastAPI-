from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.reviews.models import Review

from .models import (
    ReviewLike,
    ReviewBookmark,
    ReviewComment,
    ReviewReport,
)

from .serializers import (
    ReviewCommentSerializer,
    ReviewReportSerializer,
)



# class ReviewLikeViewSet(ViewSet):
#     def list(self, request):
#         likes = ReviewLike.objects.all()
#         serializer = ReviewLikeSerializer(likes, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = ReviewLikeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)    



# class ReviewBookmarkViewSet(ViewSet):
#     def list(self, request):
#         bookmarks = ReviewBookmark.objects.all()
#         serializer = ReviewBookmarkSerializer(bookmarks, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = ReviewBookmarkSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)


# class ReviewCommentViewSet(ViewSet):
#     def list(self, request):
#         comments = ReviewComment.objects.all()
#         serializer = ReviewCommentSerializer(comments, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = ReviewCommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)



# class ReviewReportViewSet(ViewSet):
#     def list(self, request):
#         reports = ReviewReport.objects.all()
#         serializer = ReviewReportSerializer(reports, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = ReviewReportSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors)
    



class ReviewLikeToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):

        # review_id에 해당하는 리뷰 가져오기
        review = get_object_or_404(Review, id=review_id)

        # 좋아요가 이미 있는지 확인 후 생성
        obj, created = ReviewLike.objects.get_or_create(
            review=review,
            user=request.user
        )

        # 이미 존재하면 → 좋아요 취소
        if not created:
            obj.delete()
            liked = False
        else:
            # 새로 생성 → 좋아요 추가
            liked = True

        # 현재 리뷰의 총 좋아요 수 계산
        count = ReviewLike.objects.filter(review=review).count()

        # 결과 반환
        return Response(
            {
                "liked": liked,         # 현재 사용자의 좋아요 상태
                "like_count": count,    # 총 좋아요 수
            },
            status=status.HTTP_200_OK
        )


class ReviewBookmarkToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):

        # 대상 리뷰 조회
        review = get_object_or_404(Review, id=review_id)

        # 북마크 존재 여부 확인 후 생성
        obj, created = ReviewBookmark.objects.get_or_create(
            review=review,
            user=request.user
        )

        # 이미 있으면 삭제
        if not created:
            obj.delete()
            bookmarked = False
        else:
            bookmarked = True

        # 현재 북마크 개수 계산
        count = ReviewBookmark.objects.filter(review=review).count()

        return Response(
            {
                "bookmarked": bookmarked,
                "bookmark_count": count,
            },
            status=status.HTTP_200_OK
        )


class ReviewCommentCreateAPIView(APIView):
    """
    리뷰 댓글 생성 API

    요청
    POST /reviews/{review_id}/comments/

    body
    {
        "content": "댓글 내용"
    }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):

        # 댓글이 달릴 리뷰 조회
        review = get_object_or_404(Review, id=review_id)

        # 요청 body에서 댓글 내용 가져오기
        content = request.data.get("content", "").strip()

        # 내용이 없으면 오류
        if not content:
            return Response(
                {"detail": "내용이 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 댓글 생성
        comment = ReviewComment.objects.create(
            review=review,
            user=request.user,
            content=content
        )

        # serializer로 JSON 변환
        serializer = ReviewCommentSerializer(comment)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    

class ReviewCommentListAPIView(APIView):
    """
    리뷰 댓글 목록 조회 API

    요청
    GET /reviews/{review_id}/comments/
    """

    # 댓글 조회는 로그인 없이 가능
    permission_classes = [AllowAny]

    def get(self, request, review_id):

        # 리뷰 조회
        review = get_object_or_404(Review, id=review_id)

        # 해당 리뷰의 댓글 조회
        comments = ReviewComment.objects.filter(
            review=review
        ).order_by("-created_at")

        # serializer로 변환
        serializer = ReviewCommentSerializer(comments, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class ReviewCommentDetailAPIView(APIView):
    """
    리뷰 댓글 수정 / 삭제 API

    수정
    PATCH /comments/{comment_id}/

    삭제
    DELETE /comments/{comment_id}/
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, comment_id):

        # 댓글 조회
        comment = get_object_or_404(ReviewComment, id=comment_id)

        # 작성자만 수정 가능
        if comment.user != request.user:
            return Response(
                {"detail": "본인 댓글만 수정할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 수정할 내용
        content = request.data.get("content", "").strip()

        # 내용 검사
        if not content:
            return Response(
                {"detail": "내용이 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 댓글 수정
        comment.content = content
        comment.save()

        serializer = ReviewCommentSerializer(comment)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, comment_id):

        # 댓글 조회
        comment = get_object_or_404(ReviewComment, id=comment_id)

        # 작성자만 삭제 가능
        if comment.user != request.user:
            return Response(
                {"detail": "본인 댓글만 삭제할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 댓글 삭제
        comment.delete()

        return Response(
            {"detail": "댓글이 삭제되었습니다."},
            status=status.HTTP_204_NO_CONTENT
        )

class ReviewReportCreateAPIView(APIView):
    """
    리뷰 신고 생성 API

    요청
    POST /reviews/{review_id}/report/

    body
    {
        "reason": "스팸 리뷰"
    }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):

        # 신고 대상 리뷰 조회
        review = get_object_or_404(Review, id=review_id)

        # 신고 사유
        reason = request.data.get("reason", "").strip()

        # 신고 사유 없으면 오류
        if not reason:
            return Response(
                {"detail": "신고 사유가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 신고 생성
        report = ReviewReport.objects.create(
            review=review,
            user=request.user,
            reason=reason
        )

        serializer = ReviewReportSerializer(report)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class ReviewReportListAPIView(APIView):
    """
    리뷰 신고 목록 조회 API
    (관리자 확인용)

    GET /reviews/{review_id}/reports/
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, review_id):

        # 리뷰 조회
        review = get_object_or_404(Review, id=review_id)

        # 해당 리뷰의 신고 목록 조회
        reports = ReviewReport.objects.filter(
            review=review
        ).order_by("-created_at")

        serializer = ReviewReportSerializer(reports, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
