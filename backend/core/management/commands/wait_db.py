import time

from django.contrib.gis.db.backends.mysql.base import DatabaseWrapper
from django.core.management import BaseCommand
from django.db import connection, OperationalError

connection: DatabaseWrapper = connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting db....')
        con_db = False

        while not con_db:
            try:
                connection.ensure_connection()
                con_db = True
            except OperationalError:
                self.stdout.write('Database unavailable, wait 3 seconds...')
                time.sleep(3)

        self.stdout.write(self.style.SUCCESS('Database available!'))
