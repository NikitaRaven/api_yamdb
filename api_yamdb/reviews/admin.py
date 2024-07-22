from django.contrib import admin

from .models import Genre, Category, Title, Review, Comment, GenreTitle

admin.site.empty_value_display = 'Не задано'


class GenreTitleInline(admin.StackedInline):
    model = GenreTitle
    extra = 0


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0


class TitleInline(admin.StackedInline):
    model = Title
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class TitleAdmin(admin.ModelAdmin):
    inlines = (
        GenreTitleInline,
        ReviewInline,
    )
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    list_editable = (
        'year',
        'description',
        'category'
    )
    search_fields = (
        'name',
        'year',
        'description',
        'genre',
        'category'
    )
    list_filter = (
        'year',
        'genre',
        'category'
    )
    list_display_links = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    inlines = (
        CommentInline,
    )
    list_display = (
        'title',
        'score',
        'author',
        'text'
    )
    list_editable = (
        'author',
        'score',
        'text'
    )
    search_fields = (
        'title',
        'score',
        'author'
    )
    list_filter = (
        'score',
        'author',
        'pub_date',
    )


class GenreCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    list_editable = (
        'slug',
    )
    search_fields = (
        'name',
    )


class GenreAdmin(GenreCategoryAdmin):
    inlines = (
        GenreTitleInline,
    )


class CategoryAdmin(GenreCategoryAdmin):
    inlines = (
        TitleInline,
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'review',
        'author',
        'pub_date'
    )
    list_editable = (
        'review',
        'author',
    )
    search_fields = (
        'text',
        'review',
        'author'
    )
    list_filter = (
        'author',
        'pub_date',
    )


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
