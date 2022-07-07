import analytics.replica_ro.models_ajapaik
import analytics.replica_ro.models_ajapaik_facerecognition
import analytics.replica_ro.models_ajapaik_objectrecognition
from django.contrib.gis.db.models import Model, CharField, TextField, BooleanField, DateTimeField, ForeignKey, RESTRICT, PositiveIntegerField, DO_NOTHING
from django.utils.translation import gettext as _

class Translation(Model):
    photo = ForeignKey('replica_ro.Photo', related_name='translations', null=True, on_delete=DO_NOTHING)
    name = CharField(_('Name'), max_length=255, db_index=True)
    description = TextField(_('Description'), null=True, blank=True, max_length=2047)
    is_original = BooleanField(_('Is public'), default=False)
    language =  CharField(_('Name'), max_length=5, db_index=True)
    comment =  CharField(_('comment'), max_length=255, db_index=True)
    created = DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        app_label = 'replica_user'
