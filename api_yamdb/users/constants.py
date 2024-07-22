NAME_LENGTH: int = 150
MAIL_LENGTH: int = 254
CODE_LENGTH: int = 10
ROLE_LENGTH: int = 9
USER: str = 'user'
MODERATOR: str = 'moderator'
ADMIN: str = 'admin'
ROLE_CHOICES: tuple = (
    (USER, 'User'),
    (MODERATOR, 'Moderator'),
    (ADMIN, 'admin'),
)

VERBOSE_NAME_USERNAME: str = 'имя пользователя'
VERBOSE_NAME_EMAIL: str = 'адрес почты'
VERBOSE_NAME_FIRST_NAME: str = 'имя'
VERBOSE_NAME_LAST_NAME: str = 'фамилия'
VERBOSE_NAME_BIO: str = 'о себе'
VERBOSE_NAME_ROLE: str = 'группа'
VERBOSE_NAME_CONFIRMATION_CODE: str = 'код подтверждения'
CUSTOM_USER_VERBOSE: str = 'пользователь'
CUSTOM_USER_VERBOSE_PLURAL: str = 'пользователи'
