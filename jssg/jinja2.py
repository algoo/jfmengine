from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment

from jssg.templatetags.filter_opengraph_metadata import filter_opengraph_metadata

def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
        }
    )
    env.filters.update(
        {
            "filter_opengraph_metadata" : filter_opengraph_metadata
        }
    )
    return env