from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status, generics
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .mixins import CreateDestroyListMixin
from .permissions import (
    IsAdminUserOrReadOnly,
    ReviewCommentPermission,
    IsAdmin,
    IsOwnerOfProfile,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    UserDetailSerializer,
    SignUpSerializer,
    TokenSerializer,
)
from .utils import create_confirmation_code, send_email, get_tokens_for_user


class UserSignUp(APIView):
    """
    Регистрация новых пользователей и отправка кода подтвержения на почту.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=False):
            confirmation_code = create_confirmation_code()
            email = serializer.validated_data['email']
            name = serializer.validated_data['username']
            serializer.save(confirmation_code=confirmation_code)
            send_email(email, confirmation_code, name)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuth(generics.CreateAPIView):
    """Получение пользователем токена."""

    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return get_object_or_404(User, username=self.request.user)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        response = get_tokens_for_user(user)
        return Response(response, status=status.HTTP_200_OK)


class UsersViewSet(ModelViewSet):
    """Отображение списка пользователей, профиля и добавление новых админом."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    permission_classes = (IsAdmin,)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsOwnerOfProfile,),
        serializer_class=UserDetailSerializer,
    )
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if self.request.method == 'PATCH':
            self.partial_update(request)
            request.user.refresh_from_db()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


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
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))

    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    """Обрабатывает запрос к обзорам."""

    serializer_class = ReviewSerializer

    permission_classes = (ReviewCommentPermission,)

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
        return self.get_title().reviews.all()


class CommentViewSet(ModelViewSet):
    """Обрабатывает запрос к комментариям."""

    serializer_class = CommentSerializer

    permission_classes = (ReviewCommentPermission,)

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
        serializer.save(
            author=self.request.user, review_id=self.get_review().id
        )

    def get_queryset(self):
        """Возвращает список комментариев к обзору."""
        return self.get_review().comments.all()
