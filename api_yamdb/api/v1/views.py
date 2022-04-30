from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from reviews.models import Category, Comments, Genre, Review, Title

from .serializers import UserSerializer, SignUpSerializer, TokenSerializer
from .utils import create_confirmation_code, send_email, get_tokens_for_user
from .mixins import CreateDestroyListMixin
from .permissions import IsAdminUserOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)


class UserSignUp(APIView):
    """Регистрация новых пользователей и отправка кода подтвержения на почту."""

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


class UsersViewSet(viewsets.ModelViewSet):
    """Отображение списка пользователей и добавление новых админом."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class UserDetailViewSet(viewsets.ModelViewSet):
    """Профиль пользователя."""


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
