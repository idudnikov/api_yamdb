from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_('Имя категории'), max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('Наименование жанра', max_length=256)
    slug = models.SlugField('Slug жанра', unique=True)


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


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.DO_NOTHING
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.DO_NOTHING
    )
