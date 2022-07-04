# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.gis.db.models import Model, CharField, FloatField, FileField, URLField, BigIntegerField, PositiveIntegerField, PositiveSmallIntegerField, DateTimeField, SlugField, TextField, BooleanField, ManyToManyField, PointField, IntegerField, DateField, ImageField, ForeignKey, RESTRICT, Index, F
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext as _
from django_extensions.db.fields import json
from datetime import datetime
import analytics.replica.models_ajapaik_facerecognition as fr

#import FaceRecognitionRectangle, FaceRecognitionRectangleSubjectDataSuggestion, \
#    FaceRecognitionRectangleFeedback, FaceRecognitionUserSuggestion


#from django.contrib.gis.db.models import Model, TextField, FloatField, CharField, BooleanField, BigIntegerField, \
#    ForeignKey, IntegerField, DateTimeField, ImageField, URLField, ManyToManyField, SlugField, \
#    PositiveSmallIntegerField, PointField, Manager, PositiveIntegerField

# Master file for models
# https://github.com/Ajapaik/ajapaik-web/blob/master/ajapaik/ajapaik/models.py

# Pretty much unused
class Area(Model):
    name = CharField(max_length=255) # Multilingual
    lat = FloatField(null=True)
    lon = FloatField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'project_area'

class AlbumPhoto(Model):
    CURATED, RECURATED, MANUAL, STILL, UPLOADED, FACE_TAGGED, COLLECTION = range(7)
    TYPE_CHOICES = (
        (CURATED, 'Curated'),
        (RECURATED, 'Re-curated'),
        (MANUAL, 'Manual'),
        (STILL, 'Still'),
        (UPLOADED, 'Uploaded'),
        (FACE_TAGGED, 'Face tagged'),
        (COLLECTION, 'Collection')
    )

    album = ForeignKey('Album', on_delete=RESTRICT)
    photo = ForeignKey('Photo', related_name='albumphoto', on_delete=RESTRICT)
    profile = ForeignKey('Profile', blank=True, null=True, related_name='album_photo_links', on_delete=RESTRICT)
    type = PositiveSmallIntegerField(choices=TYPE_CHOICES, default=MANUAL, db_index=True)
    created = DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_albumphoto'

class Album(Model):
    CURATED, FAVORITES, AUTO, PERSON, COLLECTION = range(5)
    TYPE_CHOICES = (
        (CURATED, 'Curated'),
        (FAVORITES, 'Favorites'),
        (AUTO, 'Auto'),
        (PERSON, 'Person'),
        (COLLECTION, 'Collection')
    )

    FEMALE, MALE = range(2)
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
    )

    name = CharField(_('Name'), max_length=255, db_index=True)
    slug = SlugField(null=True, blank=True, max_length=255)
    description = TextField(_('Description'), null=True, blank=True, max_length=2047)
    subalbum_of = ForeignKey('self', blank=True, null=True, related_name='subalbums', on_delete=RESTRICT)
    atype = PositiveSmallIntegerField(choices=TYPE_CHOICES)
    profile = ForeignKey('Profile', related_name='albums', blank=True, null=True, on_delete=RESTRICT)
    is_public = BooleanField(_('Is public'), default=True)
    open = BooleanField(_('Is open'), default=False)
    ordered = BooleanField(default=False)
    photos = ManyToManyField('Photo', through='AlbumPhoto', related_name='albums')
    videos = ManyToManyField('Video', related_name='albums', blank=True)
    # Why do albums have coordinates anyway?
    lat = FloatField(null=True, blank=True, db_index=True)
    lon = FloatField(null=True, blank=True, db_index=True)
    geography = PointField(srid=4326, null=True, blank=True, geography=True, spatial_index=True)
    cover_photo = ForeignKey('Photo', null=True, blank=True, on_delete=RESTRICT)
    cover_photo_flipped = BooleanField(default=False)
    photo_count_with_subalbums = IntegerField(default=0)
    rephoto_count_with_subalbums = IntegerField(default=0)
    geotagged_photo_count_with_subalbums = IntegerField(default=0)
    comments_count_with_subalbums = IntegerField(default=0)
    is_film_still_album = BooleanField(default=False)
    date_of_birth = DateField(blank=True, null=True)
    gender = PositiveSmallIntegerField(_('Gender'), choices=GENDER_CHOICES, blank=True, null=True)
    is_public_figure = BooleanField(default=False)
    wikidata_qid = CharField(_('Wikidata identifier'), max_length=255, blank=True, null=True)
    face_encodings = TextField(blank=True, null=True)
    created = DateTimeField(auto_now_add=True, db_index=True)
    modified = DateTimeField(auto_now=True)
    similar_photo_count_with_subalbums = IntegerField(default=0)
    confirmed_similar_photo_count_with_subalbums = IntegerField(default=0)
    source = ForeignKey('Source', null=True, blank=True, on_delete=RESTRICT)
    name_original_language = CharField(_('Name original language'), max_length=255, blank=True, null=True)
    muis_person_ids = ArrayField(IntegerField(blank=True), default=list, null=True, blank=True)

    original_lat = None
    original_lon = None

    as_json = None

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_album'

    def __str__(self):
        if self.as_json:
            return json.dumps({
                'name': self.name,
                'gender': self.gender
            })

        if self.atype == Album.PERSON and self.date_of_birth:
            return f'{self.name} ({_("b.")} {str(self.date_of_birth)})'

        return self.name

    @property
    def get_album_type(self):
        if self.is_film_still_album:
            return 'Film'
        return Album.TYPE_CHOICES[self.atype][1]

class Photo(Model):
#    objects = EstimatedCountManager()

    # Removed sorl ImageField because of https://github.com/mariocesar/sorl-thumbnail/issues/295
    image = ImageField(_('Image'), upload_to='uploads', blank=True, null=True, max_length=255, height_field='height',
                       width_field='width')
    image_unscaled = ImageField(upload_to='uploads', blank=True, null=True, max_length=255)
    image_no_watermark = ImageField(upload_to='uploads', blank=True, null=True, max_length=255)
    height = IntegerField(null=True, blank=True)
    width = IntegerField(null=True, blank=True)
    aspect_ratio = FloatField(null=True, blank=True)
    flip = BooleanField(null=True)
    invert = BooleanField(null=True)
    stereo = BooleanField(null=True)
    # In degrees
    rotated = IntegerField(null=True, blank=True)
    date = DateTimeField(null=True, blank=True)
    date_text = CharField(max_length=255, blank=True, null=True)
    title = TextField(_('Title'), null=True, blank=True)
    description = TextField(_('Description'), null=True, blank=True)
    muis_title = TextField(_('MUIS title'), null=True, blank=True)
    muis_comment = TextField(_('MUIS comment'), null=True, blank=True)
    muis_event_description_set_note = TextField(_('MUIS event description set note'), null=True, blank=True)
    muis_text_on_object = TextField(_('MUIS text on object'), null=True, blank=True)
    muis_legends_and_descriptions = TextField(_('MUIS legends and descriptions'), null=True, blank=True)
    muis_update_time = DateTimeField(null=True, blank=True)
    author = CharField(_('Author'), null=True, blank=True, max_length=255)
    uploader_is_author = BooleanField(default=False)
    licence = ForeignKey('Licence', null=True, blank=True, on_delete=RESTRICT)
    # Basically keywords describing medium
    types = CharField(max_length=255, blank=True, null=True)
    keywords = TextField(null=True, blank=True)
    # Legacy field name, actually profile
    user = ForeignKey('Profile', related_name='photos', blank=True, null=True, on_delete=RESTRICT)
    # Unused, was set manually for some of the very earliest photos
    level = PositiveSmallIntegerField(default=0)
    suggestion_level = FloatField(default=3)
    lat = FloatField(null=True, blank=True, validators=[MinValueValidator(-85.05115), MaxValueValidator(85)],
                     db_index=True)
    lon = FloatField(null=True, blank=True, validators=[MinValueValidator(-180), MaxValueValidator(180)],
                     db_index=True)
    geography = PointField(srid=4326, null=True, blank=True, geography=True, spatial_index=True)
    # Should effectively lock the location
    bounding_circle_radius = FloatField(null=True, blank=True)
    address = CharField(max_length=255, blank=True, null=True)
    azimuth = FloatField(null=True, blank=True)
    confidence = FloatField(default=0, null=True, blank=True)
    azimuth_confidence = FloatField(default=0, null=True, blank=True)
    source_key = CharField(max_length=100, null=True, blank=True)
    external_id = CharField(max_length=100, null=True, blank=True)
    external_sub_id = CharField(max_length=100, null=True, blank=True)
    source_url = URLField(null=True, blank=True, max_length=1023)
    source = ForeignKey('Source', null=True, blank=True, on_delete=RESTRICT)
    device = ForeignKey('Device', null=True, blank=True, on_delete=RESTRICT)
    # Useless
    area = ForeignKey('Area', related_name='areas', null=True, blank=True, on_delete=RESTRICT)
    rephoto_of = ForeignKey('self', blank=True, null=True, related_name='rephotos', on_delete=RESTRICT)
    first_rephoto = DateTimeField(null=True, blank=True)
    latest_rephoto = DateTimeField(null=True, blank=True)
    rephoto_count = IntegerField(default=0, db_index=True)
    fb_object_id = CharField(max_length=255, null=True, blank=True)
    comment_count = IntegerField(default=0, null=True, blank=True, db_index=True)
    first_comment = DateTimeField(null=True, blank=True)
    latest_comment = DateTimeField(null=True, blank=True)
    view_count = PositiveIntegerField(default=0)
    first_view = DateTimeField(null=True)
    latest_view = DateTimeField(null=True)
    like_count = IntegerField(default=0, db_index=True)
    first_like = DateTimeField(null=True, blank=True)
    latest_like = DateTimeField(null=True, blank=True)
    geotag_count = IntegerField(default=0, db_index=True)
    first_geotag = DateTimeField(null=True, blank=True)
    latest_geotag = DateTimeField(null=True, blank=True)
    dating_count = IntegerField(default=0, db_index=True)
    first_dating = DateTimeField(null=True, blank=True)
    latest_dating = DateTimeField(null=True, blank=True)
    transcription_count = IntegerField(default=0, db_index=True)
    first_transcription = DateTimeField(null=True, blank=True)
    latest_transcription = DateTimeField(null=True, blank=True)
    annotation_count = IntegerField(default=0, db_index=True)
    first_annotation = DateTimeField(null=True, blank=True)
    latest_annotation = DateTimeField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True, db_index=True)
    modified = DateTimeField(auto_now=True)
    gps_accuracy = FloatField(null=True, blank=True)
    gps_fix_age = FloatField(null=True, blank=True)
    # Old picture's zoom level (float [0.5, 4.0])
    cam_scale_factor = FloatField(null=True, blank=True, validators=[MinValueValidator(0.5), MaxValueValidator(4.0)])
    # yaw, pitch, roll: phone orientation (float radians)
    cam_yaw = FloatField(null=True, blank=True)
    cam_pitch = FloatField(null=True, blank=True)
    cam_roll = FloatField(null=True, blank=True)
    video = ForeignKey('Video', null=True, blank=True, related_name='stills', on_delete=RESTRICT)
    video_timestamp = IntegerField(null=True, blank=True)
    face_detection_attempted_at = DateTimeField(null=True, blank=True, db_index=True)
    perceptual_hash = BigIntegerField(null=True, blank=True)
    has_similar = BooleanField(default=False)
    similar_photos = ManyToManyField('self', through='ImageSimilarity', symmetrical=False)
    back_of = ForeignKey('self', blank=True, null=True, related_name='back', on_delete=RESTRICT)
    front_of = ForeignKey('self', blank=True, null=True, related_name='front', on_delete=RESTRICT)
    INTERIOR, EXTERIOR = range(2)
    SCENE_CHOICES = (
        (INTERIOR, _('Interior')),
        (EXTERIOR, _('Exterior'))
    )
    scene = PositiveSmallIntegerField(_('Scene'), choices=SCENE_CHOICES, blank=True, null=True)
    GROUND_LEVEL, RAISED, AERIAL = range(3)
    VIEWPOINT_ELEVATION_CHOICES = (
        (GROUND_LEVEL, _('Ground')),
        (RAISED, _('Raised')),
        (AERIAL, _('Aerial'))
    )
    viewpoint_elevation = PositiveSmallIntegerField(_('Viewpoint elevation'), choices=VIEWPOINT_ELEVATION_CHOICES,
                                                    blank=True, null=True)
    description_original_language = CharField(_('Description original language'), max_length=255, blank=True, null=True)

    original_lat = None
    original_lon = None

    class Meta:
        managed = False
        read_only_model = True
        ordering = ['-id']
        db_table = 'project_photo'
        indexes = [
            Index(F('latest_annotation').desc(nulls_last=True), name='latest_annotation_idx'),
            Index(F('first_annotation').asc(nulls_last=True), name='first_annotation_idx'),
            Index(F('latest_transcription').desc(nulls_last=True), name='latest_transcription_idx'),
            Index(F('first_transcription').asc(nulls_last=True), name='first_transcription_idx'),
            Index(F('latest_dating').desc(nulls_last=True), name='latest_dating_idx'),
            Index(F('first_dating').asc(nulls_last=True), name='first_dating_idx'),
            Index(F('latest_geotag').desc(nulls_last=True), name='latest_geotag_idx'),
            Index(F('first_geotag').asc(nulls_last=True), name='first_geotag_idx'),
            Index(F('latest_like').desc(nulls_last=True), name='latest_like_idx'),
            Index(F('first_like').asc(nulls_last=True), name='first_like_idx'),
            Index(F('latest_view').desc(nulls_last=True), name='latest_view_idx'),
            Index(F('first_view').asc(nulls_last=True), name='first_view_idx'),
            Index(F('latest_comment').desc(nulls_last=True), name='latest_comment_idx'),
            Index(F('first_comment').asc(nulls_last=True), name='first_comment_idx'),
            Index(F('latest_rephoto').desc(nulls_last=True), name='latest_rephoto_idx'),
            Index(F('first_rephoto').asc(nulls_last=True), name='first_rephoto_idx'),
        ]
    @property
    def get_iiif_manifest_url(self):
        return 'https://ajapaik.ee/photo/' + str(self.id) + '/v2/manifest.json' 

    @property
    def get_iiif_image_url(self):
        prefix='uploads/'
        imagepath=str(self.image)
        if imagepath.startswith(prefix):
            imagepath=imagepath[len(prefix):]
        return 'https://ajapaik.ee/iiif/work/iiif/ajapaik/' + imagepath + '.tif/full/max/0/default.jpg' 

    @property
    def get_thumbnail_url(self):
        return 'https://ajapaik.ee/photo-thumb/'+ str(self.id) +'/400/' 

    @property
    def get_full_image_url(self):
        return 'https://ajapaik.ee/media/'+ str(self.image)

    @property
    def get_full_image_path(self):
        return '/storage/ajapaik_media/'+ str(self.image)

    @property
    def get_display_text(self):
        if self.title:
            return self.title
        elif self.description:
            return self.description
        elif self.muis_title:
            return self.muis_title
        elif self.muis_comment:
            return self.muis_comment
        elif self.muis_event_description_set_note:
            return self.muis_event_description_set_note
        else:
            return None

    def get_absolute_url(self):
        return reverse('photo', args=(self.id, self.get_pseudo_slug()))

    def get_pseudo_slug(self):
        if self.get_display_text is not None and self.get_display_text != '':
            slug = '-'.join(slugify(self.get_display_text).split('-')[:6])[:60]
        elif self.source_key is not None and self.source_key != '':
            slug = slugify(self.source_key)
        else:
            slug = slugify(self.created.__format__('%Y-%m-%d'))

    def __str__(self):
        return f'{str(self.get_display_text)}' + ' (' + str(self.pk) + ')' 

class ImageSimilarity(Model):
    from_photo = ForeignKey(Photo, related_name='from_photo', on_delete=RESTRICT)
    to_photo = ForeignKey(Photo, related_name='to_photo', on_delete=RESTRICT)
    confirmed = BooleanField(default=False)
    DIFFERENT, SIMILAR, DUPLICATE = range(3)
    SIMILARITY_TYPES = (
        (DIFFERENT, _('Different')),
        (SIMILAR, _('Similar')),
        (DUPLICATE, _('Duplicate'))
    )
    similarity_type = PositiveSmallIntegerField(choices=SIMILARITY_TYPES, blank=True, null=True)
    user_last_modified = ForeignKey('Profile', related_name='user_last_modified', null=True, on_delete=RESTRICT)
    created = DateTimeField(auto_now_add=True, db_index=True)
    modified = DateTimeField(auto_now=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_imagesimilarity'

class ImageSimilaritySuggestion(Model):
    image_similarity = ForeignKey(ImageSimilarity, related_name='image_similarity', on_delete=RESTRICT)
    proposer = ForeignKey('Profile', related_name='image_similarity_proposer', null=True, blank=True, on_delete=RESTRICT)
    DIFFERENT, SIMILAR, DUPLICATE = range(3)
    SIMILARITY_TYPES = (
        (DIFFERENT, _('Different')),
        (SIMILAR, _('Similar')),
        (DUPLICATE, _('Duplicate'))
    )
    similarity_type = PositiveSmallIntegerField(choices=SIMILARITY_TYPES, blank=True, null=True)
    created = DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_imagesimilaritysuggestion'

class PhotoMetadataUpdate(Model):
    photo = ForeignKey('Photo', related_name='metadata_updates', on_delete=RESTRICT)
    old_title = CharField(max_length=255, blank=True, null=True)
    new_title = CharField(max_length=255, blank=True, null=True)
    old_description = TextField(null=True, blank=True)
    new_description = TextField(null=True, blank=True)
    old_author = CharField(null=True, blank=True, max_length=255)
    new_author = CharField(null=True, blank=True, max_length=255)
    created = DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_photometadataupdate'

class PhotoComment(Model):
    photo = ForeignKey('Photo', related_name='comments', on_delete=RESTRICT)
    fb_comment_id = CharField(max_length=255, unique=True)
    fb_object_id = CharField(max_length=255)
    fb_comment_parent_id = CharField(max_length=255, blank=True, null=True)
    fb_user_id = CharField(max_length=255)
    text = TextField()
    created = DateTimeField()

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_photocomment'

    def __str__(self):
        return f'{self.text[:50]}'

class DifficultyFeedback(Model):
    photo = ForeignKey('Photo', on_delete=RESTRICT)
    user_profile = ForeignKey('Profile', related_name='difficulty_feedbacks', on_delete=RESTRICT)
    level = PositiveSmallIntegerField()
    trustworthiness = FloatField()
    geotag = ForeignKey('GeoTag', on_delete=RESTRICT)
    created = DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_difficultyfeedback'

class Points(Model):
    GEOTAG, REPHOTO, PHOTO_UPLOAD, PHOTO_CURATION, PHOTO_RECURATION, DATING, DATING_CONFIRMATION, FILM_STILL, \
        ANNOTATION, CONFIRM_SUBJECT, CONFIRM_IMAGE_SIMILARITY, SUGGESTION_SUBJECT_AGE, SUGGESTION_SUBJECT_GENDER, \
        TRANSCRIBE, CATEGORIZE_SCENE, ADD_VIEWPOINT_ELEVATION, FLIP_PHOTO, ROTATE_PHOTO, INVERT_PHOTO = range(19)
    ACTION_CHOICES = (
        (GEOTAG, _('Geotag')),
        (REPHOTO, _('Rephoto')),
        (PHOTO_UPLOAD, _('Photo upload')),
        (PHOTO_CURATION, _('Photo curation')),
        (PHOTO_RECURATION, _('Photo re-curation')),
        (DATING, _('Dating')),
        (DATING_CONFIRMATION, _('Dating confirmation')),
        (FILM_STILL, _('Film still')),
        (ANNOTATION, _('Annotation')),
        (CONFIRM_SUBJECT, _('Confirm subject')),
        (CONFIRM_IMAGE_SIMILARITY, _('Confirm Image similarity')),
        (SUGGESTION_SUBJECT_AGE, _('Suggestion subject age')),
        (SUGGESTION_SUBJECT_GENDER, _('Suggestion subject age')),
        (TRANSCRIBE, _('Transcribe')),
        (CATEGORIZE_SCENE, _('Categorize scene')),
        (ADD_VIEWPOINT_ELEVATION, _('Add viewpoint elevation')),
        (FLIP_PHOTO, _('Flip photo')),
        (INVERT_PHOTO, _('Invert photo')),
        (ROTATE_PHOTO, _('Rotate photo')),
    )

    user = ForeignKey('Profile', related_name='points', on_delete=RESTRICT)
    action = PositiveSmallIntegerField(choices=ACTION_CHOICES, db_index=True)
    photo = ForeignKey('Photo', null=True, blank=True, on_delete=RESTRICT)
    album = ForeignKey('Album', null=True, blank=True, on_delete=RESTRICT)
    geotag = ForeignKey('GeoTag', null=True, blank=True, on_delete=RESTRICT)
    dating = ForeignKey('Dating', null=True, blank=True, on_delete=RESTRICT)
    dating_confirmation = ForeignKey('DatingConfirmation', null=True, blank=True, on_delete=RESTRICT)
    annotation = ForeignKey('analytics.FaceRecognitionRectangle', null=True, blank=True, on_delete=RESTRICT)
    face_recognition_rectangle_subject_data_suggestion = ForeignKey(
        'FaceRecognitionRectangleSubjectDataSuggestion', null=True, blank=True, on_delete=RESTRICT)
    subject_confirmation = ForeignKey('FaceRecognitionUserSuggestion', null=True, blank=True, on_delete=RESTRICT)
    image_similarity_confirmation = ForeignKey('ImageSimilaritySuggestion', null=True, blank=True, on_delete=RESTRICT)
    points = IntegerField(default=0)
    created = DateTimeField(db_index=True)
    transcription = ForeignKey('Transcription', null=True, blank=True, on_delete=RESTRICT)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_points'
        verbose_name_plural = 'Points'
        unique_together = (
            ('user', 'geotag'), ('user', 'dating'), ('user', 'dating_confirmation'), ('user', 'subject_confirmation'),
            ('user', 'image_similarity_confirmation'))

    def __str__(self):
        return u'%d - %s - %d' % (self.user_id, self.ACTION_CHOICES[self.action], self.points)

class Transcription(Model):
    text = CharField(max_length=5000, null=True, blank=True)
    photo = ForeignKey('Photo', related_name='transcriptions', on_delete=RESTRICT)
    user = ForeignKey('Profile', related_name='transcriptions', on_delete=RESTRICT)
    created = DateTimeField(auto_now_add=True, db_index=True)
    modified = DateTimeField(auto_now=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_transcription'

class TranscriptionFeedback(Model):
    created = DateTimeField(auto_now_add=True, db_index=True)
    user = ForeignKey('Profile', related_name='transcription_feedback', on_delete=RESTRICT)
    transcription = ForeignKey(Transcription, related_name='transcription', on_delete=RESTRICT)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_transcriptionfeedback'

class GeoTag(Model):
    MAP, EXIF, GPS, CONFIRMATION, STREETVIEW, SOURCE_GEOTAG, ANDROIDAPP = range(7)
    # FIXME: EXIF and GPS have never been used
    TYPE_CHOICES = (
        (MAP, _('Map')),
        (EXIF, _('EXIF')),
        (GPS, _('GPS')),
        (CONFIRMATION, _('Confirmation')),
        (STREETVIEW, _('StreetView')),
        (SOURCE_GEOTAG, _('Source geotag')),
        (ANDROIDAPP, _('Android app')),
    )
    GAME, MAP_VIEW, GALLERY, PERMALINK, SOURCE, REPHOTO = range(6)
    ORIGIN_CHOICES = (
        (GAME, _('Game')),
        (MAP_VIEW, _('Map view')),
        (GALLERY, _('Gallery')),
        (PERMALINK, _('Permalink')),
        (SOURCE, _('Source')),
        (REPHOTO, _('Rephoto')),
    )
    GOOGLE_MAP, GOOGLE_SATELLITE, OPEN_STREETMAP, JUKS, NO_MAP = range(5)
    MAP_TYPE_CHOICES = (
        (GOOGLE_MAP, _('Google map')),
        (GOOGLE_SATELLITE, _('Google satellite')),
        (OPEN_STREETMAP, _('OpenStreetMap')),
        (JUKS, _('Juks')),
        (NO_MAP, _('No map')),
    )

    lat = FloatField(validators=[MinValueValidator(-85.05115), MaxValueValidator(85)])
    lon = FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    geography = PointField(srid=4326, null=True, blank=True, geography=True, spatial_index=True)
    azimuth = FloatField(null=True, blank=True)
    azimuth_line_end_lat = FloatField(null=True, blank=True)
    azimuth_line_end_lon = FloatField(null=True, blank=True)
    zoom_level = IntegerField(null=True, blank=True)
    origin = PositiveSmallIntegerField(choices=ORIGIN_CHOICES, default=0)
    type = PositiveSmallIntegerField(choices=TYPE_CHOICES, default=0)
    map_type = PositiveSmallIntegerField(choices=MAP_TYPE_CHOICES, default=0)
    hint_used = BooleanField(default=False)
    photo_flipped = BooleanField(default=False)
    user = ForeignKey('Profile', related_name='geotags', null=True, blank=True, on_delete=RESTRICT)
    photo = ForeignKey('Photo', related_name='geotags', on_delete=RESTRICT)
    is_correct = BooleanField(default=False)
    azimuth_correct = BooleanField(default=False)
    score = IntegerField(null=True, blank=True)
    azimuth_score = IntegerField(null=True, blank=True)
    trustworthiness = FloatField()
    created = DateTimeField(auto_now_add=True, db_index=True)
    modified = DateTimeField(auto_now=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_geotag'

    def __str__(self):
        # Django admin may crash with too long names
        importer = 'user: ' + str(self.user_id) if self.user else 'Ajapaik'
        photo = self.photo
        if importer:
            return f'{str(self.id)} - {str(photo.id)} - {photo.get_display_text[:50]} - {importer}'

class LocationPhoto(Model):
    location = ForeignKey('Location', on_delete=RESTRICT)
    photo = ForeignKey('Photo', on_delete=RESTRICT)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_locationphoto'

class Location(Model):
    name = CharField(max_length=255, null=True, blank=True)
    location_type = CharField(max_length=255, null=True, blank=True)
    photos = ManyToManyField('Photo', through='LocationPhoto', related_name='locations')
    sublocation_of = ForeignKey('self', blank=True, null=True, related_name='sublocations', on_delete=RESTRICT)
    google_reverse_geocode = ForeignKey(
        'GoogleMapsReverseGeocode',
        blank=True,
        null=True,
        related_name='google_reverse_geocode',
        on_delete=RESTRICT
    )

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_location'

class Source(Model):
    name = CharField(max_length=255)
    description = TextField(null=True, blank=True)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_source'

class Device(Model):
    camera_make = CharField(null=True, blank=True, max_length=255)
    camera_model = CharField(null=True, blank=True, max_length=255)
    lens_make = CharField(null=True, blank=True, max_length=255)
    lens_model = CharField(null=True, blank=True, max_length=255)
    software = CharField(null=True, blank=True, max_length=255)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_device'

    def __str__(self):
        return f'{self.camera_make} {self.camera_model} {self.lens_make} {self.lens_model} {self.software}'

class Skip(Model):
    user = ForeignKey('Profile', related_name='skips', on_delete=RESTRICT)
    photo = ForeignKey('Photo', on_delete=RESTRICT)
    created = DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_skip'

    def __str__(self):
        return f'{str(self.user_id)} {str(self.photo.pk)}'

class Licence(Model):
    name = CharField(max_length=255)
    url = URLField(blank=True, null=True)
    image_url = URLField(blank=True, null=True)
    is_public = BooleanField(default=False)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_licence'

    def __str__(self):
        return self.name

class GoogleMapsReverseGeocode(Model):
    lat = FloatField(validators=[MinValueValidator(-85.05115), MaxValueValidator(85)], db_index=True)
    lon = FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)], db_index=True)
    response = json.JSONField()

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_googlemapsreversegeocode'

    def __str__(self):
        if self.response.get('results') and self.response.get('results')[0]:
            location = self.response.get('results')[0].get('formatted_address')
            return f'{location};{self.lat};{self.lon}'
        else:
            return f'{self.lat};{self.lon}'

class Dating(Model):
    DAY, MONTH, YEAR = range(3)
    ACCURACY_CHOICES = (
        (DAY, _('Day')),
        (MONTH, _('Month')),
        (YEAR, _('Year')),
    )

    photo = ForeignKey('Photo', related_name='datings', on_delete=RESTRICT)
    profile = ForeignKey('Profile', blank=True, null=True, related_name='datings', on_delete=RESTRICT)
    raw = CharField(max_length=25, null=True, blank=True)
    comment = TextField(blank=True, null=True)
    start = DateField(default=datetime.strptime('01011000', '%d%m%Y').date())
    start_approximate = BooleanField(default=False)
    start_accuracy = PositiveSmallIntegerField(choices=ACCURACY_CHOICES, blank=True, null=True)
    end = DateField(default=datetime.strptime('01013000', '%d%m%Y').date())
    end_approximate = BooleanField(default=False)
    end_accuracy = PositiveSmallIntegerField(choices=ACCURACY_CHOICES, blank=True, null=True)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_dating'

    def __str__(self):
        return f'{str(self.profile.pk)} - {str(self.photo.pk)}'

class DatingConfirmation(Model):
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)
    confirmation_of = ForeignKey('Dating', related_name='confirmations', on_delete=RESTRICT)
    profile = ForeignKey('Profile', related_name='dating_confirmations', on_delete=RESTRICT)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_datingconfirmation'

    def __str__(self):
        return f'{str(self.profile.pk)} - {str(self.confirmation_of.pk)}'

class Video(Model):
    name = CharField(max_length=255)
    slug = SlugField(null=True, blank=True, max_length=255, unique=True)
    file = FileField(upload_to='videos', blank=True, null=True)
    width = IntegerField()
    height = IntegerField()
    author = CharField(max_length=255, blank=True, null=True)
    date = DateField(blank=True, null=True)
    source = ForeignKey('Source', blank=True, null=True, on_delete=RESTRICT)
    source_key = CharField(max_length=255, blank=True, null=True)
    source_url = URLField(blank=True, null=True)
    cover_image = ImageField(upload_to='videos/covers', height_field='cover_image_height',
                             width_field='cover_image_width', blank=True, null=True)
    cover_image_height = IntegerField(blank=True, null=True)
    cover_image_width = IntegerField(blank=True, null=True)
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_video'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('videoslug', args=(self.id, self.slug))

class Suggestion(Model):
    created = DateTimeField(auto_now_add=True, db_index=True)
    photo = ForeignKey('Photo', on_delete=RESTRICT)

    class Meta:
        abstract = True

class PhotoSceneSuggestion(Suggestion):
    INTERIOR, EXTERIOR = range(2)
    SCENE_CHOICES = (
        (INTERIOR, _('Interior')),
        (EXTERIOR, _('Exterior'))
    )
    scene = PositiveSmallIntegerField(_('Scene'), choices=SCENE_CHOICES, blank=True, null=True)
    proposer = ForeignKey('Profile', blank=True, null=True, related_name='photo_scene_suggestions', on_delete=RESTRICT)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_photoscenesuggestion'

class PhotoViewpointElevationSuggestion(Suggestion):
    GROUND_LEVEL, RAISED, AERIAL = range(3)
    VIEWPOINT_ELEVATION_CHOICES = (
        (GROUND_LEVEL, _('Ground')),
        (RAISED, _('Raised')),
        (AERIAL, _('Aerial'))
    )
    viewpoint_elevation = PositiveSmallIntegerField(_('Viewpoint elevation'), choices=VIEWPOINT_ELEVATION_CHOICES, blank=True, null=True)
    proposer = ForeignKey('Profile', blank=True, null=True, related_name='photo_viewpoint_elevation_suggestions', on_delete=RESTRICT)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_photoviewpointelevationsuggestion'

class PhotoFlipSuggestion(Suggestion):
    proposer = ForeignKey('Profile', blank=True, null=True, related_name='photo_flip_suggestions', on_delete=RESTRICT)
    flip = BooleanField(null=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_photoflipsuggestion'

class PhotoInvertSuggestion(Suggestion):
    proposer = ForeignKey('Profile', blank=True, null=True, related_name='photo_invert_suggestions', on_delete=RESTRICT)
    invert = BooleanField(null=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_photoinvertsuggestion'

class PhotoRotationSuggestion(Suggestion):
    rotated = IntegerField(null=True, blank=True)
    proposer = ForeignKey('Profile', blank=True, null=True, related_name='photo_rotate_suggestions', on_delete=RESTRICT)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_photorotationsuggestion'

class MuisCollection(Model):
    spec = CharField(max_length=255, null=True, blank=True)
    name = CharField(max_length=255, null=True, blank=True)
    imported = BooleanField(default=False)
    blacklisted = BooleanField(default=False)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_muiscollection'


class AlbumVideos(Model):
    album = ForeignKey(Album, on_delete=RESTRICT)
    video = ForeignKey(Video, on_delete=RESTRICT)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_album_videos'
        unique_together = (('album', 'video'),)


class Profile(Model):
#    score = PositiveIntegerField(default=0, db_index=True)
#    display_name = CharField(max_length=255, null=True, blank=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'project_profile_ids'
