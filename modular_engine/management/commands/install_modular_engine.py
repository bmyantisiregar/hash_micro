import subprocess
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Install the modular_engine: migrate, create superuser, and start server.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('👉 Starting modular_engine installation...'))

        # 1. Check database connection
        self.stdout.write(self.style.NOTICE('Checking database connection...'))
        db_conn = connections['default']
        try:
            db_conn.ensure_connection()
            self.stdout.write(self.style.SUCCESS('Database connection successful.'))
        except OperationalError:
            self.stdout.write(self.style.ERROR('Database connection failed. Please check your .env or settings.py!'))
            return

        # 3. Migrate 
        self.stdout.write(self.style.NOTICE('Running migrations...'))
        try:
            call_command('migrate')
            self.stdout.write(self.style.SUCCESS('Migrations applied.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Migration failed: {e}'))
            return

        # 4. Create default superuser if not exists
        User = get_user_model()
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'
        if not User.objects.filter(username=username).exists():
            self.stdout.write(self.style.NOTICE(f'👤 Creating default superuser: {username}/{password}'))
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))

        # 5. Confirm that /module/ page is ready
        self.stdout.write(self.style.SUCCESS('Setup complete!'))
        self.stdout.write(self.style.SUCCESS('You can now visit: http://127.0.0.1:8000/module/ to manage modules.'))

        # # 6. Start server automatically
        # self.stdout.write(self.style.NOTICE('Starting Django development server...'))
        # try:
        #     subprocess.run(["python", "manage.py", "runserver"], check=True)
        # except subprocess.CalledProcessError as e:
        #     self.stdout.write(self.style.ERROR(f'Error starting server: {e}'))
