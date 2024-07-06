from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = 'Displays all project URLs'

    def handle(self, *args, **options):
        url_patterns = get_resolver().url_patterns
        for pattern in url_patterns:
            self.stdout.write(self.style.SUCCESS(f'{pattern.pattern}'))
