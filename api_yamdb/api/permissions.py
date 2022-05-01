from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin()
        return False


class ReviewCommentPermission(BasePermission):
    """
    Класс для ограничения доступа к отзывам и комментариям.
    Если запрос безопасный - доступ разрешен,
    небезопасные запросы доступны только администрации или автору.
    """

    message = 'Нет прав для изменения/удаления отзывы или комментария.'

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Проверяет тип запроса на безопасность.
        Если запрос небезопасный - проверяет,
        что запрос сделан автором или администрацией.
        """
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin()
            or request.user.is_moderator()
        )


class IsOwnerOfProfile(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_admin()
        return False