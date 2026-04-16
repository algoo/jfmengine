import os
from pathlib import Path

import minify_html
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management.base import BaseCommand

import re

MINIFIED_JS_FILEPATH_PATTERN = r".*\.min.*\.js"  # minified JS files are like .min.js or .min.dfd824922bdc.js
MINIFIED_CSS_FILEPATH_PATTERN = r".*\.min.*\.css"  # minified CSS files are like .min.js or .min.dfd824922bdc.css


class Command(BaseCommand):
    help = "Format (beautify or minify) the html files in dist content"

    def add_arguments(self, parser):
        parser.add_argument(
            "mode",
            choices=["beautify", "minify"],
            type=str,
            help="Beautify or minify the html files",
        ),
        parser.add_argument(
            "distpath",
            nargs="?",
            type=str,
            default=str(settings.DIST_DIR),
            help="To specify a particular dist path. Default is: "
            + str(settings.DIST_DIR),
        )

    def handle(self, *args, **options):
        if options["mode"] == "minify":
            for path in Path(options["distpath"]).rglob("*.html"):
                self.__minify_file(path)
            for path in Path(options["distpath"]).rglob("*.js"):
                if re.match(MINIFIED_JS_FILEPATH_PATTERN, str(path)):
                    print(f"Skip minification for {path}")
                else:
                    self.__minify_file(path)
            for path in Path(options["distpath"]).rglob("*.css"):
                if re.match(MINIFIED_CSS_FILEPATH_PATTERN, str(path)):
                    print(f"Skip minification for {path}")
                else:
                    self.__minify_file(path)
        else:
            for path in Path(options["distpath"]).rglob("*.html"):
                self.__beautify_file(path)

    def __minify_file(
        self, file_path: Path, display_downsize_ratio: bool = True
    ) -> None:
        size_before = os.stat(file_path).st_size
        with open(file_path, "r+") as file:
            # INFO - 2025-08-21 - D.A. - see API https://github.com/wilsonzlin/minify-html/blob/master/minify-html/src/cfg/mod.rs
            minified = minify_html.minify(
                file.read(),
                minify_doctype=False,
                allow_noncompliant_unquoted_attribute_values=True,
                keep_closing_tags=True,
                allow_removing_spaces_between_attributes=False,
                keep_comments=False,
                keep_html_and_head_opening_tags=True,
                keep_input_type_text_attr=True,
                preserve_brace_template_syntax=True,
                preserve_chevron_percent_template_syntax=True,
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

    def __beautify_file(
        self, file_path: Path, display_upsize_ratio: bool = True
    ) -> None:
        """
        beautify a HTML file
        """
        size_before = os.stat(file_path).st_size
        with open(file_path, "r+") as file:
            soup = BeautifulSoup(file.read(), "html.parser")
            file.seek(0)
            file.write(soup.prettify())
            file.truncate()

        size_after = os.stat(file_path).st_size
        if display_upsize_ratio:
            message = f"[+{size_after / size_before - 1:.1%}] {file_path}"  # shows +xx.x% ration
            print(message)
