from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from .serializers import UserSerializer, SignUpSerializer, TokenSerializer
from .utils import create_confirmation_code, send_email, get_tokens_for_user


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

    pass
