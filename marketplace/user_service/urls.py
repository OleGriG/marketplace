from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from .views import UserRegisterView, RefreshTokenView, LoginView


urlpatterns = [
    path(
        'registration/',
        UserRegisterView.as_view(),
        name=UserRegisterView.__name__
    ),
    path(
        'refresh-token/',
        RefreshTokenView.as_view(),
        name=RefreshTokenView.__name__
    ),
    path(
        'login/',
        LoginView.as_view(),
        name=RefreshTokenView.__name__
    ),

]