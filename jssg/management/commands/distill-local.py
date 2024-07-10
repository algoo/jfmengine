import importlib
DistilllocalCommand = importlib.import_module("django_distill.management.commands.distill-local").Command
from django.core.management import call_command

class Command(DistilllocalCommand):
    def handle(self, *args, **options):
        call_command('make-widgets')
        super(Command, self).handle(*args, **options)