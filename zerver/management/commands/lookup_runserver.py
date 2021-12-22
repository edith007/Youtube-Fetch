import os
import asyncio

from django.core.management import call_command
from django.core.management.commands.runserver import Command as BaseCommand

loop = asyncio.get_event_loop()


def start_sync():
    print("Starting Sync with API...")
    call_command("lookup")


class Command(BaseCommand):
    """Command to run runserver and sync with API."""

    def handle(self, *args, **options):
        if os.environ.get("RUN_MAIN") != "true":
            loop.run_in_executor(None, start_sync)
        super(Command, self).handle(*args, **options)
