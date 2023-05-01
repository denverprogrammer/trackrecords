"""
Django command to wait for the database to be available.
"""

import os
import typing

from core.models import (
    Exchange,
    Market,
    NaicsCode,
    Security,
    SicCode,
    Symbol,
    TempSymbol,
)
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.db.backends.utils import CursorWrapper


class Command(BaseCommand):
    """Django command to import Exchanges, Markets, Securities and Symbols."""

    def handle(self, *args: typing.Any, **options: typing.Any) -> None:
        """Entrypoint for command"""
        self.stdout.write('Starting data import...')

        cursor: CursorWrapper = connection.cursor()

        self.stdout.write('Clearning temp table...')
        NaicsCode.objects.clear_table(cursor)
        NaicsCode.objects.import_from_file(cursor)
        self.stdout.write('Imported NAICS codes...')
        SicCode.objects.clear_table(cursor)
        SicCode.objects.import_from_file(cursor)
        self.stdout.write('Imported SIC codes...')
        Exchange.objects.clear_table(cursor)
        Exchange.objects.import_from_file(cursor)
        self.stdout.write('Imported Exchanges...')
        Security.objects.clear_table(cursor)
        Security.objects.import_from_file(cursor)
        self.stdout.write('Imported Securities...')
        self.stdout.write('Initial import of related data complete...')

        TempSymbol.objects.download_data_file()
        self.stdout.write('Download complete...')

        TempSymbol.objects.clear_table(cursor)
        TempSymbol.objects.import_from_file(cursor)
        self.stdout.write('Import of temp symbols complete...')

        qs = TempSymbol.objects.all()
        Exchange.objects.insert_from_temp(cursor, qs.distinct_exchanges())
        self.stdout.write('Inserted new Exchanges...')
        Market.objects.insert_from_temp(cursor, qs.distinct_markets())
        self.stdout.write('Inserted new Markets...')
        Security.objects.insert_from_temp(cursor, qs.distinct_securities())
        self.stdout.write('Inserted new Securities...')
        NaicsCode.objects.insert_from_temp(cursor, qs.distinct_naics())
        self.stdout.write('Inserted new NAICS codes...')
        SicCode.objects.insert_from_temp(cursor, qs.distinct_sic())
        self.stdout.write('Inserted new SIC codes...')
        Symbol.objects.insert_from_temp(cursor, qs.distinct_symbols())
        self.stdout.write('Inserted related symbols...')

        TempSymbol.objects.remove_data_file()
        self.stdout.write('File removed...')

        TempSymbol.objects.clear_table(cursor)
        connection.close()
        self.stdout.write(self.style.SUCCESS('Temp Symbols cleared'))

        self.stdout.write(self.style.SUCCESS('Import data complete'))
