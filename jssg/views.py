# JSSG - Jtremesay's Static Site Generator
# Copyright (C) 2024 Jonathan Tremesaygues
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.
from pathlib import Path
from typing import List

from django.conf import settings
from django.contrib.syndication.views import Feed
from django.db.models.base import Model as Model
from django.shortcuts import render
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from django.views.generic import DetailView

from jssg.models import Page, Post, PostList


class PostFeedsView(Feed):
    title = "MY WEBSITE - last articles"
    link = ""
    feed_type = Atom1Feed

    def items(self) -> List[Post]:
        return sorted(Post.load_glob(), key=lambda p: p.timestamp, reverse=True)[:20]

    def item_title(self, post: Post) -> str:
        return post.title

    def item_description(self, item: Post):
        return item.content

    def item_link(self, post: Post) -> str:
        return reverse("post", args=(post.slug,))

    def item_pubdate(self, post: Post) -> str:
        return post.timestamp


class PageView(DetailView):
    model = Page
    template_name = "page.html"

    def get_object(self, queryset=None) -> Model:
        if "dir" not in self.kwargs.keys():
            self.kwargs["dir"] = ""
        model = self.model.load_page_with_slug(self.kwargs["slug"], self.kwargs["dir"])
        return model


class IndexView(PageView):
    model = Page
    template_name = "page.html"

    def get_object(self, queryset=None) -> Model:
        if len(settings.JFME_INDEX_PAGE.rsplit("/", 1)) > 1:
            self.kwargs["dir"], self.kwargs["slug"] = settings.JFME_INDEX_PAGE.rsplit(
                "/", 1
            )
        else:
            self.kwargs["dir"], self.kwargs["slug"] = (
                "",
                settings.JFME_INDEX_PAGE.rsplit("/", 1)[0],
            )
        return super().get_object(queryset)


class PostView(PageView):
    model = Post
    template_name = "post.html"


class PostListView(DetailView):
    template_name = "post-list.html"

    def get_object(self, queryset=None) -> Model:
        if "category" not in self.kwargs.keys():
            self.kwargs["category"] = ""
        return PostList.load_post_list_with_category(
            self.kwargs["category"], self.kwargs["page"]
        )

def jfme_seo_helper(request):

    pages = []
    for page in Page.load_glob(
            path=list(map(lambda p: Path(p).absolute(), settings.JFME_PAGES_DIRS)),
            all=True,
    ):
        og_image = page.metadata["og:image"]
        og_image = og_image.replace("https://" + settings.JFME_DOMAIN, "")
        og_image = og_image.replace("http://" + settings.JFME_DOMAIN, "")
        page.metadata["og:image_local_url"] = og_image  # HACK - D.A. - 2025-09-22 - Allow to show local images
        pages.append(page)

    # TODO - 2025-09-22 - D.A. - Also add blog articles to SEO helper page

    return render(request, "seo_page_list.html", {"pages": pages})