from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management import call_command

class Command(RunserverCommand):
    def inner_run(self, *args, **options):
        call_command('make-widgets')
        super(Command, self).inner_run(*args, **options)