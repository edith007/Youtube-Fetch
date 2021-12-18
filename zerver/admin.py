from django.contrib import admin

# Register your models here.
from zerver.models import SearchResults


class ZerverAdmin(admin.ModelAdmin):
    sorted_by = ('published_datetime',)
    list_display = ('ids', 'title', 'published_datetime')


admin.site.register(SearchResults)
