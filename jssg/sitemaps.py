from typing import Any
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from jssg.models import Page, Post, PostList
from django.conf import settings

class MySitemap(Sitemap) :
    def get_urls(self, site=None, **kwargs):
        site = Site(domain=settings.JFME_DOMAIN, name=settings.JFME_DOMAIN)
        return super(MySitemap, self).get_urls(site=site, **kwargs)

class ConstantUrlSitemap(MySitemap) :
    def items(self) :
        return ["/", "/atom.xml", "/sitemap.xml"]
    def location(self, url) -> str:
        return url

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
    def location(self, post) -> str:
        if post.rel_folder_path != '' :
            return "/posts/article/" + post.rel_folder_path + "/" + post.slug + ".html"
        else :
            return "/posts/articles/" + post.slug + ".html"
        
class PostListSitemap(MySitemap) :
    def items(self) :
        return PostList().get_postlists()
    def location(self, postlist) -> str:
        if "category" in postlist :
            return "/posts/category/" + postlist["category"] + "/page" + str(postlist["page"]) + ".html"
        else :
            return "/posts/category/page" + str(postlist["page"]) + ".html"