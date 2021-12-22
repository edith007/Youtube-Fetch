from django.core import paginator
from django.core.paginator import Paginator, EmptyPage
from django.forms import model_to_dict
from django.http import JsonResponse
from zerver.models import SearchResults


def get_videos(request):
    """Return JSON Response"""

    if request.method != "GET":
        return JsonResponse({"details": "Method not allowed"}, status=405)

    videos = SearchResults.objects.all().order_by("-published_datetime")
    paginator = Paginator(videos, 50)
    page_no = int(request.GET.get("page") or "1")
    try:
        paginated_videos = paginator.page(page_no)
    except EmptyPage:
        return JsonResponse({"details": "Page not found"}, status=404)
    next_page = (
        paginated_videos.next_page_number() if paginated_videos.has_next() else None
    )
    prev_page = (
        paginated_videos.previous_page_number()
        if paginated_videos.has_previous()
        else None
    )
    return JsonResponse(
        {
            "next_page": next_page,
            "previous_page": prev_page,
            "videos": [model_to_dict(v) for v in list(paginated_videos)],
        }
    )
