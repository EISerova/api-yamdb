from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .filters import TitleFilter
from .mixins import CreateDestroyListMixin
from .permissions import IsAdminUserOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)
from reviews.models import Category, Comment, Genre, Review, Title


class CategoryViewSet(CreateDestroyListMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    pass
