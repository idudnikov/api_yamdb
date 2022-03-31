from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(_('Имя категории'), max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(_('Наименование жанра'), max_length=256)
    slug = models.SlugField(_('Slug жанра'), unique=True)

    class Meta:
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')


class Title(models.Model):
    name = models.CharField(_('Название'), max_length=200, blank=False)
    year = models.DateTimeField(_('Год выпуска'), auto_now_add=True)
    rating = models.IntegerField(_('Рейтинг'), null=True)
    description = models.CharField(_('Описание'), max_length=200)
    genre = models.ManyToManyField(Genre,
                                   through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = _('Произведение')
        verbose_name_plural = _('Произведения')


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.DO_NOTHING
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.DO_NOTHING
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name=_('Произведение')
    )
    text = models.TextField(_('Текст отзыва'))
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('Автор отзыва')
    )
    score = models.IntegerField(
        _('Оценка'),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        _('Дата добавления'), auto_now_add=True
    )

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_('Автор комментария')
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name=_('Отзыв')
    )
    text = models.TextField(_('Текст комментария'))
    pub_date = models.DateTimeField(
        _('Дата добавления'), auto_now_add=True
    )

    class Meta:
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')
