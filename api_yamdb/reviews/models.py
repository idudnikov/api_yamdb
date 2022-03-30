from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_('Имя категории'), max_length=256)
    slug = models.SlugField(max_length=50)
