from django.core.management.commands.migrate import Command as MigrateCommand  # type: ignore[import]
from django.db import connections


class Command(MigrateCommand):

    def add_arguments(self, parser):
        super().add_arguments(parser)
        # parser.add_argument(
        #     '--batch', action='store_true',
        #     help='Run more commands together.',
        # )
        parser.add_argument(
            '--ask', action='store_true',
            help='Run migrate subcommands interactive.',
        )
        parser.add_argument(
            '--no-check-permissions', action='store_true',
            help='Run migrate withot check permissions of CustomObjects.',
        )

    def handle(self, *args, **options):
        database = options['database']
        connection = connections[database]
        if connection.vendor == 'salesforce':
            connection.migrate_options = {
                # 'batch': options['batch'],
                'ask': options['ask'],
                'no_check_permissions': options['no_check_permissions'],
            }
        super().handle(*args, **options)
