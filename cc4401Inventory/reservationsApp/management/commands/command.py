from django.core.management.base import BaseCommand, CommandError
# from polls.models import Question as Poll

class Command(BaseCommand):
    help = 'Corre cada hora para borrar la lista prestamos realizados'

    # def add_arguments(self, parser):
    #     parser.add_argument('commmad', nargs='+', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Successfully running'))