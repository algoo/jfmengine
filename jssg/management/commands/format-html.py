import os
from django.core.management.base import BaseCommand
from pathlib import Path
from bs4 import BeautifulSoup
from django.conf import settings
import minify_html


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
            help="To specify a particular dist path. Default is: " + str(settings.DIST_DIR)
        )

    def handle(self, *args, **options) :
        if options["mode"] == "minify":
            for path in Path(options["distpath"]).rglob("*.html"):
                self.__minify_file(path)
            for path in Path(options["distpath"]).rglob("*.js"):
                self.__minify_file(path)
            for path in Path(options["distpath"]).rglob("*.css"):
                self.__minify_file(path)
        else:
            for path in Path(options["distpath"]).rglob("*.html"):
                self.__beautify_file(path)

    def __minify_file(self, file_path: Path, display_downsize_ratio: bool=True) -> None:
        size_before = os.stat(file_path).st_size
        with open(file_path, "r+") as file:
            minified = minify_html.minify(
                file.read(),
                do_not_minify_doctype=True,
                ensure_spec_compliant_unquoted_attribute_values=True,
                keep_closing_tags=True,
                keep_spaces_between_attributes=True,
                minify_css=True,
                minify_js=True,
            )
            file.seek(0)
            file.write(minified)
            file.truncate()

        size_after = os.stat(file_path).st_size
        if display_downsize_ratio:
            message = f"[-{1 - size_after / size_before:.1%}] {file_path}"  # shows -xx.x% ration
            print(message)

    def __beautify_file(self, file_path: Path, display_upsize_ratio: bool=True) -> None:
        """
        beautify a HTML file
        """
        size_before = os.stat(file_path).st_size
        with open(file_path, "r+") as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            file.seek(0)
            file.write(soup.prettify())
            file.truncate()

        size_after = os.stat(file_path).st_size
        if display_upsize_ratio:
            message = f"[+{size_after / size_before - 1:.1%}] {file_path}"  # shows +xx.x% ration
            print(message)
