import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Genre, Title, Review, Comment, GenreTitle

User = get_user_model()


class Command(BaseCommand):
    help = 'Import data from a CSV file'
    def handle(self, *args, **kwargs):
        base_path = 'static/data/'
        category_csv = base_path + 'category.csv'
        genre_csv = base_path + 'genre.csv'
        titles_csv = base_path + 'titles.csv'
        genre_title_csv = base_path + 'genre_title.csv'
        users_csv = base_path + 'users.csv'
        review_csv = base_path + 'review.csv'
        comments_csv = base_path + 'comments.csv'

        try:
            with open(genre_csv, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    Genre.objects.create(
                        name=row['name'],
                        slug=row['slug'],
                    )
        except Exception:
            pass

        try:
            with open(category_csv, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    Category.objects.create(
                        name=row['name'],
                        slug=row['slug'],
                    )
        except Exception:
            pass

        try:
            with open(titles_csv, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    cur_category = Category.objects.get(pk=row['category'])
                    Title.objects.create(
                        name=row['name'],
                        year=row['year'],
                        category=cur_category,
                    )
        except Exception:
            pass

        try:
            with open(genre_title_csv, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    cur_title = Title.objects.get(pk=row['title_id'])
                    cur_genre = Genre.objects.get(pk=row['genre_id'])
                    GenreTitle.objects.create(
                        title_id=cur_title,
                        genre_id=cur_genre,
                    )
        except Exception:
            pass

        try:
            with open(users_csv, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    User.objects.create(
                        username=row['username'],
                        email=row['email'],
                        bio=row['bio'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                    )
        except Exception:
            pass

        try:
            with open(review_csv, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    cur_title = Title.objects.get(pk=row['title_id'])
                    cur_user = User.objects.get(pk=row['author'])
                    Review.objects.create(
                        title_id=cur_title,
                        text=row['text'],
                        author=cur_user,
                        score=row['score'],
                        pub_date=row['pub_date'],
                    )
        except Exception:
            pass

        try:
            with open(comments_csv, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    cur_review = Review.objects.get(pk=row['review_id'])
                    cur_user = User.objects.get(pk=row['author'])
                    Comment.objects.create(
                        review_id=cur_review,
                        text=row['text'],
                        author=cur_user,
                        pub_date=row['pub_date'],
                    )
        except Exception:
            pass



