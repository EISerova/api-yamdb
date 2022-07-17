from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UsersViewSet, user_auth,
                    user_signup)

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register(r'categories', CategoryViewSet, basename='сategories')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'users', UsersViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)

urlpatterns = [
    path('v1/auth/signup/', user_signup),
    path('v1/auth/token/', user_auth),
    path('v1/', include(router_v1.urls)),
]
