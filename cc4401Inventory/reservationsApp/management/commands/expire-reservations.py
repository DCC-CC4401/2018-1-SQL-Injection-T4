from django.core.management.base import BaseCommand, CommandError
from reservationsApp.models import Reservation
from datetime import datetime, timedelta, date
from datetime import datetime

class Command(BaseCommand):
    help = 'Corre cada hora para borrar la lista prestamos realizados'

    # def add_arguments(self, parser):
    #     parser.add_argument('id', nargs='+', type=int)

    def handle(self, *args, **options):
        delta = datetime.now() - timedelta(hours=24)
        to_reject = Reservation.objects.filter(starting_date_time__lt=delta, 
                                            state='P', 
                                            space__name__icontains='quincho')
        for res in to_reject:
            res.state = 'R'
            res.save()

            self.stdout.write(self.style.SUCCESS('Successfully rejected "%s" ' % res.space.name))