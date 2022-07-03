from django.db.models import Model, RESTRICT, ForeignKey, TextField, DateTimeField, FloatField, BooleanField
import analytics.replica.models_ajapaik as ajapaik


# MASTER FILE
# https://github.com/Ajapaik/ajapaik-web/blob/master/ajapaik/ajapaik_object_recognition/models.py

class ObjectDetectionModel(Model):
    model_file_name = TextField(max_length=200)

    class Meta:
        managed = False
        db_table = 'ajapaik_object_recognition_objectdetectionmodel'

    def __str__(self):
        return self.model_file_name

class ObjectAnnotationClass(Model):
    alias = TextField(max_length=200, null=True)
    wiki_data_id = TextField(max_length=30)
    translations = TextField()
    detection_model = ForeignKey(ObjectDetectionModel, on_delete=RESTRICT)

    def __str__(self):
        english_translation = self.translations
        return f'{self.wiki_data_id}: {english_translation}'

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_object_recognition_objectannotationclass'

class ObjectDetectionAnnotation(Model):
    x1 = FloatField()
    x2 = FloatField()
    y1 = FloatField()
    y2 = FloatField()

    photo = ForeignKey('analytics.Photo', on_delete=RESTRICT)
    detected_object = ForeignKey(ObjectAnnotationClass, on_delete=RESTRICT)
    user = ForeignKey('analytics.Profile', on_delete=RESTRICT)
    is_manual_detection = BooleanField()

    created_on = DateTimeField(auto_now_add=True)
    modified_on = DateTimeField(auto_now=True)
    deleted_on = DateTimeField(null=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_object_recognition_objectdetectionannotation'

    def __str__(self):
        return f'Detected {self.detected_object.__str__()} on photo {self.photo.id} at ' \
               f'x1: {self.x1}, y1: {self.y1}, x2: {self.x2}, y2: {self.y2}'

class ObjectAnnotationFeedback(Model):
    object_detection_annotation = ForeignKey(ObjectDetectionAnnotation, related_name='feedback', on_delete=RESTRICT)

    confirmation = BooleanField(default=True)
    alternative_object = ForeignKey(ObjectAnnotationClass, null=True, on_delete=RESTRICT)
    user = ForeignKey('analytics.Profile', on_delete=RESTRICT)

    created_on = DateTimeField(auto_now_add=True)
    modified_on = DateTimeField(auto_now=True)

    class Meta:
        managed = False
        read_only_model = True
        db_table = 'ajapaik_object_recognition_objectannotationfeedback'

    def __str__(self):
        string_label = ''

        if self.confirmation:
            string_label += f'Confirmed annotation {self.object_detection_annotation.id}'
        else:
            string_label += f'Rejected annotation {self.object_detection_annotation.id}'

        if self.alternative_object is not None:
            string_label += f', alternative object suggested: {self.alternative_object.__str__()}'

        return string_label
















