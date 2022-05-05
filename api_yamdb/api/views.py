from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .mixins import CreateDestroyListMixin
from .permissions import (
    IsAdmin,
    IsAdminUserOrReadOnly,
    IsAuthorAdminModeratorOrReadOnly,
)
from .serializers import (
    AccountSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    TokenSerializer,
    UserSerializer,
)
from .utils import (
    create_confirmation_code,
    get_tokens_for_user,
    get_user,
    send_email,
    check_username_email
)


class CategoryGenreViewSet(CreateDestroyListMixin, GenericViewSet):
    """Базовый класс для CategoryViewSet и GenreViewSet."""

    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class UserSignUp(APIView):
    """
    Регистрация новых пользователей и отправка кода подтвержения на почту.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']

        user = get_user(username, email)

        if user:
            confirmation_code = user.confirmation_code
            send_email(email, confirmation_code, username)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if check_username_email(username, email):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        confirmation_code = create_confirmation_code()
        serializer.validated_data['email'] = email.lower()

        serializer.save(confirmation_code=confirmation_code)
        send_email(email, confirmation_code, username)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        if request.data['confirmation_code'] != user.confirmation_code:
            return Response(
                serializer.data, status=status.HTTP_400_BAD_REQUEST
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
        permission_classes=(IsAuthenticated,),
        serializer_class=AccountSerializer,
    )
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.partial_update(request)
            request.user.refresh_from_db()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class CategoryViewSet(CategoryGenreViewSet):
    """Обрабатывает запрос к категориям."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    """Обрабатывает запрос к жанрам."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """Обрабатывает запрос к произведениям."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    ordering = ['-rating', 'name']
    permission_classes = (IsAdminUserOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    """Обрабатывает запрос к обзорам."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorAdminModeratorOrReadOnly,
    )

    def get_title(self):
        """Получает из запроса объект Title."""
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        """
        Создает обзор к произведению.
        Автором обзора автоматически устанавливается пользователь.
        """
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        """Возвращает список обзоров к произведению."""
        return self.get_title().reviews.all()


class CommentViewSet(ModelViewSet):
    """Обрабатывает запрос к комментариям."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorAdminModeratorOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )

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
