"""
Django command to wait for the database to be available.
"""

import os
import time
import typing
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

import psycopg2
from config.settings import DATABASES
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to import Exchanges, Markets, Securities and Symbols."""

    def handle(self, *args: typing.Any, **options: typing.Any) -> None:
        """Entrypoint for command"""
        host = 'https://www.iqfeed.net'
        path = '/downloads/download_file.cfm'
        params = 'type=mktsymbols'
        self.stdout.write('Starting data import...')
        response = urlopen(f'{host}{path}?{params}')

        zipfile = ZipFile(BytesIO(response.read()))
        self.stdout.write('Download complete...')

        zipfile.extractall(path='/home/data')
        self.stdout.write('File extracted...')

        conn = psycopg2.connect(
            database=DATABASES['default']['NAME'],
            user=DATABASES['default']['USER'],
            password=DATABASES['default']['PASSWORD'],
            host=DATABASES['default']['HOST'],
            port=DATABASES['default']['PORT']
        )

        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute('DELETE FROM dataset_tempsymbol;')
        self.stdout.write('Temp Symbol cleaned...')

        cursor.execute('''
            COPY dataset_tempsymbol(
                symbol,
                description,
                exchange,
                listed_market,
                security_type,
                sic,
                frontmonth,
                naics
            )
            FROM '/home/data/mktsymbols_v2.txt'
            DELIMITER '\t'
            CSV HEADER;
        ''')
        self.stdout.write('Upsert complete...')

        conn.commit()
        conn.close()

        os.remove('/home/data/mktsymbols_v2.txt')
        self.stdout.write('File removed...')

        self.stdout.write(self.style.SUCCESS('Import data complete'))
