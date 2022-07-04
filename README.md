# ajapaik-analytics
Sample app for accessing to Ajapaik replica database

# Access rights
For database access & portforwarding etc you need user/password. Ask Zache or Vahur from Ajapaik slack for creation


# Installation

1.) Get source code
```
git clone git@github.com:Ajapaik/ajapaik-analytics.git
cd ajapaik-analytics
```

2.) Create virtualenv for python and activate it
```
python3 -m venv ./venv
source ./venv/bin/activate
```

3.) Install requirements
```
pip install -r requirements.txt
```

4.) Create analytics/settings/local.py
```
cp analytics/settings/local.py.example analytics/settings/local.py
edit analytics/settings/local.py
```

5.) (OPTIONAL) If you are running code locally and not in analytics then create portforward to analytics for database access
```
ssh -L 5430:127.0.0.1:5430 USERNAME@ajapaik.ee -p PORT
```

6.) Test that database connections and models are working
```
python manage.py testmodels
```

( Code is in ajapaik-analytics/analytics/management/testmodels.py )

# Example

Django documentation for management commands
* https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/

File: [analytics/management/commands/example.py](analytics/management/commands/example.py)

```
from django.core.management.base import BaseCommand, CommandError
from analytics.replica.models_ajapaik import Photo

class Command(BaseCommand):

    help = 'Print coordinates of first 100 photos'

    def handle(self, *args, **options):
        photos = Photo.objects.filter(lat__isnull=False, lon__isnull=False).order_by('id')[:100]
        for photo in photos:
            print('lat: ' + str(photo.lat) + '\tlon: ' + str(photo.lon) +'\t' + str(photo))
```
Running
```
python manage.py example
```

# Models
Replicated Ajapaik models in database

![Replicated models](ajapaik_replica_models.png)

For regenerating model map
```
apt-get install graphviz-dev
pip install pygraphviz
./manage.py graph_models --pygraphviz -o ajapaik_replica_models.png
```
