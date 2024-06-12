from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from .models import Category, Product, Slider, Cart
from .serializers import (
    CategorySerializer, ProductSerializer, DetaileProductSerializer,
    SliderSerializer, CartSerializer, CartAddProductSerializer,
    CartRemoveProducts
)
from .filtersets import ProductFilter
from core.permissions import OnlySellers, IsOwnerOrReadOnly, IsOwner


class ListCategoryView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('owner')
    permission_classes = [IsOwnerOrReadOnly]
    serializer_classes = {
        "create": ProductSerializer,
        "update": ProductSerializer,
        "destroy": ProductSerializer,
        "list": ProductSerializer,
        "retrive": DetaileProductSerializer
    }
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, ProductSerializer)

    def get_permissions(self):
        if self.action == 'create':
            return [OnlySellers()]
        return super().get_permissions()


class SliderApiView(ListAPIView):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [AllowAny]


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    @action(methods=['post'], detail=False, url_path='add-to-cart')
    def add_to_cart(self, request):
        cart = self.get_queryset()
        serializer = CartAddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']
        product = Product.objects.get(id=product_id)
        cart.products.add(product)
        cart.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='get-cart')
    def get_cart(self, request):
        cart = self.get_queryset()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='remove-products')
    def remove_products_from_cart(self, request):
        cart = self.get_queryset()
        serializer = CartRemoveProducts(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_ids = serializer.validated_data.get('product_ids')
        products_to_remove = Product.objects.filter(id__in=product_ids)
        cart.products.remove(*products_to_remove)
        return Response({"message": "Ok"}, status=status.HTTP_200_OK)
