from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from user_service import urls as users_urls
from product_service import urls as products_urls
from .swagger import swagger_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include(users_urls)),
    path('api/marketplace/', include(products_urls)),
] + swagger_urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
