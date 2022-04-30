from rest_framework import filters
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)

from .mixins import CreateDestroyListMixin
from .permissions import IsAdminUserOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from reviews.models import Category, Comment, Genre, Review, Title
from .permissions import ReviewCommentPermission


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


class ReviewViewSet(ModelViewSet):
    """Обрабатывает запрос к обзорам."""

    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_title(self):
        """Получает из запроса объект Title."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        """
        Создает обзор к произведению.
        Автором обзор автоматически устанавливается пользователь.
        """
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        """Возвращает список обзоров к произведению."""
        return self.get_title().reviews


class CommentViewSet(ModelViewSet):
    """Обрабатывает запрос к комментариям."""

    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_review(self):
        return get_object_or_404(
            Review,
            title_id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id'),
        )

    def perform_create(self, serializer):
        """
        Создает комментарий к обзору.
        Автором комментария автоматически устанавливается пользователь.
        """
        serializer.save(author=self.request.user, review_id=self.get_review())

    def get_queryset(self):
        """Возвращает список комментариев к обзору."""
        return self.get_review().comments
