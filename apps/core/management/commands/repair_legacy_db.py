from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder


LEGACY_MARKER_TABLE = 'django_admin_log'
BOOTSTRAP_MODELS = [
    ('accounts', '0001_initial', 'accounts', 'User'),
    ('achievements', '0001_initial', 'achievements', 'Achievement'),
    ('courses', '0001_initial', 'courses', 'Course'),
    ('games', '0001_initial', 'games', 'Game'),
]


class Command(BaseCommand):
    help = 'Repairs a legacy Railway database so Django migrations can run cleanly.'

    def handle(self, *args, **options):
        existing_tables = set(connection.introspection.table_names())

        if LEGACY_MARKER_TABLE not in existing_tables:
            self.stdout.write('Legacy repair not needed.')
            return

        recorder = MigrationRecorder(connection)
        recorder.ensure_schema()

        created_tables = []
        recorded_migrations = []

        for app_label, migration_name, model_app_label, model_name in BOOTSTRAP_MODELS:
            model = apps.get_model(model_app_label, model_name)
            table_name = model._meta.db_table
            migration_applied = recorder.migration_qs.filter(
                app=app_label,
                name=migration_name,
            ).exists()

            if table_name not in existing_tables:
                self.stdout.write(f'Creating missing table: {table_name}')
                with connection.schema_editor() as schema_editor:
                    schema_editor.create_model(model)
                existing_tables.add(table_name)
                created_tables.append(table_name)

            if not migration_applied:
                recorder.record_applied(app_label, migration_name)
                recorded_migrations.append(f'{app_label}.{migration_name}')

        if created_tables:
            self.stdout.write(self.style.WARNING(
                'Created tables: ' + ', '.join(created_tables)
            ))

        if recorded_migrations:
            self.stdout.write(self.style.WARNING(
                'Recorded migrations: ' + ', '.join(recorded_migrations)
            ))

        self.stdout.write(self.style.SUCCESS('Legacy database repaired.'))
