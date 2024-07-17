from typing import Any
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from jssg.models import Page, Post
from django.conf import settings

class MySitemap(Sitemap) :
    def get_urls(self, site=None, **kwargs):
        site = Site(domain=settings.JFME_DOMAIN, name=settings.JFME_DOMAIN)
        return super(MySitemap, self).get_urls(site=site, **kwargs)

class PageSitemap(MySitemap) :
    def items(self) :
        return list(Page.load_glob(all = True))
    def location(self, page) -> str:
        if page.rel_folder_path != '' :
            return "/" + page.rel_folder_path + "/" + page.slug + ".html"
        else :
            return "/" + page.slug + ".html"
        
class PostSitemap(MySitemap) :
    def items(self) :
        return list(Post.load_glob(all = True))
    def location(self, page) -> str:
        if page.rel_folder_path != '' :
            return "/posts/article/" + page.rel_folder_path + "/" + page.slug + ".html"
        else :
            return "posts/articles/" + page.slug + ".html"