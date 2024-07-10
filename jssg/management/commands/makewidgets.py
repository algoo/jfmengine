from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = "Make a file which contains all widgets for easier import in templates and pages."

    def add_arguments(self, parser):
        parser.add_argument(
            "engine",
            nargs = '?',
            type=str,
            default="",
            help="The template engine <django> or <jinja2>. If not given, make for both engines."
        )

    def handle(self, *args, **options):
        if options["engine"] != "jinja2" and options["engine"] != "django" and options["engine"] != "" :
            call_command("makewidgets", "--help")
            return

        if options["engine"] == "" :
            call_command("makewidgets", "jinja2")
            call_command("makewidgets", "django")
            return 

        path = settings.BASE_DIR / "content" / "templates" / options["engine"] / ("allwidgets.html")
        buf = ""
        n = 0
        for template_dir in settings.JFME_TEMPLATES_DIRS :
            for widget in (template_dir / options["engine"] / "widgets").rglob("*") :
                if widget.is_file() :
                    w = open(widget, "r")
                    buf += w.read() + "\n"
                    w.close()
                    n += 1

        if n == 0 :
            self.stdout.write(
                "0 %s widget written" % 
                options["engine"]
            )
        else :
            path.parent.mkdir(exist_ok=True, parents=True)
            with open(path, "w+") as f :
                f.write(buf)
            if n == 1 :
                self.stdout.write(
                    "1 %s widget written in %s" % 
                    (options["engine"], path.relative_to(settings.BASE_DIR))
                )
            else :
                self.stdout.write(
                    "%d %s widgets written in %s" % 
                    (n, options["engine"], path.relative_to(settings.BASE_DIR))
                )