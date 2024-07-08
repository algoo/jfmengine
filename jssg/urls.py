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
from jssg.models import Page, Post
from jssg import settings 

def get_pages() :
    return ({"slug": p.slug} if p.dir == '' else {"dir": p.dir, "slug" : p.slug} for p in Page.load_glob(all = True))

def get_posts() :
    return ({"slug": p.slug} if p.dir == '' else {"dir": p.dir, "slug" : p.slug} for p in Post.load_glob(all = True))

print([p for p in get_pages()])

urlpatterns = [
    distill_path(
        "", views.IndexView.as_view(), name="index", distill_file="index.html"
    ),
    distill_path("atom.xml", views.PostFeedsView(), name="atom_feed"),
    distill_re_path(
        r'^(?!posts/)(?P<slug>[a-zA-Z0-9-]+).html$',
        views.PageView.as_view(),
        name="page",
        distill_func=get_pages,
    ),
    distill_re_path(
        r'^(?!posts/)(?P<dir>[a-zA-Z-/]+)/(?P<slug>[a-zA-Z0-9-]+).html$',
        views.PageView.as_view(),
        name="page",
        distill_func=get_pages,
    ),
    distill_path(
        "posts/<slug:slug>.html",
        views.PostView.as_view(),
        name="post",
        distill_func=get_posts,
    ),
    distill_path(
        "posts/<path:dir>/<slug:slug>.html",
        views.PostView.as_view(),
        name="post",
        distill_func=get_posts,
    )
]
