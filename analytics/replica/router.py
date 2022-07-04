class ReplicaRouter:
    """
    A router to control all database operations on models in the
    replica_db.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read user models go to users_db.
        """
        if model._meta.app_label == 'replica_ro':
            return 'replica_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write user models go to users_db.
        """
        if model._meta.app_label == 'replica_ro':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the user app is involved.
        """
#        if obj1._meta.app_label == 'replica_ro' or \
#           obj2._meta.app_label == 'replica_ro':
#           return True
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'users_db'
        database.
        """
        if app_label == 'replica_ro':
            return False
        return None
