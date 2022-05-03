from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class GenreClass(admin.ModelAdmin):
    """Админка жанров."""

    list_display = (
        'pk',
        'slug',
        'name',
    )
    list_editable = (
        'slug',
        'name',
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class CategoryClass(admin.ModelAdmin):
    """Админка категорий."""

    list_display = (
        'pk',
        'slug',
        'name',
    )
    list_editable = (
        'slug',
        'name',
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class TitleClass(admin.ModelAdmin):
    """Админка произведений."""

    list_display = (
        'pk',
        'name',
        'description',
        'year',
        'category',
    )
    list_filter = (
        'year',
        'category',
        'genre',
    )
    list_editable = (
        'name',
        'description',
        'year',
    )
    search_fields = (
        'year',
        'category',
        'genre',
    )
    empty_value_display = '-пусто-'


class ReviewClass(admin.ModelAdmin):
    """Админка обзоров."""

    list_display = (
        'pk',
        'text',
        'title_id',
        'author',
        'score',
        'pub_date',
    )
    list_filter = (
        'title_id',
        'author',
        'pub_date',
    )
    list_editable = ('text',)
    search_fields = (
        'title',
        'author',
        'pub_date',
    )
    empty_value_display = '-пусто-'


class CommentClass(admin.ModelAdmin):
    """Админка комментов."""

    list_display = (
        'pk',
        'text',
        'review',
        'author',
        'pub_date',
    )
    list_filter = (
        'review',
        'author',
        'pub_date',
    )
    list_editable = ('text',)
    search_fields = (
        'review',
        'author',
        'pub_date',
    )
    empty_value_display = '-пусто-'


class UserClass(admin.ModelAdmin):
    """Админка юзеров."""

    list_display = (
        'id',
        'password',
        'last_login',
        'is_superuser',
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'bio',
        'email',
        'role',
    )
    list_filter = (
        'role',
        'last_login',
    )
    list_editable = (
        'password',
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'bio',
        'email',
        'role',
    )
    search_fields = (
        'username',
        'email',
        'role',
    )
    empty_value_display = '-пусто-'


admin.site.register(Genre, GenreClass)
admin.site.register(Category, CategoryClass)
admin.site.register(Title, TitleClass)
admin.site.register(Review, ReviewClass)
admin.site.register(Comment, CommentClass)
admin.site.register(User, UserClass)
