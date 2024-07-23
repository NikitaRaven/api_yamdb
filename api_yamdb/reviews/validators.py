from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .constants import INVALID_YEAR


def title_year_validator(value):
    if value < 1000 or value > timezone.now().year:
        raise ValidationError(INVALID_YEAR)
