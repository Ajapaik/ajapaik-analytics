import json

from django.contrib.gis.db.models import DateTimeField, ImageField
from django.db.models import Model, ForeignKey, PositiveSmallIntegerField, TextField, BooleanField, RESTRICT
import analytics.replica.models_ajapaik as ajapaik
from django.utils.translation import gettext as _

# MASTER MODEL
# https://github.com/Ajapaik/ajapaik-web/blob/master/ajapaik/ajapaik_face_recognition/models.py

CHILD, ADULT, ELDERLY, UNKNOWN, NOT_APPLICABLE = range(5)
AGE = (
    (CHILD, _('Child')),
    (ADULT, _('Adult')),
    (ELDERLY, _('Elderly')),
    (UNKNOWN, _('Unknown')),
    (NOT_APPLICABLE, _('Not Applicable'))
)
FEMALE, MALE, UNKNOWN, NOT_APPLICABLE = range(4)
GENDER = (
    (FEMALE, _('Female')),
    (MALE, _('Male')),
    (UNKNOWN, _('Unknown')),
    (NOT_APPLICABLE, _('Not Applicable'))
)


class FaceRecognitionRectangle(Model):
    USER, ALGORITHM, PICASA = range(3)
    ORIGIN_CHOICES = (
        (USER, _('User')),
        (ALGORITHM, _('Algorithm')),
        (PICASA, _('Picasa')),
    )

    photo = ForeignKey('Photo', related_name='face_recognition_rectangles', on_delete=RESTRICT)
    subjectPhoto = ImageField(_('SubjectPhoto'), upload_to='uploads', blank=True, null=True, max_length=255)
    subject_consensus = ForeignKey('Album', null=True, blank=True,
                                          related_name='face_recognition_crowdsourced_rectangles', on_delete=RESTRICT)
    subject_ai_suggestion = ForeignKey('Album', null=True, blank=True,
                                              related_name='face_recognition_ai_detected_rectangles', on_delete=RESTRICT)
    # If no user is attached, means OpenCV detected it
    user = ForeignKey('Profile', blank=True, null=True, related_name='face_recognition_rectangles', on_delete=RESTRICT)
    origin = PositiveSmallIntegerField(choices=ORIGIN_CHOICES, default=ALGORITHM)
    gender = PositiveSmallIntegerField(choices=GENDER, blank=True, null=True)
    age = PositiveSmallIntegerField(choices=AGE, blank=True, null=True)
    # [top, right, bottom, left]
    coordinates = TextField()
    face_encoding = TextField(null=True, blank=True)
    # Users can have it deleted, but we'll keep records in our DB in case of malice
    deleted = DateTimeField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return f'{str(self.id)} - {str(self.photo)} - {str(self.user)}'

    def decode_coordinates(self):
        return json.loads(self.coordinates)

    def get_subject_name(self):
        subject_album = self.get_subject()

        return subject_album.name if subject_album else None

    def get_subject(self):
        subject_album = None

        # Prefer what people think
        if self.subject_consensus:
            subject_album: Album = self.subject_consensus
        elif self.subject_ai_suggestion:
            subject_album: Album = self.subject_ai_suggestion

        return subject_album

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_face_recognition_facerecognitionrectangle'

class FaceRecognitionRectangleSubjectDataSuggestion(Model):
    face_recognition_rectangle = ForeignKey(FaceRecognitionRectangle,related_name='face_recognition_rectangle', on_delete=RESTRICT)
    proposer = ForeignKey('Profile', related_name='subject_data_proposer', on_delete=RESTRICT)
    gender = PositiveSmallIntegerField(choices=GENDER, null=True)
    age = PositiveSmallIntegerField(choices=AGE, null=True)
    created = DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_face_recognition_facerecognitionrectanglesubjectdatbadc'


class FaceRecognitionRectangleFeedback(Model):
    rectangle = ForeignKey(FaceRecognitionRectangle, related_name='feedback', on_delete=RESTRICT)
    user = ForeignKey('Profile', related_name='face_recognition_rectangle_feedback', on_delete=RESTRICT)
    alternative_subject = ForeignKey('Album', null=True, on_delete=RESTRICT)
    # So users could downvote bad rectangles
    is_correct = BooleanField(default=False)
    is_correct_person = BooleanField(null=True)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        string_label = ''

        if self.is_correct:
            string_label += f'Confirmed annotation {self.rectangle_id}'
        else:
            string_label += f'Rejected annotation {self.rectangle_id}'

        if self.alternative_subject is not None:
            string_label += f', alternative subject suggested: {self.alternative_subject.name}'

        return string_label

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_face_recognition_facerecognitionrectanglefeedback'

class FaceRecognitionUserSuggestion(Model):
    USER, ALGORITHM, PICASA = range(3)
    ORIGIN_CHOICES = (
        (USER, _('User')),
        (ALGORITHM, _('Algorithm')),
        (PICASA, _('Picasa')),
    )

    subject_album = ForeignKey('Album', related_name='face_recognition_suggestions', on_delete=RESTRICT)
    rectangle = ForeignKey(FaceRecognitionRectangle, related_name='face_recognition_suggestions', on_delete=RESTRICT)
    # Empty user means OpenCV recognized the face automatically
    user = ForeignKey('Profile', related_name='face_recognition_suggestions', blank=True,
                             null=True, on_delete=RESTRICT)
    origin = PositiveSmallIntegerField(choices=ORIGIN_CHOICES, default=ALGORITHM)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return f'{str(self.id)} - {str(self.rectangle_id)} - {str(self.user_id)} - {str(self.subject_album_id)}'

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_face_recognition_facerecognitionusersuggestion'













