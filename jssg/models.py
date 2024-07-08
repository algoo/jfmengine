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

import datetime
import json
import typing
from io import StringIO
from pathlib import Path
from typing import Iterator, Mapping, Optional, List

import markdown2
from django.conf import settings
from django.template import Context, Template, engines
from django.utils.text import slugify

from django.core.management.commands.runserver import Command as runserver

class Document:
    """A document.

    A text with some metadata

    This is a base class for more specialized document types
    """

    # Default dir to search document
    BASE_DIR = settings.JFME_CONTENT_DIRS

    def __init__(self, content: str, **metadata: Mapping[str, str]) -> None:
        """Create a new document.

        :param content: The content (body) of the document
        :param metadata: Associated metadata
        """
        self.body = content
        self.metadata = dict(metadata)
        self.path = metadata["path"]
        self.data = {}

    @property
    def content(self) -> str:
        """Render the content as markdown to html.

        Note: the content will be processed by the django template engine
        before being converted to html

        :return: the rendered document
        """
        import re
        # INFO DA 2024-02-18 - Replace "{{{ }}}" pattern into one-line pattern
        # this is usefull in order to exploit multi-line includes
        # {{{ include "block.html" with
        #     var1 = "some text"
        #     var2 = "another text"
        #     var3 = "a standard double-quote
        #             multiline text
        #             easy to read"
        # }}}

        # INFO - D.A. - Original code is below and is returned a markdown-based processed content
        # this works only with unindented HTML templates because markdown interprets indentation
        #
        # Expected: allow to process both HTML and markdown content types
        #
        # return markdown2.markdown(
        #     Template(self.body).render(
        #         Context(
        #             {
        #                 "posts": sorted(
        #                     Post.load_glob(), key=lambda p: p.timestamp, reverse=True
        #                 ),
        #                 "data": self.data
        #             }
        #         )
        #     ),
        #     extras=["fenced-code-blocks", "tables"],
        # )


        if "template_engine" in self.metadata.keys() and self.metadata["template_engine"] == "django" :
            return Template(self.body).render(
                Context(
                    {
                        "posts": sorted(
                            Post.load_glob(), key=lambda p: p.timestamp, reverse=True
                        ),
                        "data": self.data
                    }
                )
            )
        else :
            return engines["jinja2"].from_string(self.body).render(
                {
                    "posts": sorted(
                        Post.load_glob(), key=lambda p: p.timestamp, reverse=True
                    ),
                    "data":self.data
                }
            )

    @classmethod
    def load(cls, path: Path) -> "Document":
        """Load a document.

        :param path: Path to the document
        :return: The loaded document
        """
        _path = path
        metadata = {}
        data = {}
        json_data = ""
        content = StringIO()

        with path.open() as f:
            # States:
            # 0: search the metadata start block
            # 1: parse the metadata
            # 2: parse the metadata
            # 3: parse the content
            state = 0
            for line in f:
                if state == 0:
                    # Search the metadata start block
                    # The metadata start block is expected to be on the first line
                    if line.rstrip().startswith("---"):
                        # Metadata start block found
                        state = 1
                    else:
                        # Metadata start block not found, abort
                        break
                elif state == 1:
                    if line.rstrip().startswith("---"):
                        # Metadata end block found
                        state = 2
                    else:
                        if line.strip() == "":  # ignore empty lines
                            continue
                        if line.startswith("#"):  # ignore comment lines
                            continue

                        # Parse a metadata key value pair
                        # key, value = map(str.strip, line.split("", maxsplit=1))
                        import re
                        key, value = map(str.strip, re.split("[\s]", line, maxsplit=1))
                        # FIXME  print("KEY {} : {} (line is: {})".format(key, value, line))
                        metadata[key] = value
                elif state == 2:
                    if line.rstrip().startswith("---"):
                        # data end block found
                        # FIXME print("json reading finished: {}".format(json_data))
                        data = json.loads(json_data)
                        state = 3
                    else:
                        if line.strip() == "":
                            continue  # remove empty lines
                        if line.startswith("#"):
                            continue  # remove comment lines

                        # FIXME print("json data: append {}".format(line))
                        json_data += line

                else:
                    # Read the content
                    content.write(line)

        if state == 0:
            # Empty document or document not starting by a metadata block
            raise ValueError(
                f"Document {path.resolve()} doesn't start with a meta-data block"
            )
        elif state == 1:
            # Metadata end block not found
            raise ValueError(
                f"Document {path.resolve()}'s meta-data block doesn't have an end"
            )

        metadata["path"] = path
        metadata["json"] = json_data
        metadata["data"] = data

        obj = cls(content=content.getvalue(), **metadata)
        obj.data = data
        return obj

    @classmethod
    def load_glob(
        cls, path: Optional[List[Path]] = None, glob: str = "*.md"
    ) -> Iterator["Document"]:
        """Load multiple document.

        :param path: The base path
        :param glob: The glob pattern
        :return: The documents that match the pattern
        """
        if path is None:
            path = cls.BASE_DIR

        if path is None:
            raise RuntimeError("No path and no self.BASE_DIR defined")
        
        files = []
        for p in path :
            files += p.glob(glob)
        # print(files)
        return map(cls.load, files)


class Page(Document):
    """A webpage, with a title and some content."""

    BASE_DIR = settings.JFME_PAGES_DIRS

    def __init__(self, content: str, **metadata) -> None:
        """Create a new page.

        :param content: The content (body) of the page
        :param metadata: Associated metadata
        """
        super().__init__(content, **metadata)
        self.title = metadata["title"]
        try:
            self.slug = metadata["slug"]
        except KeyError:
            self.slug = slugify(self.title)

    @classmethod
    def load_page_with_slug(cls, slug: str) -> "Page":
        return next(filter(lambda p: p.slug == slug, cls.load_glob()))

    @classmethod
    def load_glob(
        cls, path: Optional[List[Path]] = None, glob: str = "*.md"
    ) -> Iterator["Page"]:
        """Overridden only to make the static typing happy."""
        return super().load_glob(path, glob)
    
    @classmethod
    def get_pages(cls):
        return ({"slug": p.slug} for p in Page.load_glob())


class Post(Page):
    """A webblog post."""

    BASE_DIR = settings.JFME_POSTS_DIRS

    def __init__(self, content: str, **metadata) -> None:
        """Create a new post.

        :param content: The content (body) of the page
        :param metadata: Associated metadata
        """
        super().__init__(content, **metadata)
        self.timestamp = datetime.datetime.fromisoformat(metadata["date"])

    @classmethod
    def load_glob(
        cls, path: Optional[List[Path]] = None, glob: str = "*.md"
    ) -> Iterator["Post"]:
        """Overridden only to make the static typing happy."""
        return super().load_glob(path, glob)

    @classmethod
    def get_posts(cls):
        return ({"slug": p.slug} for p in Post.load_glob())

class Sitemap :
    BASE_DIR = settings.JFME_PAGES_DIRS + settings.JFME_POSTS_DIRS
    domain = settings.JFME_DOMAIN
    pages_slugs = [p["slug"] for p in Page.get_pages()]
    posts_slugs = [p["slug"] for p in Post.get_posts()]
