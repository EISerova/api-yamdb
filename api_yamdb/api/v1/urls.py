"""Роутеры к API-запросам."""

from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()


router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    ReviewViewSet,
    basename='review',
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
