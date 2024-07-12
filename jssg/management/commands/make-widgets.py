from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from re import findall

class Command(BaseCommand):
    help = "Make a file which contains all widgets macros for easier import in templates and pages."

    def handle(self, *args, **options):

        path = settings.BASE_DIR / "content" / "templates" / "jinja2" / "allwidgets.html"
        buf = ""
        n = 0
        for template_dir in settings.JFME_TEMPLATES_DIRS :
            for widget in (template_dir / "jinja2" / "widgets").rglob("*") :
                if widget.is_file() :
                    with open(widget, "r") as w :
                        for macro in findall(r"{%[\s]*macro[\s\S]*%}[\s\S]*{%[\s]*endmacro[\s]*%}", w.read()) :
                            buf += macro + "\n"
                            n += 1

        if n == 0 :
            self.stdout.write(
                "0 widget macro written"
            )
        else :
            path.parent.mkdir(exist_ok=True, parents=True)
            with open(path, "w+") as f :
                f.write(buf)
            if n == 1 :
                self.stdout.write(
                    "1 widget macro written in %s" % 
                    (path.relative_to(settings.BASE_DIR))
                )
            else :
                self.stdout.write(
                    "%d widget macros written in %s" % 
                    (n, path.relative_to(settings.BASE_DIR))
                )