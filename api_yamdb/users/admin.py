from django.contrib import admin
from reviews.admin import CustomAdmin

from .models import CustomUser


class CustomUserAdmin(CustomAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'is_active',
        'is_staff',
    )
    ordering = ('username',)

    def parse_csv(self, csv_file):
        for row in csv_file.values:
            values = row.tolist()
            CustomUser.objects.update_or_create(id=values[0],
                                                username=values[1],
                                                email=values[2],
                                                role=values[3],
                                                bio=values[4],
                                                first_name=values[5],
                                                last_name=values[6])
        return


admin.site.register(CustomUser, CustomUserAdmin)
