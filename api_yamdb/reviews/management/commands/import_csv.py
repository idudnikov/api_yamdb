import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.utils import (parse_csv_Category, parse_csv_Comment,
                           parse_csv_Genre, parse_csv_GenreTitle,
                           parse_csv_Review, parse_csv_Title, parse_csv_Users)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-f',
                            '--file',
                            action='store',
                            help='Input file .csv',
                            )

    def handle(self, *args, **options):
        if not options['file']:
            raise CommandError('you have to set up filepath')
        filepath = options['file']
        filename = filepath.split('/')[-1]
        if not filename.endswith('.csv'):
            raise CommandError('only .csv file allowed')
        model_name = filename.replace(
            '.csv', '').replace('_', ' ').title().replace(' ', '')
        with open(filepath, 'r', encoding='utf-8') as file:
            csv_file = csv.reader(file)
            next(csv_file)
            callbacks = {
                'Category': parse_csv_Category(csv_file, model_name),
                'Genre': parse_csv_Genre(csv_file, model_name),
                'Titles': parse_csv_Title(csv_file, model_name),
                'Review': parse_csv_Review(csv_file, model_name),
                'Comments': parse_csv_Comment(csv_file, model_name),
                'GenreTitle': parse_csv_GenreTitle(csv_file, model_name),
                'Users': parse_csv_Users(csv_file, model_name)
            }
            try:
                callbacks[model_name]
            except KeyError:
                raise CommandError(f'No model named {model_name}')
            return
