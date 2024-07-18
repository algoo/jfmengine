from django.core.management.base import BaseCommand
from pathlib import Path
from bs4 import BeautifulSoup
from django.conf import settings

class Command(BaseCommand):
    help = "Format (beautify or minify) the html files in dist content"

    def add_arguments(self, parser):
        parser.add_argument(
            "mode",
            choices=["beautify", "minify"],
            type=str,
            help="Beautify or minify the html files"
        ),
        parser.add_argument(
            "distpath",
            nargs='?',
            type=str,
            default=str(settings.DIST_DIR),
            help="To specify a particular dist path"
        )

    def handle(self, *args, **options) :
        for path in Path(options["distpath"]).rglob("*.html") :
            with open(path, "r+") as file :
                soup = BeautifulSoup(file.read(), 'html.parser')
                file.seek(0)
                if options["mode"] == "minify" :
                    file.write(str(soup).replace('\n', ''))
                else :
                    file.write(soup.prettify())
                file.truncate()