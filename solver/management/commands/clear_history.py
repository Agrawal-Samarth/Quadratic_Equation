from django.core.management.base import BaseCommand
from solver.models import QuadraticEquation


class Command(BaseCommand):
    help = 'Clear all quadratic equation history from the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Skip confirmation prompt',
        )

    def handle(self, *args, **options):
        count = QuadraticEquation.objects.count()
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('No equations found in the database.')
            )
            return

        if not options['confirm']:
            confirm = input(
                f'Are you sure you want to delete {count} equations? (yes/no): '
            )
            if confirm.lower() != 'yes':
                self.stdout.write(
                    self.style.WARNING('Operation cancelled.')
                )
                return

        deleted_count, _ = QuadraticEquation.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {deleted_count} equations from the database.'
            )
        )
