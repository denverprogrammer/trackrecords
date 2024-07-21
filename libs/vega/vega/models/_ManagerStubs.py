
import os
import typing
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

from django.db import models
from django.db.backends.utils import CursorWrapper


class ImportExportStub(object):

    import_columns = []
    insert_columns = []
    file_name = None
    download_url = None
    extract_folder = None
    extract_file = None

    def download_data_file(self) -> None:
        response = urlopen(self.download_url)
        zipfile = ZipFile(BytesIO(response.read()))
        zipfile.extractall(path=self.extract_folder)

    def remove_data_file(self) -> None:
        os.remove(self.file_name)

    def get_import_columns(self) -> str:
        return ', '.join(self.import_columns)

    def get_insert_columns(self) -> str:
        return ', '.join(self.insert_columns)

    def import_from_file(self, cursor: CursorWrapper) -> None:
        sql = f'''
            COPY {self.model._meta.db_table} ({self.get_import_columns()})
            FROM '{self.file_name}'
            DELIMITER E'\t' CSV HEADER;
        '''

        cursor.execute(sql)

    def export_to_file(self, cursor: CursorWrapper) -> None:
        sql = f'''
            COPY (select {self.get_import_columns()} from {self.model._meta.db_table})
            TO '{self.file_name}'
            WITH DELIMITER E'\t' CSV HEADER;
        '''

        cursor.execute(sql)

    def insert_from_temp(self, cursor: CursorWrapper, query: models.QuerySet) -> None:
        sql = f'''
            INSERT INTO {self.model._meta.db_table} ({self.get_insert_columns()})
            {query.query}
            ON CONFLICT ({self.insert_columns[0]}) DO NOTHING;
        '''

        cursor.execute(sql)

    def clear_table(self, cursor: CursorWrapper) -> str:
        cursor.execute(f'DELETE FROM {self.model._meta.db_table};')
