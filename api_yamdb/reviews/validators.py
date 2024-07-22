from datetime import datetime

from rest_framework.exceptions import ValidationError

from .constants import INVALID_YEAR


def title_year_validator(value):
    if value < 1000 or value > datetime.now().year:
        raise ValidationError(INVALID_YEAR)
