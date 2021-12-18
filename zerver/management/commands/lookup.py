import os
import datetime
from re import search
from time import sleep

from django.core.management.base import BaseCommand
from googleapiclient.discovery import build

from zerver.models import SearchResults


DEVELOPER_KEY = os.environ['YOUTUBE_API_KEY']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
SYNC_INTERVAL = int(os.environ['SYNC_INTERVAL'] if 'SYNC_INTERVAL' in os.environ else 10)


def lookup(query, result, published_time, page_token=None):
    """Search Queries in youtube and return result"""

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    search = youtube.search().list(
        q=query,
        type='video',
        order='date',
        part='id,snippet',
        publishedAfter=published_time,
        pageToken=page_token,
        maxResults=result
    ).execute()
    return search

def save_youtube_videos(new_video):
    """Save Youtube videos to database"""

    for video in new_video['items']:
        SearchResults.objects.create(ids=video['id']['videoId'],
                                     published_datetime=video['snippet']['publishedAt'],
                                     title=video['snippet']['title'],
                                     description=video['snippet']['description'],
                                     thumbnail_url=video['snippet']['thumbnails']['medium']['url'])


class Command(BaseCommand):
    """Django command to sync the DB with youtube API at specific interval"""

    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('Sync Service Started...')

        while True:
            
            videos = SearchResults.objects.all().order_by('-published_datetime')
            if videos.exists():
                published_time = videos.first().published_datetime.replace(
                    tzinfo=None)
            else:
                published_time = datetime.datetime.utcnow() - \
                                  datetime.timedelta(minutes=30)

            next_page = None
            published_after_str = published_time.isoformat("T") + "Z"

            while True:

                new_videos = lookup('football',
                                            50,
                                            published_after_str,
                                            next_page)

                save_youtube_videos(new_videos)


                if 'nextPageToken' in new_videos:
                    next_page = new_videos['nextPageToken']
                else:
                    break
            self.stdout.write("Sync Completed successfully at {}".format(
                datetime.datetime.utcnow()))

            
            sleep(SYNC_INTERVAL)