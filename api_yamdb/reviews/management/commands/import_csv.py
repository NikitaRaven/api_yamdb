import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class Command(BaseCommand):
    help = 'Import data from a CSV file'

    def handle(self, *args, **kwargs):
        base_path = 'static/data/'
        data_files = (
            ('category.csv', Category, ('id', 'name', 'slug')),
            ('genre.csv', Genre, ('id', 'name', 'slug')),
            ('titles.csv', Title, ('id', 'name', 'year', 'category')),
            ('users.csv', User, (
                'id',
                'username',
                'email',
                'role',
                'bio',
                'first_name',
                'last_name'
            )),
            ('review.csv', Review,
             ('id', 'title', 'text', 'author', 'score', 'pub_date')),
            ('comments.csv', Comment,
             ('id', 'review', 'text', 'author', 'pub_date')),
        )
        related_fields = {
            'author': User,
            'title': Title,
            'review': Review,
            'category': Category,
        }

        for file_name, model, fields in data_files:
            file_path = base_path + file_name
            try:
                with open(file_path, 'r') as file:
                    csv_reader = csv.DictReader(file)

                    for row in csv_reader:
                        data = {field:
                                row[field] if field not in related_fields
                                else related_fields[field].objects.get(
                                    pk=row[field + '_id']
                                    if model in (Review, Comment)
                                    and field in ('review', 'title')
                                    else row[field]) for field in fields}
                        model.objects.create(**data)

            except Exception as e:
                print(f'Ошибка при импорте данных: {e}')

        try:
            file_path = base_path + 'genre_title.csv'
            with open(file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    title = Title.objects.get(pk=row['title_id'])
                    genre = Genre.objects.get(pk=row['genre_id'])
                    title.genre.add(genre)
        except Exception as e:
            print(f'Ошибка при импорте данных: {e}')