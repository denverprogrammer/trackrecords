"""
Django command to wait for the database to be available.
"""

import time
import typing

import psycopg2
from django.core.management.base import BaseCommand
from django.db import utils


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args: typing.Any, **options: typing.Any) -> None:
        """Entrypoint for command"""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (psycopg2.OperationalError, utils.OperationalError):
                self.stdout.error('Database unavailable, waiting 1 second...')
                time.sleep(10)

        self.stdout.write(self.style.SUCCESS('Database available'))
