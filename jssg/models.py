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
import re
from django.conf import settings
from django.template import Context, Template, engines
from django.utils.text import slugify

from django.core.management.commands.runserver import Command as runserver

from math import ceil


class EmptyLine(Exception):
    pass


class CommentLine(Exception):
    pass


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
        #
        # TODO - D.A. - 2024-09-09: implement in jinja2.py module
        # the possibility to import extra markdown extensions like 'fenced-code-blocks', etc

        if (
            "template_engine" in self.metadata.keys()
            and self.metadata["template_engine"] == "django"
        ):
            return Template(self.body).render(
                Context(
                    {
                        "posts": sorted(
                            Post.load_glob(), key=lambda p: p.timestamp, reverse=True
                        ),
                        "data": self.data,
                    }
                )
            )
        else:
            # TODO - D.A. - 2024-09-09 - Log markdown extensions for user usage
            # for mdext in engines["jinja2"].env.markdowner.registeredExtensions:
            #    print("Extension: ", mdext)
            return (
                engines["jinja2"]
                .from_string(self.make_imports() + self.body)
                .render(
                    {
                        "posts": sorted(
                            Post.load_glob(), key=lambda p: p.timestamp, reverse=True
                        ),
                        "data": self.data,
                    }
                )
            )

    @classmethod
    def process_metadata_substitutions(cls, metadata: dict) -> dict:
        """
        process substitutions in all metadata values.
        metadata are key/value pairs representing page or blog entry metadata.
        They may be static strings or dynamically referencign other metadata.
        They can also be composed of strings + other metadata values.

        Example:
        - lang         en
        - twitter:lang ((lang))
        - title        Product: ((og:title))
        - og:title     This is the title of the page
        - og:locale    ((twitter:lang))

        After substitutions, this will result in the following metadata:
        - lang         en
        - twitter:lang en
        - title        Product: This is the title of the page
        - og:title     This is the title of the page
        - og:locale    en

        The algorithm supports recursive substitutions and avoid infinite loops through cycle detection.
        """
        print("METADATA")
        for key in metadata:
            print(f"{key} -> {metadata[key]}")

        import re
        from copy import deepcopy

        substituted_metadata = deepcopy(metadata)

        # Keep track of previous states to detect cycles
        seen_states = set()
        iteration = 0

        substitution_pattern = re.compile(r'\(\(([^)]+)\)\)')  # match ((metadata_name)) patterns in metadata values

        while True:
            iteration += 1
            print(f"Substitution iteration {iteration}")

            # Create a hashable representation of current state
            current_state = tuple(
                sorted(
                    (k, v)
                    for k, v in substituted_metadata.items()
                    if isinstance(v, str) and k != "path"
                )
            )

            if current_state in seen_states:
                print(
                    "Cycle detected in substitutions. Stopping to prevent infinite loop."
                )
                break

            seen_states.add(current_state)
            changes_made = False

            for key, value in list(substituted_metadata.items()):
                if key == "path" or not isinstance(value, str):
                    continue

                print(f"processing substitution for {key} -> {value}")
                original_value = value
                new_value = value

                # Find all substitution patterns in the current value
                matches = substitution_pattern.findall(new_value)

                if matches:
                    print(f"  Found substitution patterns: {matches}")

                    # Apply substitutions for each found pattern
                    for metadata_name in matches:
                        pattern_to_replace = f"(({metadata_name}))"

                        # Check if the referenced metadata exists and is a string
                        if (metadata_name in substituted_metadata and
                                isinstance(substituted_metadata[metadata_name], str)):

                            replacement_value = substituted_metadata[metadata_name]
                            new_value = new_value.replace(pattern_to_replace, replacement_value)
                            print(f"    Replacing {pattern_to_replace} with '{replacement_value}'")
                        else:
                            print(f"    Warning: Referenced metadata '{metadata_name}' not found or not a string")

                # Check if this value changed
                if new_value != original_value:
                    substituted_metadata[key] = new_value
                    changes_made = True
                    print(
                        f"Replace metadata[{key}]: value from [{original_value}] to [{new_value}]"
                    )

            # If no changes were made, we're done
            if not changes_made:
                print("No more changes to make, substitution complete")
                break

        print(f"Substitution completed after {iteration} iterations")
        return substituted_metadata

    @classmethod
    def load(cls, path: Path) -> "Document":
        """Load a document.

        :param path: Path to the document
        :return: The loaded document
        """
        _path = path
        metadata = settings.JFME_DEFAULT_METADATA_DICT.copy()
        data = {}
        json_data = ""
        content = StringIO()

        with settings.JFME_DEFAULT_METADATA_FILEPATH.open() as f:
            for line in f:
                try:
                    # Parse a metadata key value pair
                    key, value = cls.parse_metadata_line(line)
                    metadata[key] = value
                except EmptyLine:  # ignore empty lines
                    continue
                except CommentLine:  # ignore comment lines
                    continue

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
                        try:
                            # Parse a metadata key value pair
                            key, value = cls.parse_metadata_line(line)
                            metadata[key] = value
                        except EmptyLine:  # ignore empty lines
                            continue
                        except CommentLine:  # ignore comment lines
                            continue
                elif state == 2:
                    if line.rstrip().startswith("---"):
                        # data end block found
                        # FIXME print("json reading finished: {}".format(json_data))
                        # data = json.loads(json_data)
                        state = 3
                    else:
                        try:
                            json_data += cls.parse_json_data_line(line)
                        except EmptyLine:  # ignore empty lines
                            continue
                        except CommentLine:  # ignore comment lines
                            continue
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

        metadata = cls.process_metadata_substitutions(metadata)
        metadata["path"] = path
        metadata["data"] = json.loads(json_data)

        obj = cls(content=content.getvalue(), **metadata)
        obj.data = data
        return obj

    @classmethod
    def load_glob(
        cls, path: Optional[List[Path]] = None, dir="", glob: str = "*.html", all=False
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
        for p in path:
            if all:
                files += (p / dir).rglob(glob)
            else:
                files += (p / dir).glob(glob)
        return map(cls.load, files)

    @classmethod
    def make_imports(cls):

        import_str = ""
        for template_dir in settings.JFME_TEMPLATES_DIRS:
            for widget_file in (template_dir / "jinja2" / "widgets").rglob("*"):
                if widget_file.is_file():
                    import_str += (
                        "{% "
                        + "import '{}' as {}".format(
                            widget_file.relative_to(template_dir / "jinja2"),
                            widget_file.stem,
                        )
                        + " %}\n"
                    )
        return import_str

    @classmethod
    def parse_metadata_line(cls, line):
        if line.strip() == "":  # ignore empty lines
            raise EmptyLine()
        if line.startswith("#"):  # ignore comment lines
            raise CommentLine(line)
        # key, value = map(str.strip, line.split("", maxsplit=1))
        return map(str.strip, re.split("[\s]", line, maxsplit=1))

    @classmethod
    def parse_json_data_line(cls, line: str):
        # TODO - D.A. - 2024-12-15 use an efficient json5 parser
        if line.strip() == "":  # ignore empty lines
            raise EmptyLine()
        if line.strip().startswith("#"):  # ignore comment lines, even if indented
            raise CommentLine(line)
        return line


class Page(Document):
    """A webpage, with a title and some content."""

    BASE_DIR = settings.JFME_PAGES_DIRS
    lastmod_format = settings.JFME_SITEMAP_LASTMOD_DATETIME_FORMAT

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

        self.content_page_dir = self.path
        while self.content_page_dir not in self.BASE_DIR:
            self.content_page_dir = self.content_page_dir.parent

        # page folder path relative to its content_page_dir
        self.rel_folder_path = str(self.path.relative_to(self.content_page_dir).parent)
        if self.rel_folder_path == ".":
            self.rel_folder_path = ""

    @classmethod
    def load_page_with_slug(cls, slug: str, dir: str) -> "Page":
        # for page in list(cls.load_glob(dir=dir)):
        #     print("Search for SLUG {slug} in {dir}, compare with page {pageslug}".format(slug=slug, dir=dir, pageslug=page.slug))
        #     if page.slug == slug:
        #        return page

        return next(filter(lambda p: p.slug == slug, cls.load_glob(dir=dir)))

    @classmethod
    def load_glob(
        cls, path: Optional[List[Path]] = None, dir="", glob: str = "*.html", all=False
    ) -> Iterator["Page"]:
        """Overridden only to make the static typing happy."""
        return super().load_glob(path, dir, glob, all)

    @classmethod
    def get_pages(cls):
        return (
            (
                {"slug": p.slug}
                if p.rel_folder_path == ""
                else {"dir": p.rel_folder_path, "slug": p.slug}
            )
            for p in Page.load_glob(all=True)
        )


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
        if "category" in self.metadata:
            self.metadata["category"] = slugify(self.metadata["category"])
        else:
            self.metadata["category"] = ""

    @classmethod
    def load_glob(
        cls, path: Optional[List[Path]] = None, dir="", glob: str = "*.md", all=False
    ) -> Iterator["Post"]:
        """Overridden only to make the static typing happy."""
        return super().load_glob(path, dir, glob, all)

    @classmethod
    def get_posts(cls):
        return (
            (
                {"slug": p.slug}
                if p.rel_folder_path == ""
                else {"dir": p.rel_folder_path, "slug": p.slug}
            )
            for p in Post.load_glob(all=True)
        )


class PostList:
    metadata = {"page_header_h1": "Posts"}
    category = ""

    def __init__(self, category="", page=1) -> None:
        self.category = category
        self.page = page

        if category == "":
            nb_posts = len(list(Post.load_glob(all=True)))
        else:
            nb_posts = len(
                list(
                    filter(
                        lambda p: p.metadata["category"] == self.category,
                        Post.load_glob(all=True),
                    )
                )
            )

        if settings.JFME_NUMBER_OF_POSTS_BY_PAGE > 0:
            self.posts_by_page = settings.JFME_NUMBER_OF_POSTS_BY_PAGE
        else:
            self.posts_by_page = nb_posts

        if self.posts_by_page > 0:
            self.nb_pages = ceil(
                nb_posts / self.posts_by_page
            )  # number of posts / number of posts by page

    @classmethod
    def load_post_list_with_category(cls, category, page):
        return cls(category, page)

    @property
    def categories(self):
        cat = set()
        for post in Post.load_glob(all=True):
            if post.metadata["category"] != "":
                cat.add(post.metadata["category"])
        return sorted(cat)

    @classmethod
    def get_categories_and_pages(cls):
        t = []
        for category in cls().categories:
            t += [
                {"category": category, "page": page}
                for page in range(1, cls(category).nb_pages + 1)
            ]
        return t

    def get_postlists(cls):
        return cls.get_categories_and_pages() + cls.get_pages()

    @classmethod
    def get_pages(cls):
        if len(list(Post.load_glob(all=True))) > 0:
            return [{"page": page} for page in range(1, cls().nb_pages + 1)]
        else:
            return []

    @property
    def posts(self):
        posts = sorted(
            Post.load_glob(all=True), key=lambda p: p.timestamp, reverse=True
        )
        if self.category == "":
            return posts[
                self.posts_by_page * (self.page - 1) : self.posts_by_page * (self.page)
            ]
        else:
            return list(
                filter(lambda p: p.metadata["category"] == self.category, posts)
            )[self.posts_by_page * (self.page - 1) : self.posts_by_page * (self.page)]
