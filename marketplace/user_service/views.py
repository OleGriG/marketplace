from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import (
    get_object_or_404
)
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User
from .serializers import (
    UserRegisterSerializer, UserSerializer
)


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)

    schema = {
        status.HTTP_201_CREATED: UserSerializer(),
        status.HTTP_400_BAD_REQUEST: "Bad request",
    }

    serializer_classes = {
        "POST": UserRegisterSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method)

    @swagger_auto_schema(request_body=UserRegisterSerializer, responses=schema)
    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            password = request.data["password"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.data["password"] = make_password(password)
        try:
            response = self.create(request, *args, **kwargs)
            if response.status_code == status.HTTP_201_CREATED:
                user_data = response.data
                user = User.objects.get(id=user_data['id'])
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                response.data['refresh'] = str(refresh)
                response.data['access'] = access_token
        except Exception as e:
            return Response({'error': f'Ошибка при регистрации: {e}'}, status=400)

        return response


class LoginView(TokenViewBase):
    """Авторизация"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'login': openapi.Schema(type=openapi.TYPE_STRING, description='Username or email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                            'photo': openapi.Schema(type=openapi.TYPE_STRING, description='photo')
                        }
                    )
                },
                description='Successful login'
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        login = request.data.get('login')
        password = request.data.get('password')
        user = get_object_or_404(User, email=login)
        if user:
            user = authenticate(email=login, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                })
        return Response({'error': 'Неверные данные для входа'},
                        status=status.HTTP_400_BAD_REQUEST) 


class RefreshTokenView(APIView):
    """Обновление access токена с помощью refresh"""

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='refresh token'),
            }
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='access token'),
                },
                description='Successful response'
            ),
        }
    )
    def post(self, request):
        refresh = request.data.get('refresh')

        if refresh:
            try:
                token = RefreshToken(refresh)
                access = str(token.access_token)
                return Response({'access': access})
            except Exception as e:
                return Response({'error': str(e)}, status=400)
        else:
            return Response({'error': 'Refresh token is required'}, status=400)
