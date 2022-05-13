from django.core.management.base import BaseCommand, CommandError
from .csfd_scrapper import CSFDscrapper

class Command(BaseCommand):
    help = 'Loads movies and actors into the sqlite database'

    def add_arguments(self, parser):
        parser.add_argument('number_of_movies', nargs='+', type=int)

    def handle(self, *args, **options):
        scrapper = CSFDscrapper()
        try:
            scrapper.load_db(options['number_of_movies'][0])
        except Exception as e:
            print(e)
        print("Successfully loaded DB with data")
