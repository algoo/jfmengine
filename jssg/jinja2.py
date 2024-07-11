from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment

from jssg.templatetags.filter_opengraph_metadata import filter_opengraph_metadata


from jssg.models import Page

def url_from_slug(slug) :
    url = ""
    pages_with_slug = ""

    for page in Page.load_glob(all=True) :
        if page.slug == slug :
            if pages_with_slug == "" :
                url = "/" + page.dir + "/" + page.slug + ".html"
            else :
                url = ""
            pages_with_slug += str(page.path.relative_to(page.page_dir.parent)) + ", "

    if url == "" and pages_with_slug != "" :
        raise Exception("url_slug() : slug '%s' is not unique, found in : [%s] ; use url_abs()" % (slug, pages_with_slug[:-2]))
    elif url == "" :
        raise Exception("url_slug() : slug '%s' not found" % slug)
    return url

def url_absolute(url_path) :
    dir = '/'.join(url_path.split('/')[:-1])
    slug = ''.join((''.join(url_path.split('/')[-1])).split('.')[0])

    for page in Page.get_pages() :
        if page["slug"] == slug and dir == "" :
            return "/" + slug + ".html"
        elif page["slug"] == slug and "dir" in page.keys() and page["dir"] == dir :
            return "/" + dir + "/" + slug + ".html"

    raise Exception("url_abs() : page for %s url not found" % url_path)

def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            "url_slug": url_from_slug,
            "url_abs" : url_absolute
        }
    )
    env.filters.update(
        {
            "filter_opengraph_metadata" : filter_opengraph_metadata
        }
    )
    return env