from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from PIL import ImageFile
import bleach
from activities.models import Activity


# Create your models here.

@python_2_unicode_compatible
class Feed(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=500)
    post_image = models.ImageField(upload_to='post_images',null=True,blank=True)
    parent = models.ForeignKey('Feed', null=True, blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')
        ordering = ('-date',)

    def __str__(self):
        return self.post

    @staticmethod
    def get_feeds(from_feed=None):
        if from_feed is not None:
            feeds = Feed.objects.filter(parent=None, id__lte=from_feed)
        else:
            feeds = Feed.objects.filter(parent=None)
        return feeds

    def calculate_upvotes(self):
        likes = Activity.objects.filter(activity_type=Activity.UP_VOTE,
                                        feed=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def calculate_downvotes(self):
        likes = Activity.objects.filter(activity_type=Activity.DOWN_VOTE,
                                        feed=self.pk).count()
        self.likes = likes
        self.save()
        return self.likes

    def calculate_comments(self):
        self.comments = FeedComment.objects.filter(feed=self).count()
        self.save()
        return self.comments

    def comment(self, user, comment):
        feed_comment = FeedComment(user=user, comment=comment, feed=self)
        feed_comment.save()
        self.comments = FeedComment.objects.filter(feed=self).count()
        self.save()
        return feed_comment

    def get_upcounts(self):
        upcounts = Activity.objects.filter(activity_type=Activity.UP_VOTE,
                                        feed=self.pk)
        return upcounts

    def get_upcounters(self):
        upcounts = self.get_upcounts()
        upcounters = []
        for upcount in upcounts:
            upcounters.append(upcount.user)
        return upcounters

    def get_downcounts(self):
        downcounts = Activity.objects.filter(activity_type=Activity.DOWN_VOTE,
                                        feed=self.pk)
        return downcounts

    def get_downcounters(self):
        downcounts = self.get_downcounts()
        downcounters = []
        for downcount in downcounts:
            downcounters.append(downcount.user)
        return downcounters

    def linkfy_post(self):
        return bleach.linkify(escape(self.post))

    def get_comments(self):
        return FeedComment.objects.filter(feed=self).order_by('date')

@python_2_unicode_compatible
class FeedComment(models.Model):
    feed = models.ForeignKey(Feed)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    class Meta:
        verbose_name = _("Feed Comment")
        verbose_name_plural = _("Feed Comments")
        ordering = ("date",)

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.feed.pk)
