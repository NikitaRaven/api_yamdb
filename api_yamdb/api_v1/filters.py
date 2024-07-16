import django_filters

from reviews.models import Title, Category, Genre


class TitleFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        field_name="category",
        to_field_name='slug',
        queryset=Category.objects.all()
    )
    genre = django_filters.ModelChoiceFilter(
        field_name="genre",
        to_field_name='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
