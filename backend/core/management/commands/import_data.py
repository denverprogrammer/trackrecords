"""
Django command to wait for the database to be available.
"""

import os
import typing

from dataset.models import Exchange, Market, NaicsCode, Security, SicCode, TempSymbol
from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    """Django command to import Exchanges, Markets, Securities and Symbols."""

    def handle(self, *args: typing.Any, **options: typing.Any) -> None:
        """Entrypoint for command"""
        self.stdout.write('Starting data import...')

        cursor = connection.cursor()
        cursor.execute(NaicsCode.objects.import_data())
        cursor.execute(SicCode.objects.import_data())
        cursor.execute(Exchange.objects.import_data())
        cursor.execute(Security.objects.import_data())
        self.stdout.write('Initial import of related data complete...')

        TempSymbol.objects.download_data_file()
        self.stdout.write('Download complete...')

        cursor.execute(TempSymbol.objects.clear_temp())
        cursor.execute(TempSymbol.objects.import_data())
        self.stdout.write('Import of temp symbols complete...')

        cursor.execute(TempSymbol.objects.insert_exchanges())
        cursor.execute(TempSymbol.objects.insert_markets())
        cursor.execute(TempSymbol.objects.insert_securities())
        cursor.execute(TempSymbol.objects.insert_naics())
        cursor.execute(TempSymbol.objects.insert_sic())
        self.stdout.write('Insert of related data complete...')

        cursor.execute(TempSymbol.objects.insert_symbols())
        self.stdout.write('Insert of symbols complete...')
        connection.close()

        os.remove('/home/data/symbols/mktsymbols_v2.txt')
        self.stdout.write('File removed...')

        cursor.execute(TempSymbol.objects.clear_temp())
        self.stdout.write(self.style.SUCCESS('Temp Symbols cleared'))

        self.stdout.write(self.style.SUCCESS('Import data complete'))
