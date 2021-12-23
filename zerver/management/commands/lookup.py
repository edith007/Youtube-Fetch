import os
import datetime
from re import search
from time import sleep

from django.core.management.base import BaseCommand
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from uritemplate import api

from zerver.models import SearchResults
from backend_apis.models import Backend_apis

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
SYNC_INTERVAL = int(
    os.environ["SYNC_INTERVAL"] if "SYNC_INTERVAL" in os.environ else 10
)


def lookup(backend_api, query, result, published_time, page_token=None):
    """Search Queries in youtube and return result"""

    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=backend_api
    )

    try:
        search = (
            youtube.search()
            .list(
                q=query,
                type="video",
                order="date",
                part="id,snippet",
                publishedAfter=published_time,
                pageToken=page_token,
                maxResults=result,
            )
            .execute()
        )
        return search
    except HttpError as e:
        raise e


def save_youtube_videos(new_video):
    """Save Youtube videos to database"""

    for video in new_video["items"]:

        video_in_db = SearchResults.objects.filter(ids=video["id"]["videoId"])
        if video_in_db.exists():
            continue

        SearchResults.objects.create(
            ids=video["id"]["videoId"],
            published_datetime=video["snippet"]["publishedAt"],
            title=video["snippet"]["title"],
            description=video["snippet"]["description"],
            thumbnail_url=video["snippet"]["thumbnails"]["medium"]["url"],
        )


class Command(BaseCommand):
    """Django command to sync the DB with youtube API at specific interval"""

    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write("Sync Service Started...")

        api_keys = Backend_apis.objects.all()
        current_api = api_keys.first().key if api_keys.exists() else "random"
        current_api_number = 0

        while True:

            try:
                videos = SearchResults.objects.all().order_by("-published_datetime")
                if videos.exists():
                    published_time = videos.first().published_datetime.replace(
                        tzinfo=None
                    )
                else:
                    published_time = datetime.datetime.utcnow() - datetime.timedelta(
                        minutes=30
                    )

                next_page = None
                published_after_str = published_time.isoformat("T") + "Z"

                while True:

                    new_videos = lookup(
                        current_api, "football", 50, published_after_str, next_page
                    )

                    num_videos = len(new_videos["items"])
                    if num_videos > 0:
                        save_youtube_videos(new_videos)

                    if "nextPageToken" in new_videos:
                        next_page = new_videos["nextPageToken"]
                    else:
                        break
                self.stdout.write(
                    "Sync Completed successfully at {}".format(
                        datetime.datetime.utcnow()
                    )
                )
            except HttpError as e:
                api_keys = Backend_apis.objects.all()
                if not api_keys.exists():
                    self.stdout.write("You don't have any existed API. Please add some")
                    break
                if e.resp["status"] == "403":
                    self.stdout.write("API error")
                    current_api_number = (current_api_number + 1) % api_keys.count()
                    current_api = api_keys[current_api_number].key
                    if current_api_number ==  api_keys.count() - 1:
                        break
                    else:
                        continue
                else:
                    self.stderr.write("Error calling API")
            finally:

                sleep(SYNC_INTERVAL)
