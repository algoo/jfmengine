from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from jinja2.nodes import Macro

from jssg.jinja2 import Environment


class Command(BaseCommand):
    help = "List all the widgets found in content templates."

    def add_arguments(self, parser):
        parser.add_argument(
            "-django", action="store_true", help="For only print Django widgets."
        )
        parser.add_argument(
            "-jinja2", action="store_true", help="For only print Jinja2 widgets."
        )

    def handle(self, *args, **options):
        if options["jinja2"] and options["django"]:
            call_command("list-widgets", "-django")
            self.stdout.write("\n")
            call_command("list-widgets", "-jinja2")
            return

        if options["django"]:
            nb_file_found = 0
            for template_dir in settings.JFME_TEMPLATES_DIRS:
                for widget in (template_dir / "django" / "widgets").rglob("*"):
                    if widget.is_file():
                        with open(widget, "r") as w:
                            self.stdout.write(
                                "%s" % widget.relative_to(template_dir.parent.parent)
                            )
                            nb_file_found += 1

            self.stdout.write(
                self.style.HTTP_INFO(
                    "%d django %s found"
                    % (nb_file_found, "widget" if nb_file_found <= 1 else "widgets")
                )
            )

        elif options["jinja2"]:
            nb_file_found = 0
            nb_macro_found = 0
            visited = []
            for template_dir in settings.JFME_TEMPLATES_DIRS:
                for widget in (template_dir / "jinja2" / "widgets").rglob("*"):
                    rel_widget_path = widget.relative_to(template_dir.parent.parent)
                    if widget.is_file():
                        with open(widget, "r") as w:
                            self.stdout.write("%s" % str(rel_widget_path))
                            nb_file_found += 1
                            for macro in Environment().parse(w.read()).find_all(Macro):
                                visited.append(
                                    (widget.stem, macro.name, rel_widget_path)
                                )
                                self.stdout.write("\t%s()" % macro.name)
                                nb_macro_found += 1

            self.stdout.write(
                self.style.HTTP_INFO(
                    "%d jinja2 widget %s found (%d %s)"
                    % (
                        nb_file_found,
                        "file" if nb_file_found <= 1 else "files",
                        nb_macro_found,
                        "macro" if nb_file_found <= 1 else "macros",
                    )
                )
            )
            couple_visited = [(x[0], x[1]) for x in visited]
            duplicates = set(
                [t for t in couple_visited if couple_visited.count(t) > 1]
            )  # get the (widget.stem, macro.name) doublons
            for duplicate in duplicates:
                self.stdout.write(
                    self.style.WARNING(
                        "Warning : macro '%s' in a file named '%s' found more than once, could be ambiguous ; found in :"
                        % (duplicate[1], duplicate[0])
                    )
                )
                paths = [
                    x[2] for x in filter(lambda t: (t[0], t[1]) == duplicate, visited)
                ]  # get the paths corresponding to (widget.stem, macro.name)
                for p in paths:
                    self.stdout.write(self.style.WARNING("\t- %s" % p))

        else:
            call_command("list-widgets", "-django")
            self.stdout.write("\n")
            call_command("list-widgets", "-jinja2")
