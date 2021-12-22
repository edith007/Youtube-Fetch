from django.urls import path

from zerver.views import get_videos

urlpatterns = [path("", get_videos)]
