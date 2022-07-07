from django.db.models import Model

class ReplicatedModel(Model):
    class Meta:
        abstract = True
        app_label = 'replica_ro'
        managed = False
        read_only_model = True
