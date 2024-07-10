from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = "List all the widgets found in content templates."

    def add_arguments(self, parser):
        parser.add_argument(
            "engine",
            nargs='?',
            type=str,
            default="",
            help="<django> or <jinja2>, for only print one engine widgets. If not given, print for both engines."
        )

    def handle(self, *args, **options) :
        if options["engine"] != "jinja2" and options["engine"] != "django" and options["engine"] != "" :
            call_command("list-widgets", "--help")
            return

        if options["engine"] == "" :
            call_command("list-widgets", "jinja2")
            call_command("list-widgets", "django")
            return 

        n = 0
        for template_dir in settings.JFME_TEMPLATES_DIRS :
            for widget in (template_dir / options["engine"] / "widgets").rglob("*") :
                if widget.is_file() :
                    self.stdout.write(str(widget.relative_to(settings.BASE_DIR)))
                    n += 1

        if n > 1 :
            self.stdout.write(
                "%d %s widgets found" % 
                (n, options["engine"])
            )
        else :
            self.stdout.write(
                "%d %s widget found" % 
                (n, options["engine"])
            )