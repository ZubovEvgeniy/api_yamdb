from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from core.models import CreatedModel
from reviews.validators import validate_year

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

CHOICES = (
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Админ'),
    (USER, 'Пользователь')
)


class User(AbstractUser):
    """Модель пользователя."""
    email = models.EmailField(
        verbose_name='Почта',
        unique=True
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='Роли',
        max_length=30,
        default=USER,
        choices=CHOICES
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user')
        ]

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель категории."""
    name = models.CharField(
        verbose_name='Категория',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""
    name = models.CharField(
        verbose_name='Жанр',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        verbose_name='Имя произведения',
        max_length=200
    )
    year = models.PositiveIntegerField(
        validators=[validate_year],
        verbose_name='Год',
        db_index=True
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель Произведения и жанры."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'


class Review(CreatedModel):
    """Модель отзывов."""
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='reviews',
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        related_name='reviews',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        verbose_name='Оценка'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(CreatedModel):
    """Модель комментария."""
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='comments',
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Текст нового комментария'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
