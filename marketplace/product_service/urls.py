from django.urls import path

from rest_framework import routers

from .views import ListCategoryView, ProductViewSet, SliderApiView

router = routers.DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path(
        'category-list/',
        ListCategoryView.as_view(),
        name=ListCategoryView.__name__
    ),
    path(
        'slider/',
        SliderApiView.as_view(),
        name=SliderApiView.__name__
    )
] + router.urls
