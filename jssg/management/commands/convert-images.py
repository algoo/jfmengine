from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from jssg.imagework import ImageSize, JFMEImageWork, ResizeStrategy


class Command(BaseCommand):
    help = "Convert JPEG images to WebP format in-place, with optional resize."

    def add_arguments(self, parser):
        source_group = parser.add_mutually_exclusive_group(required=True)
        source_group.add_argument(
            "--folder-path",
            type=str,
            help="Process all JPEG files found recursively in this folder.",
        )
        source_group.add_argument(
            "--file-path",
            type=str,
            help="Process a single JPEG file.",
        )
        parser.add_argument(
            "--strategy",
            type=str,
            choices=[s.value for s in ResizeStrategy],
            help="Resize strategy (overrides JFME_RESIZE_DEFAULT_STRATEGY).",
        )
        parser.add_argument(
            "--size",
            type=str,
            help="Resize dimensions e.g. '1024x512' (overrides JFME_RESIZE_DEFAULT_SIZE).",
        )
        parser.add_argument(
            "--quality",
            type=float,
            help="WebP quality as a float in [0.0, 1.0] (overrides JFME_RESIZE_DEFAULT_QUALITY).",
        )
        parser.add_argument(
            "--static-content-folder",
            type=str,
            default=None,
            help=(
                "If given, search .html/.md/.js/.css files in this folder for references "
                "to converted images and offer to substitute the filename in-place."
            ),
        )

    def handle(self, *args, **options):
        worker = JFMEImageWork.from_django_settings()

        cli_size = ImageSize.from_str(options["size"]) if options.get("size") else None
        cli_strategy = ResizeStrategy(options["strategy"]) if options.get("strategy") else None
        cli_quality: float | None = options.get("quality")

        static_content_folder: Path | None = None
        if options.get("static_content_folder"):
            static_content_folder = Path(options["static_content_folder"])
            if not static_content_folder.is_dir():
                raise CommandError(f"Not a directory: {static_content_folder}")

        if options["folder_path"]:
            folder = Path(options["folder_path"])
            if not folder.is_dir():
                raise CommandError(f"Not a directory: {folder}")
            files = worker.find_jpeg_files(folder)
        else:
            p = Path(options["file_path"])
            if not p.is_file():
                raise CommandError(f"Not a file: {p}")
            files = [p]

        if not files:
            self.stdout.write(self.style.WARNING("No JPEG files found."))
            return

        effective_size = cli_size or worker.default_size
        effective_strategy = cli_strategy or worker.default_strategy
        effective_quality = cli_quality if cli_quality is not None else worker.default_quality

        for file in files:
            backup = file.parent / (worker.backup_prefix + file.name)
            output = file.with_suffix(".webp")

            answer = self._prompt_user(file, backup, output, effective_size, effective_strategy, effective_quality)

            if answer == "n":
                self.stdout.write(self.style.WARNING("  Skipped."))
                continue

            try:
                if answer == "y":
                    result = worker.convert(file, quality=cli_quality)
                else:  # r
                    result = worker.convert_and_resize(file, size=cli_size, strategy=cli_strategy, quality=cli_quality)
            except ValueError as e:
                raise CommandError(str(e))

            self.stdout.write(
                self.style.SUCCESS(
                    f"  Done: {result.output_path}  "
                    f"({result.original_size} -> {result.output_size})"
                )
            )

            if not static_content_folder:
                self.stdout.write(self.style.WARNING(f"  Skip usage substitution for file {file.name}."))
            else:
                self.stdout.write(f"\n  Prepare substitutions for file {file.name}.")
                self._handle_references(worker, result.source_path, result.output_path, static_content_folder)

    def _prompt_user(
        self,
        file: Path,
        backup: Path,
        output: Path,
        size: ImageSize | None,
        strategy: ResizeStrategy | None,
        quality: float,
    ) -> str:
        self.stdout.write(f"\n--------------------------------------------------------------------------------\n")
        self.stdout.write(f"\nAbout to process a JPEG file")
        self.stdout.write(f"\n  File:    {file}")
        self.stdout.write(f"  Backup:  {backup}")
        self.stdout.write(f"  Output:  {output}")
        self.stdout.write(f"  Quality: {quality:.0%}")
        if size and strategy:
            self.stdout.write(f"  Resize:  {size}  strategy={strategy.value}")
        else:
            self.stdout.write("  Resize:  not configured (r will fail)")

        while True:
            answer = input("  Convert? [n=no / y=yes / r=yes+resize]: ").strip().lower()
            if answer in ("n", "y", "r"):
                return answer
            self.stdout.write(self.style.WARNING("  Please enter n, y, or r."))

    def _handle_references(
        self,
        worker: JFMEImageWork,
        original_path: Path,
        output_path: Path,
        search_folder: Path,
    ) -> None:
        old_name = original_path.name
        new_name = output_path.name

        refs = worker.find_references(original_path, search_folder)
        if not refs:
            self.stdout.write(f"  No reference found.")
            return

        for ref in refs:
            lines_str = ", ".join(str(n) for n in ref.line_numbers)
            self.stdout.write(
                f"\n    File {self.style.SUCCESS(old_name)} is referenced in "
                f"{self.style.WARNING(ref.file_path.name)} "
                f"at line{'s' if len(ref.line_numbers) > 1 else ''} {lines_str}"
                f" [{ref.file_path}]"
            )

            answer = input(f"    Substitute {self.style.SUCCESS(old_name)} → {self.style.WARNING(new_name)}? [y/n]: ").strip().lower()
            while answer not in ("y", "n"):
                answer = input(f"    Please enter y or n: ").strip().lower()

            if answer == "y":
                count = worker.substitute_reference(ref.file_path, old_name, new_name)
                self.stdout.write(self.style.SUCCESS(f"    Replaced {count} occurrence(s) in {ref.file_path.name}."))
