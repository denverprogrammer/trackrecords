import os

import django
from django.conf import settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # or 'mysql' or 'sqlite3'
        'NAME': os.getenv('DB_NAME', 'mydatabase'),
        'USER': os.getenv('DB_USER', 'myuser'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'mypassword'),
        'HOST': os.getenv('DB_HOST', 'mydb.example.com'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

def setup_django():
    if not settings.configured:
        settings.configure(
            DATABASES=DATABASES,
            INSTALLED_APPS=['vega'],  # Your Django app containing models
        )
        django.setup()
