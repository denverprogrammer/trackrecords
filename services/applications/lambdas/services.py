import os

import django
from config.settings import DATABASES
from django.conf import settings


def setup_django():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    if not settings.configured:
        settings.configure(
            DATABASES=DATABASES,
            INSTALLED_APPS=["vega"],
        )
        django.setup()
