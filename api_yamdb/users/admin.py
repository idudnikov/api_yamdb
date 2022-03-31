from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'is_active',
        'is_staff',
    )
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
