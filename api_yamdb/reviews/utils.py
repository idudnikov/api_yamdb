import sys

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import CustomUser


def parse_csv_Category(csv_file, model_name):
    if model_name == 'Category':
        for row in csv_file:
            Category.objects.update_or_create(name=row[1],
                                              slug=row[2])
        sys.stdout.write(f'Successfully imported {model_name}\n')
    return


def parse_csv_Genre(csv_file, model_name):
    if model_name == 'Genre':
        for row in csv_file:
            Genre.objects.update_or_create(name=row[1],
                                           slug=row[2])
        sys.stdout.write(f'Successfully imported {model_name}\n')
    return


def parse_csv_Title(csv_file, model_name):
    if model_name == 'Titles':
        for row in csv_file:
            Title.objects.update_or_create(
                name=row[1],
                year=row[2],
                category=Category.objects.get(id=row[3])
            )
        sys.stdout.write(f'Successfully imported {model_name}\n')
    return


def parse_csv_Review(csv_file, model_name):
    if model_name == 'Review':
        for row in csv_file:
            Review.objects.update_or_create(
                title=Title.objects.get(id=row[1]),
                text=row[2],
                author=CustomUser.objects.get(
                    id=row[3]),
                score=row[4],
                pub_date=row[5])
        sys.stdout.write(f'Successfully imported {model_name}\n')
    return


def parse_csv_Comment(csv_file, model_name):
    if model_name == 'Comments':
        for row in csv_file:
            Comment.objects.update_or_create(
                review=Review.objects.get(id=row[1]),
                text=row[2],
                author=CustomUser.objects.get(id=row[3]),
                pub_date=row[4])
        sys.stdout.write(f'Successfully imported {model_name}\n')
    return


def parse_csv_GenreTitle(csv_file, model_name):
    if model_name == 'GenreTitle':
        for row in csv_file:
            GenreTitle.objects.update_or_create(
                title=Title.objects.get(id=row[1]),
                genre=Genre.objects.get(id=row[2]))
        sys.stdout.write(f'Successfully imported {model_name}\n')
    return


def parse_csv_Users(csv_file, model_name):
    if model_name == 'Users':
        for row in csv_file:
            CustomUser.objects.update_or_create(id=row[0], username=row[1],
                                                email=row[2], role=row[3],
                                                bio=row[4], first_name=row[5],
                                                last_name=row[6])
        sys.stdout.write(f'Successfully imported {model_name}\n')
    return
