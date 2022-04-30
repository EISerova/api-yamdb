from django.contrib import admin

from .models import Genre, Category, Title, Review, Comment


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


admin.site.register(Genre, GenreClass)
admin.site.register(Category, CategoryClass)
admin.site.register(Title, TitleClass)
admin.site.register(Review, ReviewClass)
admin.site.register(Comment, CommentClass)
