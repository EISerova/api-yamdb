from django.db.models import Avg
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .mixins import CreateDestroyListMixin
from .permissions import (IsAdmin, IsAdminUserOrReadOnly,
                          IsAuthorAdminModeratorOrReadOnly)
from .serializers import (AccountSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer, ReviewSerializer,
                          SignUpSerializer, TitleReadSerializer,
                          TitleWriteSerializer, TokenSerializer,
                          UserSerializer)
from .utils import create_confirmation_code, get_tokens_for_user, send_email


class CategoryGenreViewSet(CreateDestroyListMixin, GenericViewSet):
    """Базовый класс для CategoryViewSet и GenreViewSet."""

    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


@api_view(["POST"])
@permission_classes([AllowAny])
def user_signup(request):
    """Регистрация пользователей и отправка кода подтвержения на почту."""

    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data["email"].lower()
    username = serializer.validated_data["username"]
    confirmation_code = create_confirmation_code()

    try:
        user, created = User.objects.get_or_create(
            username=username,
            email=email,
            defaults={"confirmation_code": confirmation_code},
        )
    except IntegrityError:
        return Response(
            "Пользователь с таким именем или почтой уже существует.",
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not created:
        confirmation_code = user.confirmation_code

    send_email(email, confirmation_code, username)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def user_auth(request):
    """Получение пользователем токена."""

    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    if serializer.validated_data[
        "confirmation_code"
    ] != user.confirmation_code:
        return Response(
            serializer.data,
            status=status.HTTP_400_BAD_REQUEST
        )
    response = get_tokens_for_user(user)
    return Response(response, status=status.HTTP_200_OK)


class UsersViewSet(ModelViewSet):
    """Обработка профиля пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    permission_classes = (IsAdmin,)
    lookup_field = "username"

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=AccountSerializer,
    )
    def me(self, request):
        """Вывод профиля, добавление новых пользователей."""
        if self.request.method != "PATCH":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
    ordering = ["-rating", "name"]
    permission_classes = (IsAdminUserOrReadOnly,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Выбор сериалайзера в зависимости от типа запроса."""
        if self.action in ("list", "retrieve"):
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
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

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
        """Возвращает обзор с запрашиваемым id."""
        return get_object_or_404(
            Review,
            title_id=self.kwargs.get("title_id"),
            pk=self.kwargs.get("review_id"),
        )

    def perform_create(self, serializer):
        """
        Создает комментарий к обзору.
        Автором комментария автоматически устанавливается пользователь.
        """
        serializer.save(
            author=self.request.user,
            review_id=self.get_review().id
        )

    def get_queryset(self):
        """Возвращает список комментариев к обзору."""
        return self.get_review().comments.all()
