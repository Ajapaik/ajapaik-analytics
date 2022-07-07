from django.core.management.base import BaseCommand, CommandError
from analytics.replica_ro.models_ajapaik import Photo

# https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/

class Command(BaseCommand):
    help = 'Print coordinates and urls of 10 first photos'

    def handle(self, *args, **options):

        photos = Photo.objects.filter(lat__isnull=False, lon__isnull=False).order_by('id')[:10]
        for photo in photos:
            print(str(photo))
            print('* lat: ' + str(photo.lat) + '\tlon: ' + str(photo.lon))
            print('* IIIF manifest: ' + photo.get_iiif_manifest_url)
            print('* IIIF image server: ' + photo.get_iiif_image_url)
            print('* Thumbnail: ' + photo.get_thumbnail_url)
            print('* Full image (url): ' + photo.get_full_image_url)
            print('* Full image (on analytics disk): ' + photo.get_full_image_path)
            print('')
