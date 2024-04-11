from django.contrib import admin

from core_apps.bookmarks.models import Bookmark


@admin.register(Bookmark)
class ModelNameAdmin(admin.ModelAdmin):
    pass
