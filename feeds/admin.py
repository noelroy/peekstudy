from django.contrib import admin
from feeds.models import Feed, FeedComment
# Register your models here.

admin.site.register(Feed)
admin.site.register(FeedComment)