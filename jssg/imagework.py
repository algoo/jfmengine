"""
jssg.imagework — JPEG-to-WebP conversion and resize utilities.

Self-contained: no Django dependency in the core functions.
Use JFMEImageWork for a proxy with defaults from Django settings.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from PIL import Image, ImageOps


# ---------------------------------------------------------------------------
# Enums & dataclasses
# ---------------------------------------------------------------------------


class ResizeStrategy(Enum):
    FIT = "fit"            # Fit within box, preserve ratio (no crop, no stretch)
    FILLCROP = "fillcrop"  # Fill box exactly, center-crop excess
    MIN_FIT = "min_fit"    # Scale so both dims are >= target (no crop)
    STRETCH = "stretch"    # Exact dims, ignore aspect ratio


class ImageSize:
    """Image dimensions with dynamic width/height properties."""

    def __init__(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise ValueError(f"ImageSize dimensions must be positive, got {width}x{height}.")
        self._width = width
        self._height = height

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @classmethod
    def from_str(cls, s: str) -> ImageSize:
        """Parse '1024x512' into ImageSize(1024, 512)."""
        parts = s.lower().split("x")
        if len(parts) != 2:
            raise ValueError(f"Invalid size format {s!r}. Expected 'WxH' (e.g. '1024x512').")
        try:
            return cls(width=int(parts[0]), height=int(parts[1]))
        except ValueError:
            raise ValueError(f"Invalid size format {s!r}. Width and height must be positive integers.")

    def as_tuple(self) -> tuple[int, int]:
        return (self._width, self._height)

    def __str__(self) -> str:
        return f"{self._width}x{self._height}"

    def __repr__(self) -> str:
        return f"ImageSize({self._width}, {self._height})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ImageSize):
            return NotImplemented
        return self._width == other._width and self._height == other._height


@dataclass
class ConversionResult:
    source_path: Path     # Original path (now renamed to backup_path)
    backup_path: Path     # Original file kept with prefix
    output_path: Path     # New .webp file
    resized: bool
    quality: float        # WebP quality used (0.0–1.0)
    original_size: ImageSize
    output_size: ImageSize


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _backup_path(source: Path, prefix: str) -> Path:
    return source.parent / (prefix + source.name)


def _webp_path(source: Path) -> Path:
    return source.with_suffix(".webp")


def _read_size(image: Image.Image) -> ImageSize:
    return ImageSize(width=image.width, height=image.height)


def _apply_resize(image: Image.Image, size: ImageSize, strategy: ResizeStrategy) -> Image.Image:
    target = size.as_tuple()

    if strategy == ResizeStrategy.STRETCH:
        return image.resize(target, Image.LANCZOS)

    if strategy == ResizeStrategy.FIT:
        # thumbnail modifies in-place; copy first to preserve original
        img = image.copy()
        img.thumbnail(target, Image.LANCZOS)
        return img

    if strategy == ResizeStrategy.FILLCROP:
        return ImageOps.fit(image, target, Image.LANCZOS)

    if strategy == ResizeStrategy.MIN_FIT:
        # Scale so that both dimensions are >= target (no cropping)
        ratio = max(target[0] / image.width, target[1] / image.height)
        new_w = int(image.width * ratio)
        new_h = int(image.height * ratio)
        return image.resize((new_w, new_h), Image.LANCZOS)

    raise ValueError(f"Unsupported strategy: {strategy}")  # pragma: no cover


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------

_STATIC_CONTENT_EXTENSIONS = (".html", ".md", ".js", ".css")


@dataclass
class FileReference:
    """A static content file that references a given image filename."""
    file_path: Path
    line_numbers: list[int]   # 1-based line numbers where the image name was found


def find_jpeg_files(folder: Path, ignore_prefix: str) -> list[Path]:
    """Recursively find .jpg/.jpeg files, skipping files whose name starts with ignore_prefix."""
    result = [
        p for p in folder.rglob("*")
        if p.is_file()
        and p.suffix.lower() in (".jpg", ".jpeg")
        and not p.name.startswith(ignore_prefix)
    ]
    return sorted(result)


def find_references(image_path: Path, search_folder: Path) -> list[FileReference]:
    """
    Search for occurrences of image_path.name inside static content files
    (.html, .md, .js, .css) found recursively under search_folder.

    Returns one FileReference per file that contains at least one match,
    with the 1-based line numbers of every matching line.
    """
    filename = image_path.name
    results: list[FileReference] = []

    candidates = (
        p for p in search_folder.rglob("*")
        if p.is_file() and p.suffix.lower() in _STATIC_CONTENT_EXTENSIONS
    )

    for candidate in sorted(candidates):
        matched_lines: list[int] = []
        try:
            for lineno, line in enumerate(candidate.read_text(errors="replace").splitlines(), start=1):
                if filename in line:
                    matched_lines.append(lineno)

        except OSError:
            continue

        if matched_lines:
            results.append(FileReference(file_path=candidate, line_numbers=matched_lines))

    return results


def substitute_reference(file_path: Path, old_name: str, new_name: str) -> int:
    """
    Replace every occurrence of old_name with new_name inside file_path.

    Returns the total number of substitutions made.
    """
    content = file_path.read_text(errors="replace")
    new_content, count = content.replace(old_name, new_name), content.count(old_name)
    if count:
        file_path.write_text(new_content)
    return count


def convert_jpeg_to_webp(
    source: Path,
    backup_prefix: str,
    quality: float = 0.75,
) -> ConversionResult:
    """
    Convert a JPEG to WebP in-place.

    The original file is renamed to <backup_prefix><original_name>.
    The new .webp file replaces the original path (same stem, .webp extension).
    quality is a float in [0.0, 1.0].
    """
    backup = _backup_path(source, backup_prefix)
    output = _webp_path(source)

    with Image.open(source) as img:
        original_size = _read_size(img)
        img.save(output, "WEBP", quality=int(quality * 100))

    source.rename(backup)

    return ConversionResult(
        source_path=source,
        backup_path=backup,
        output_path=output,
        resized=False,
        quality=quality,
        original_size=original_size,
        output_size=original_size,
    )


def convert_and_resize_jpeg_to_webp(
    source: Path,
    backup_prefix: str,
    size: ImageSize,
    strategy: ResizeStrategy,
    quality: float = 0.75,
) -> ConversionResult:
    """
    Convert a JPEG to WebP and resize it, in-place.

    The original file is renamed to <backup_prefix><original_name>.
    The new .webp file is resized according to size and strategy.
    quality is a float in [0.0, 1.0].
    """
    backup = _backup_path(source, backup_prefix)
    output = _webp_path(source)

    with Image.open(source) as img:
        original_size = _read_size(img)
        resized = _apply_resize(img, size, strategy)
        output_size = _read_size(resized)
        resized.save(output, "WEBP", quality=int(quality * 100))

    source.rename(backup)

    return ConversionResult(
        source_path=source,
        backup_path=backup,
        output_path=output,
        resized=True,
        quality=quality,
        original_size=original_size,
        output_size=output_size,
    )


# ---------------------------------------------------------------------------
# Django-aware proxy
# ---------------------------------------------------------------------------


class JFMEImageWork:
    """
    Proxy over the imagework functions with defaults injected at construction.

    Standalone usage (no Django):
        worker = JFMEImageWork(
            backup_prefix=".jfme-reworked__",
            default_size=ImageSize(1024, 512),
            default_strategy=ResizeStrategy.FILLCROP,
            default_quality=0.75,
        )

    Django usage (reads JFME_RESIZE_* from settings.py):
        worker = JFMEImageWork.from_django_settings()
    """

    def __init__(
        self,
        backup_prefix: str,
        default_size: ImageSize | None = None,
        default_strategy: ResizeStrategy | None = None,
        default_quality: float = 0.75,
    ) -> None:
        self.backup_prefix = backup_prefix
        self.default_size = default_size
        self.default_strategy = default_strategy
        self.default_quality = default_quality

    @classmethod
    def from_django_settings(cls) -> JFMEImageWork:
        """Build a JFMEImageWork instance from Django settings."""
        from django.conf import settings

        prefix: str = getattr(settings, "JFME_RESIZE_PREFIX", ".jfme-reworked__")

        size: ImageSize | None = None
        size_str: str = getattr(settings, "JFME_RESIZE_DEFAULT_SIZE", "")
        if size_str:
            size = ImageSize.from_str(size_str)

        strategy: ResizeStrategy | None = None
        strategy_str: str = getattr(settings, "JFME_RESIZE_DEFAULT_STRATEGY", "")
        if strategy_str:
            strategy = ResizeStrategy(strategy_str)

        quality: float = getattr(settings, "JFME_RESIZE_DEFAULT_QUALITY", 0.75)

        return cls(backup_prefix=prefix, default_size=size, default_strategy=strategy, default_quality=quality)

    # --- Proxy methods ---

    def find_jpeg_files(self, folder: Path) -> list[Path]:
        return find_jpeg_files(folder, self.backup_prefix)

    def convert(self, source: Path, quality: float | None = None) -> ConversionResult:
        return convert_jpeg_to_webp(source, self.backup_prefix, quality=quality or self.default_quality)

    def convert_and_resize(
        self,
        source: Path,
        size: ImageSize | None = None,
        strategy: ResizeStrategy | None = None,
        quality: float | None = None,
    ) -> ConversionResult:
        """
        Convert and resize. CLI overrides take priority over instance defaults.
        Raises ValueError if size or strategy cannot be resolved.
        """
        effective_size = size or self.default_size
        effective_strategy = strategy or self.default_strategy
        effective_quality = quality if quality is not None else self.default_quality

        if effective_size is None:
            raise ValueError(
                "No resize size available. Pass --size or set JFME_RESIZE_DEFAULT_SIZE in settings."
            )
        if effective_strategy is None:
            raise ValueError(
                "No resize strategy available. Pass --strategy or set JFME_RESIZE_DEFAULT_STRATEGY in settings."
            )

        return convert_and_resize_jpeg_to_webp(
            source=source,
            backup_prefix=self.backup_prefix,
            size=effective_size,
            strategy=effective_strategy,
            quality=effective_quality,
        )

    def find_references(self, image_path: Path, search_folder: Path) -> list[FileReference]:
        """Search for image_path.name in static content files under search_folder."""
        return find_references(image_path, search_folder)

    def substitute_reference(self, file_path: Path, old_name: str, new_name: str) -> int:
        """Replace old_name with new_name in file_path. Returns substitution count."""
        return substitute_reference(file_path, old_name, new_name)
