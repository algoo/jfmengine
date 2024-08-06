from django.templatetags.static import static
from django.urls import reverse
from django_jinja_markdown.templatetags.md import markdown
from jinja2 import Environment
from django.core.management.base import BaseCommand

from jssg.templatetags.filter_opengraph_metadata import filter_opengraph_metadata
from jssg.templatetags.functions_url import url_for_slug, url_for_slug_path

from django.conf import settings

import importlib

def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            "markdown": markdown,
            "url_for_slug": url_for_slug,
            "url_for_slug_path" : url_for_slug_path
        }
    )
    env.filters.update(
        {
            "filter_opengraph_metadata" : filter_opengraph_metadata
        }
    )

    for templatetag in settings.JFME_ADDITIONAL_JINJA2_FUNCTIONS :
        module_name, function_name = settings.JFME_ADDITIONAL_JINJA2_FUNCTIONS[templatetag].rsplit('.', 1)
        try :
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)
        except(Exception) :
            command = BaseCommand()
            command.stdout.write(
                command.style.ERROR(
                    "Error: JFME_ADDITIONAL_JINJA2_FUNCTIONS: couldn't import '" + settings.JFME_ADDITIONAL_JINJA2_FUNCTIONS[templatetag] +"'"
                )
            )
        else :
            if templatetag not in env.globals :
                env.globals.update(
                    {
                        templatetag: function
                    }
                )
            else :
                command = BaseCommand()
                command.stdout.write(
                    command.style.ERROR(
                        "Error: JFME_ADDITIONAL_JINJA2_FUNCTIONS: '" + templatetag + "' function already exists"
                    )
                )

    for templatetag in settings.JFME_ADDITIONAL_JINJA2_FILTERS :
        module_name, function_name = settings.JFME_ADDITIONAL_JINJA2_FILTERS[templatetag].rsplit('.', 1)
        try :
            module = importlib.import_module(module_name)
            function = getattr(module, function_name)
        except(Exception) :
            command = BaseCommand()
            command.stdout.write(
                command.style.ERROR(
                    "Error: JFME_ADDITIONAL_JINJA2_FILTERS: couldn't import '" + settings.JFME_ADDITIONAL_JINJA2_FILTERS[templatetag] +"'"
                )
            )
        else :
            if templatetag not in env.filters :
                env.filters.update(
                    {
                        templatetag: function
                    }
                )
            else :
                command = BaseCommand()
                command.stdout.write(
                    command.style.ERROR(
                        "Error: JFME_ADDITIONAL_JINJA2_FILTERS: '" + templatetag + "' filter already exists"
                    )
                )

    return env