from django.templatetags.static import static
from django.urls import reverse
from django_jinja_markdown.templatetags.md import markdown
from jinja2 import Environment

from jssg.templatetags.filter_opengraph_metadata import filter_opengraph_metadata
from jssg.templatetags.filter_base64 import base64encode

from jssg.models import Page

import re

def url_for_slug(slug) :
    """
    @param slug: the slug of the page to search
    @return: the string of the url corresponding to the page
    @error: raise an exception if the slug does not exist or it is not unique (eg same slug found in several folders)

    >>> url_for_slug('index') # the slug exists and is unique
    /en/index.html

    >>> url_for_slug('index-duplicated') # the slug exists in several pages
    Traceback (most recent call last):
      ...
    Exception: slug 'index-duplicated' is not unique, found in : [pages/fr-index.md, pages/en-index.md] ; use url_for_slug_path()

    >>> url_for_slug('index-removed') # the slug does not exists
    Traceback (most recent call last):
      ...
    Exception: slug 'index-removed' not found

    """

    url = ""
    pages_with_slug = []

    for page in Page.load_glob(all=True) :
        if page.slug == slug : # the page exists
            if pages_with_slug == [] : # the slug has not been found yet
                if page.rel_folder_path != '' :
                    url = "/" + page.rel_folder_path + "/" + page.slug + ".html"
                else :
                    url = "/" + page.slug + ".html"
            else : # the slug already exists
                url = ""
            pages_with_slug.append(str(page.path.relative_to(page.content_page_dir.parent)))

    if url == "" and pages_with_slug != [] :
        raise Exception("slug '%s' is not unique, found in : [%s] ; use url_for_slug_path()" % (slug, ", ".join(pages_with_slug)))
    elif url == "" :
        raise Exception("slug '%s' not found" % slug)
    return url

def url_for_slug_path(url_path) :
    """
    @param url_path: the url of the page to search (absolute path)
    @return: the string of the slug url corresponding to the page
    @error: raise an exception if the url is a dead link

    >>> url_for_slug_path('/en/index') # the page exists
    /en/index.html

    >>> url_for_slug_path('/en/index-removed') # the page does not exist
    Traceback (most recent call last):
    ...
    Exception: page for '/en/index-removed' url not found (dead link)

    >>> url_for_slug_path('folder/index')
    Traceback (most recent call last):
      ...
    Exception: url 'folder/index' is not valid ; correct urls are /<dir>/<slug> or /<slug>

    """
    # Valid url are /<dir>/<slug>.html or /<slug>.html
    # Example: if url_path is "/tmp/folder/subfolder/thefile.html", then slug will be "thefile" and the dir will be "tmp/folder/subfolder"
    # Note : the dir does not start with '/' since the url parsed in url.py do not either
    try :
        _, dir, slug = re.findall(r"(^|^/([a-zA-Z0-9/-]+))/([a-zA-Z0-9-]+)$", url_path)[0]
    except :
        raise Exception("url '%s' is not valid ; correct urls are /<dir>/<slug> or /<slug>" % url_path)

    # Verify that the page exists
    for page in Page.load_glob(all=True) :
        if page.slug == slug and page.rel_folder_path == dir :
            return url_path + ".html"

    raise Exception("page for '%s' url not found (dead link)" % url_path)

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
            "filter_opengraph_metadata" : filter_opengraph_metadata,
            "base64encode" : base64encode
        }
    )
    return env