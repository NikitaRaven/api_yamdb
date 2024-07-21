from django.contrib import admin
from .models import Genre, Category, Title, Review, Comment, GenreTitle

admin.site.empty_value_display = 'Не задано'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category'
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
        'name',
        'year',
        'genre',
        'category'
    )
    list_display_links = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'score',
        'author',
        'text'
    )
    list_editable = (
        'score',
        'text'
    )
    search_fields = (
        'title',
        'score',
        'author'
    )
    list_filter = (
        'title',
        'score',
        'author',
    )


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(GenreTitle)

