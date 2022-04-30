"""Роутеры к API-запросам."""

from django.urls import include, path
from rest_framework import routers

from .views import UserSignUp
from .views import UsersViewSet, UserAuth

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', UserSignUp.as_view()),
    path('v1/auth/token/', UserAuth.as_view()),
    path('v1/', include(router_v1.urls)),
]
