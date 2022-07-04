from django.core.management.base import BaseCommand, CommandError
from analytics.replica.models_ajapaik import Photo

# https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/

class Command(BaseCommand):
    help = 'Print coordinates of 10 first photos'

    def handle(self, *args, **options):

        photos = Photo.objects.filter(lat__isnull=False, lon__isnull=False).order_by('id')[:100]
        for photo in photos:
            print('lat: ' + str(photo.lat) + '\tlon: ' + str(photo.lon) +'\t' + str(photo))
