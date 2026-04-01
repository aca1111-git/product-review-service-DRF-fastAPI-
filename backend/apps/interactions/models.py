from django.db import models
from django.conf import settings

from apps.reviews.models import Review


User = settings.AUTH_USER_MODEL


class ReviewLike(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    review = models.ForeignKey(
        "reviews.Review",
        on_delete=models.CASCADE,
        related_name="likes"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "review")
        ordering = ["-id"]

    def __str__(self):
        # 관리자 페이지 등에서 표시되는 문자열
        return f"{self.user} - {self.review}"
    
 
       
class ReviewBookmark(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    review = models.ForeignKey(
        "reviews.Review",
        on_delete=models.CASCADE,
        related_name="bookmarks"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    class Meta:
        # 같은 리뷰를 같은 사용자가 여러 번 북마크하지 못하도록 제한
        unique_together = ("user", "review")

        ordering = ["-id"]

    def __str__(self):
        return f"{self.user} - {self.review}"
    



class ReviewComment(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    review = models.ForeignKey(
        "reviews.Review",
        on_delete=models.CASCADE,
        related_name="comments"
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user} - {self.review}"
    



class ReviewReport(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    review = models.ForeignKey(
        "reviews.Review",
        on_delete=models.CASCADE,
        related_name="reports"
    )

    reason = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        # 같은 사용자가 같은 리뷰를 여러 번 신고하지 못하도록 제한
        unique_together = ("user", "review")

        ordering = ["-id"]

    def __str__(self):
        return f"{self.user} - {self.review}"
    
