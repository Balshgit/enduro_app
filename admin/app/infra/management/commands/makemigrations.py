import sys

from django.core.management.commands.makemigrations import Command as BaseCommand


class Command(BaseCommand):
    """Disable automatic names for django migrations"""

    def handle(self, *app_labels, **options):  # type: ignore
        if options["name"] is None and not any([options["dry_run"], options["check_changes"]]):
            print("Migration name (-n/--name) is required.", file=sys.stderr)  # noqa: T001, T201
            sys.exit(1)

        super().handle(*app_labels, **options)
