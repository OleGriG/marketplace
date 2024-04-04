from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .filtersets import ProductFilter
from core.permissions import OnlySallers, IsOwnerOrReadOnly


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
        "retrive": ProductSerializer
    }
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, ProductSerializer)

    def get_permissions(self):
        if self.action == 'create':
            return [OnlySellers()]
        return super().get_permissions()

