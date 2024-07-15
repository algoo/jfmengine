from django.core.management.base import BaseCommand
from django.conf import settings
from jssg.models import Page
from pathlib import Path

class Command(BaseCommand):
    help = "Check if metadata in JFME_CONTENT_REQUIRED_METADATA setting are specified in pages."

    def add_arguments(self, parser):
        parser.add_argument(
            "--verbose",
            action = "store_true",
            help="Show missing or empty metadata in each page."
        )
        parser.add_argument(
            "content path",
            nargs = "*",
            type=str,
            default=settings.JFME_PAGES_DIRS,
            help="The paths where search the pages. Set to JFME_PAGES_DIRS by default."
        )

    def handle(self, *args, **options) :
        for page in Page.load_glob(path = list(map(lambda p : Path(p).absolute(), options["content path"])), all = True) :
            missing_metadata = []
            empty_metadata = []
            for required_metadata in settings.JFME_CONTENT_REQUIRED_METADATA :
                if required_metadata not in page.metadata :
                    missing_metadata.append(required_metadata)
                elif page.metadata[required_metadata] == "" :
                    empty_metadata.append(required_metadata)

            self.stdout.write("{:3.0f}% : {}".format(
                (len(settings.JFME_CONTENT_REQUIRED_METADATA) - len(missing_metadata) - len(empty_metadata)) * 100 / len(settings.JFME_CONTENT_REQUIRED_METADATA),
                page.path.relative_to(page.content_page_dir))
            )
            if options["verbosity"]>1 or options["verbose"] :
                for missing in missing_metadata :
                    self.stdout.write("\t- '{}' is missing".format(missing))
                for empty in empty_metadata :
                    self.stdout.write("\t- '{}' is empty".format(empty))