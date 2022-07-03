# ajapaik-analytics
Sample app for accessing to Ajapaik replica database

# Installation

1.) Get source code
git clone git@github.com:Ajapaik/ajapaik-analytics.git
cd ajapaik-analytics

2.) Create virtualenv for python and activate it
python3 -m venv ./venv
source ./venv/bin/activate

3.) Install requirements
pip install -r requirements.txt

4.) Create analytics/settings/local.py with database USER and PASSWORD
cp analytics/settings/local.py.example analytics/settings/local.py
edit analytics/settings/local.py.example

5.) (OPTIONAL) If you are running code locally then create portforward to analytics for database access


6.) Test that database connections and models are working
# Code is in ajapaik-analytics/analytics/management/testmodels.py

python manage.py testmodels

# Access rights
For database access & portforwarding you need user/password. Ask Zache or Vahur from Ajapaik slack for creation
