from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),

    path("accounts/", include("apps.accounts.urls")),
    path("products/", include("apps.products.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("interactions/", include("apps.interactions.urls")),
    path("ai/", include("apps.ai_gateway.urls")),

    # 스키마 생성 (자체 분석용)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # FastAPI 스타일의 Swagger UI (이게 우리가 원하는 것!)
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)