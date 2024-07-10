from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.management import call_command

class Command(RunserverCommand):
    def inner_run(self, *args, **options):
        call_command('makewidgets', 'jinja2')
        call_command('makewidgets', 'django')
        super(Command, self).inner_run(*args, **options)