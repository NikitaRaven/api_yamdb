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

USERNAME: str = 'Имя пользователя'
EMAIL: str = 'Адрес почты'
FIRST_NAME: str = 'Имя'
LAST_NAME: str = 'Фамилия'
BIO: str = 'О себе'
ROLE: str = 'Группа'
CONFIRMATION_CODE: str = 'Код подтверждения'
USER_VERBOSE: str = 'Пользователь'
USER_VERBOSE_PLURAL: str = 'Пользователи'
