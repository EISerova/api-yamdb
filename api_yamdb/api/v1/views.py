from rest_framework import filters
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .mixins import CreateDestroyListMixin
from .permissions import IsAdminUserOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)
from reviews.models import Category, Comments, Genre, Review, Title


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
    pass
