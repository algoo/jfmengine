from django.core.management.base import BaseCommand
from django.conf import settings
from jssg.models import Page
from pathlib import Path

class MetadataStatus :
    
    @classmethod
    def get_metadata_status_for(cls, page) :
        metadata_status = MetadataStatus()
        metadata_status.missing = []
        metadata_status.empty = []
        for required_metadata in settings.JFME_CONTENT_REQUIRED_METADATA :
            if required_metadata not in page.metadata :
                metadata_status.missing.append(required_metadata)
            elif page.metadata[required_metadata] == "" :
                metadata_status.empty.append(required_metadata)
        metadata_status.complete = (metadata_status.missing == []) and (metadata_status.empty == [])
        if len(settings.JFME_CONTENT_REQUIRED_METADATA) > 0 :
            metadata_status.progression = (len(settings.JFME_CONTENT_REQUIRED_METADATA) - len(metadata_status.missing) - len(metadata_status.empty)) * 100 / len(settings.JFME_CONTENT_REQUIRED_METADATA)
        else :
            metadata_status.progression = 100
        return metadata_status

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

        if settings.JFME_CONTENT_REQUIRED_METADATA == [] :
            self.stdout.write(self.style.WARNING(
                "Warning : no metadata specified in JFME_CONTENT_REQUIRED_METADATA setting."
            ))

        for page in Page.load_glob(path = list(map(lambda p : Path(p).absolute(), options["content path"])), all = True) :

            metadata_status = MetadataStatus.get_metadata_status_for(page)

            self.stdout.write("{:3.0f}% : {}".format(
                metadata_status.progression,
                page.path.relative_to(page.content_page_dir))
            )

            if options["verbosity"] > 1 or options["verbose"] :
               if not metadata_status.complete :
                    for missing in metadata_status.missing :
                       self.stdout.write("\t- '%s' is missing" % missing)
                    for empty in metadata_status.empty :
                       self.stdout.write("\t- '%s' is empty" % empty) 