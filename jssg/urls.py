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
from django_distill import distill_path, distill_re_path

from jssg import views
from jssg.models import Page, Post, PostList
from jssg import settings 

from django.contrib.sitemaps.views import sitemap
from jssg.sitemaps import PageSitemap, PostSitemap, PostListSitemap, ConstantUrlSitemap

# print([p for p in Page.get_pages()])
# print([p for p in PostList.get_categories_and_pages()])

urlpatterns = [
    distill_path(
        "", views.IndexView.as_view(), name="index", distill_file="index.html"
    ),
    distill_re_path(
        r'^(?!posts/)(?P<slug>[a-zA-Z0-9-]+).html$',
        views.PageView.as_view(),
        name="page",
        distill_func=Page.get_pages,
    ),
    distill_re_path(
        r'^(?!posts/)(?P<dir>[a-zA-Z-/]+)/(?P<slug>[a-zA-Z0-9-]+).html$',
        views.PageView.as_view(),
        name="page",
        distill_func=Page.get_pages,
    ),

    distill_path("atom.xml", views.PostFeedsView(), name="atom_feed"),
    distill_path(
        "posts/page<int:page>.html",
        views.PostListView.as_view(),
        name = "post-index",
        distill_func = PostList.get_pages
    ),
    distill_path(
        "posts/category/<slug:category>/page<int:page>.html",
        views.PostListView.as_view(),
        name = "post-category",
        distill_func = PostList.get_categories_and_pages
    ),
    distill_path(
        "posts/articles/<slug:slug>.html",
        views.PostView.as_view(),
        name="post",
        distill_func=Post.get_posts,
    ),
    distill_path(
        "posts/articles/<path:dir>/<slug:slug>.html",
        views.PostView.as_view(),
        name="post",
        distill_func=Post.get_posts,
    ),
    
    distill_path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"constant-url": ConstantUrlSitemap, "page": PageSitemap, "posts": PostSitemap, "postlist":PostListSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    )
]
