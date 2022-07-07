from django.core.management.base import BaseCommand, CommandError
from analytics.replica_ro.models_ajapaik import Area, AlbumPhoto, Album, Photo, ImageSimilarity, ImageSimilaritySuggestion, PhotoComment, DifficultyFeedback, Points, \
    Transcription, TranscriptionFeedback, GeoTag, LocationPhoto, Location, Source, Device, Skip, Licence, GoogleMapsReverseGeocode, Dating, DatingConfirmation, \
    Video, Suggestion, PhotoSceneSuggestion, PhotoViewpointElevationSuggestion, PhotoFlipSuggestion, PhotoInvertSuggestion, PhotoRotationSuggestion, MuisCollection, AlbumVideos

from analytics.replica_ro.models_ajapaik_facerecognition import FaceRecognitionRectangle, FaceRecognitionRectangleSubjectDataSuggestion, \
    FaceRecognitionRectangleFeedback, FaceRecognitionUserSuggestion

from analytics.replica_ro.models_ajapaik_objectrecognition import ObjectDetectionModel, ObjectAnnotationClass, ObjectDetectionAnnotation,ObjectAnnotationFeedback


class Command(BaseCommand):
    help = 'Loops through all models'

#    def add_arguments(self, parser):
#        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        print("Looping through known replicated models\n")
        models = [ Area, AlbumPhoto, Album, Photo, ImageSimilarity, ImageSimilaritySuggestion, PhotoComment, DifficultyFeedback, Points,
                   Transcription, TranscriptionFeedback, GeoTag, LocationPhoto, Location, Source, Device, Skip, Licence, GoogleMapsReverseGeocode,
                   Dating, DatingConfirmation, Video, PhotoSceneSuggestion, PhotoViewpointElevationSuggestion, PhotoFlipSuggestion, PhotoInvertSuggestion,
                   PhotoRotationSuggestion, MuisCollection, AlbumVideos,\
                   \
                   # analytics.replica.models_ajapaik_facerecognition
                   FaceRecognitionRectangle, FaceRecognitionRectangleSubjectDataSuggestion, FaceRecognitionRectangleFeedback, FaceRecognitionUserSuggestion,\
                   \
                   #  analytics.replica.models_ajapaik_objectrecognition
                   ObjectDetectionModel, ObjectAnnotationClass, ObjectDetectionAnnotation,ObjectAnnotationFeedback ]


        for model in models:
            m=model.objects.first()
            print(m)
