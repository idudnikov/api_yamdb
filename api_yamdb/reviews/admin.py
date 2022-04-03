import pandas

from django.contrib import admin, messages
from django.forms import forms
from django.shortcuts import redirect, render
from django.urls import path

from users.models import CustomUser
from .models import Category, Comment, Genre, GenreTitle, Review, Title


class CSVImportFrom(forms.Form):
    csv_file = forms.FileField(label='CSV Файл')


class CustomAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv), ]
        return new_urls + urls

    def upload_csv(self, request):
        if request.method == 'POST':
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                raise messages.warning(request,
                                       'The wrong file type was uploaded')
            csv_file = pandas.read_csv(csv_file)
            self.parse_csv(csv_file)
            return redirect(request.path_info)

        form = CSVImportFrom()
        context = {'form': form}
        return render(request, 'admin/csv_upload.html', context=context)

    def parse_csv(self, csv_file):
        raise NotImplementedError(
            'You have to override this method in your successor class'
        )


class CustomCategoryAdmin(CustomAdmin):
    def parse_csv(self, csv_file):
        for row in csv_file.values:
            values = row.tolist()
            Category.objects.update_or_create(name=values[1],
                                              slug=values[2])
        return


class CustomGenreAdmin(CustomAdmin):
    def parse_csv(self, csv_file):
        for row in csv_file.values:
            values = row.tolist()
            Genre.objects.update_or_create(name=values[1],
                                           slug=values[2])
        return


class CustomTitleAdmin(CustomAdmin):
    def parse_csv(self, csv_file):
        for row in csv_file.values:
            values = row.tolist()
            Title.objects.update_or_create(
                name=values[1],
                year=values[2],
                category=Category.objects.get(id=values[3])
            )
        return


class CustomReviewAdmin(CustomAdmin):
    def parse_csv(self, csv_file):
        for row in csv_file.values:
            values = row.tolist()
            Review.objects.update_or_create(
                title=Title.objects.get(id=values[1]),
                text=values[2],
                author=CustomUser.objects.get(
                    id=values[3]),
                score=values[4],
                pub_date=values[5]
            )
        return


class CustomCommentAdmin(CustomAdmin):
    def parse_csv(self, csv_file):
        for row in csv_file.values:
            values = row.tolist()
            Comment.objects.update_or_create(
                review=Review.objects.get(id=values[1]),
                text=values[2],
                author=CustomUser.objects.get(id=values[3]),
                pub_date=values[4])
        return


class CustomGenreTitleAdmin(CustomAdmin):
    def parse_csv(self, csv_file):
        for row in csv_file.values:
            values = row.tolist()
            GenreTitle.objects.update_or_create(
                title=Title.objects.get(id=values[1]),
                genre=Genre.objects.get(id=values[2]))
        return


admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(Genre, CustomGenreAdmin)
admin.site.register(Title, CustomTitleAdmin)
admin.site.register(Review, CustomReviewAdmin)
admin.site.register(Comment, CustomCommentAdmin)
admin.site.register(GenreTitle, CustomGenreTitleAdmin)
