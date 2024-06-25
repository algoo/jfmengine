from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment

from jssg.templatetags.filter_opengraph_metadata import filter_opengraph_metadata

from jssg.models import Document
from django.conf import settings

def url_from_slug(view_name, slug) :
    for path in settings.JSSG_PAGES_DIR :
        files = path.rglob("*.md")
        for f in files :
            doc = Document.load(f)
            if doc.metadata["slug"] == slug :
                return "/" / doc.path.relative_to(path).with_suffix('.html').parent / (doc.metadata["slug"] + ".html")

def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            "url_slug": url_from_slug,
        }
    )
    env.filters.update(
        {
            "filter_opengraph_metadata" : filter_opengraph_metadata
        }
    )
    return env