from datetime import datetime

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site

from jssg.models import Page, Post, PostList


class MySitemap(Sitemap):
    # Overriding get_url() to specify the domain name
    def get_urls(self, site=None, **kwargs):
        site = Site(domain=settings.JFME_DOMAIN, name=settings.JFME_DOMAIN)
        self.protocol = "https"
        return super(MySitemap, self).get_urls(site=site, **kwargs)

    def items(self):
        """
        All child classes must NOT implement this method.
        instead, they must implement the _jssg_sitemap_items() method
        """
        from django.conf import settings
        items = []
        found_items = self._jssg_sitemap_items()
        # Exclude items if their location is found in locations to exclude
        items = [item for item in found_items if self.location(item) not in settings.JFME_SITEMAP_EXCLUDED_LOCATIONS]

        return items

    def _jssg_sitemap_items(self):
        """
        This method must be implemented by child classes.
        """
        raise NotImplementedError()


class ConstantUrlSitemap(MySitemap):
    def _jssg_sitemap_items(self):
        if len(list(Post.load_glob(all=True))) > 0:
            return ["/", "/atom.xml", "/sitemap.xml"]
        else:
            return ["/", "/sitemap.xml"]

    def location(self, url) -> str:
        return url


class PageSitemap(MySitemap):
    def _jssg_sitemap_items(self):
        return list(Page.load_glob(all=True))

    def location(self, page) -> str:
        if page.rel_folder_path != "":
            return "/" + page.rel_folder_path + "/" + page.slug + ".html"
        else:
            return "/" + page.slug + ".html"

    def lastmod(self, post):
        return datetime.fromtimestamp(post.path.lstat().st_mtime)


class PostSitemap(MySitemap):
    def _jssg_sitemap_items(self):
        return list(Post.load_glob(all=True))

    def location(self, post) -> str:
        if post.rel_folder_path != "":
            return "/posts/article/" + post.rel_folder_path + "/" + post.slug + ".html"
        else:
            return "/posts/articles/" + post.slug + ".html"

    def lastmod(self, post):
        return datetime.fromtimestamp(post.path.lstat().st_mtime)


class PostListSitemap(MySitemap):
    def _jssg_sitemap_items(self):
        return PostList().get_postlists()

    def location(self, postlist) -> str:
        if "category" in postlist:
            return (
                "/posts/category/"
                + postlist["category"]
                + "/page"
                + str(postlist["page"])
                + ".html"
            )
        else:
            return "/posts/category/page" + str(postlist["page"]) + ".html"
