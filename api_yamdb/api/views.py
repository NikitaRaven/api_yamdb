from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg

from reviews.models import Category, Genre, Title, Review
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer,
    CommentSerializer, ReviewSerializer
)
from .filters import TitleFilter
from .permissions import (
    CategoryGenreTitlePermission, ReviewCommentsPermission
)
from .constants import HTTP_METHODS_ALLOWED, ORDER_BY_SLUG, ORDER_BY_PUB_DATE
from .mixins import CreateListDestroySearchSlugMixin


class CategoryViewSet(CreateListDestroySearchSlugMixin):
    queryset = Category.objects.all().order_by(ORDER_BY_SLUG)
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroySearchSlugMixin):
    queryset = Genre.objects.all().order_by(ORDER_BY_SLUG)
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (CategoryGenreTitlePermission,)
    http_method_names = HTTP_METHODS_ALLOWED

    def get_queryset(self):
        return super().get_queryset().annotate(rating=Avg('reviews__score'))


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    http_method_names = HTTP_METHODS_ALLOWED
    permission_classes = (ReviewCommentsPermission,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all().order_by(ORDER_BY_PUB_DATE)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    http_method_names = HTTP_METHODS_ALLOWED
    permission_classes = (ReviewCommentsPermission,)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get("review_id"))

    def get_queryset(self):
        return self.get_review().comments.all().order_by(ORDER_BY_PUB_DATE)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=self.get_review())
