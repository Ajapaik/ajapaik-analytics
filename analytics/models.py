import analytics.replica_ro.models_ajapaik
from analytics.replica_ro.models_ajapaik import Photo
import analytics.replica_ro.models_ajapaik_facerecognition
import analytics.replica_ro.models_ajapaik_objectrecognition
from django.contrib.gis.db.models import Model, CharField, TextField, BooleanField, DateTimeField, ForeignKey, RESTRICT, DO_NOTHING, PositiveIntegerField
from django.utils.translation import gettext as _

# Foreing keys doesn't work between Sqlite and Postgres
# If both models (Translation and replica_ro.Photo) are in same database in Analytics Postgres then you can use ForeignKeys

class Translation(Model):
#    photo = ForeignKey('replica_ro.Photo', related_name='translations', null=True, on_delete=DO_NOTHING)
    photo = PositiveIntegerField(_('Photo'), db_index=True)
    name = CharField(_('Name'), max_length=255, db_index=True)
    description = TextField(_('Description'), null=True, blank=True, max_length=2047)
    is_original = BooleanField(_('Is public'), default=False)
    language =  CharField(_('Name'), max_length=5, db_index=True)
    comment =  CharField(_('comment'), max_length=255, db_index=True)
    created = DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        app_label = 'sqlite'

