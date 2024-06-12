from django.urls import path

from rest_framework import routers

from .views import ListCategoryView, ProductViewSet, SliderApiView, CartViewSet, CategoryViewSet

router = routers.DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'categories', CategoryViewSet, basename='categories')

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
