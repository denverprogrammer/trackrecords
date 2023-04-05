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

        cursor.execute(Exchange.objects.insert_from_data(
            TempSymbol.objects.all().distinct_exchanges()))
        cursor.execute(Market.objects.insert_from_data(
            TempSymbol.objects.all().distinct_markets()))
        cursor.execute(Security.objects.insert_from_data(
            TempSymbol.objects.all().distinct_securities()))
        cursor.execute(NaicsCode.objects.insert_from_data(
            TempSymbol.objects.all().distinct_naics()))
        cursor.execute(SicCode.objects.insert_from_data(
            TempSymbol.objects.all().distinct_sic()))
        self.stdout.write('Insert of related data complete...')

        cursor.execute(TempSymbol.objects.insert_symbols())
        self.stdout.write('Insert of symbols complete...')

        TempSymbol.objects.remove_data_file()
        self.stdout.write('File removed...')

        cursor.execute(TempSymbol.objects.clear_temp())
        connection.close()
        self.stdout.write(self.style.SUCCESS('Temp Symbols cleared'))

        self.stdout.write(self.style.SUCCESS('Import data complete'))
