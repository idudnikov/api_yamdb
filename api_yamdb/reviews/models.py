from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_('Имя категории'), max_length=256)
    slug = models.SlugField(max_length=50)


class Genre(models.Model):
    name = models.CharField('Наименование жанра', max_length=256)
    slug = models.SlugField('Slug жанра', unique=True)
