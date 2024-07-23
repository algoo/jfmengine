from django.core.management.base import BaseCommand
from django.conf import settings
from jssg.models import Page
from pathlib import Path

class MetadataStatus :
    
    def get_metadata_status_for(self, page) :
        self.missing = []
        self.empty = []
        for required_metadata in settings.JFME_CONTENT_REQUIRED_METADATA :
            if required_metadata not in page.metadata :
                self.missing.append(required_metadata)
            elif page.metadata[required_metadata] == "" :
                self.empty.append(required_metadata)
        self.complete = self.missing == [] and self.empty == []
        if len(settings.JFME_CONTENT_REQUIRED_METADATA) > 0 :
            self.progression = (len(settings.JFME_CONTENT_REQUIRED_METADATA) - len(self.missing) - len(self.empty)) * 100 / len(settings.JFME_CONTENT_REQUIRED_METADATA)
        else :
            self.progression = 100

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

            metadata_status = MetadataStatus()
            metadata_status.get_metadata_status_for(page)
            
            self.stdout.write("{:3.0f}% : {}".format(
                metadata_status.progression,
                page.path.relative_to(page.content_page_dir))
            )

            if options["verbosity"]>1 or options["verbose"] :
               if not metadata_status.complete :
                    for missing in metadata_status.missing :
                       self.stdout.write("\t- '%s' is missing" % missing)
                    for empty in metadata_status.empty :
                       self.stdout.write("\t- '%s' is empty" % empty) 