
import os

from django.conf import settings as django_settings

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render, redirect
from feeds.models import Feed

from peekstudy.decorators import ajax_required

from django.http import (HttpResponse, HttpResponseBadRequest)
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from feeds.forms import PostForm
from PIL import Image

# Create your views here.
FEEDS_NUM_PAGES = 10


@login_required
def feeds(request):
    all_feeds = Feed.get_feeds()
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    feeds = paginator.page(1)
    from_feed = -1
    if feeds:
        from_feed = feeds[0].id
    return render(request, 'feeds/feeds.html', {
        'feeds': feeds,
        'from_feed': from_feed,
        'page': 1,
        })


@login_required
def compose(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.cleaned_data.get('post')
            feed = Feed(user=request.user, post=post)
            feed.save()
            post_images = django_settings.MEDIA_ROOT + '/post_images/'
            if not os.path.exists(post_images):
                os.makedirs(post_images)
            f = request.FILES['post_image']
            image_name = feed.date.strftime('%d%m%Y') + str(feed.pk) + '.jpg'
            filename = post_images + image_name
            with open(filename, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            im = Image.open(filename)
            width, height = im.size
            if width > 600:
                new_width = 600
                new_height = (height * 600) / width
                new_size = new_width, new_height
                im.thumbnail(new_size, Image.ANTIALIAS)
                im.save(filename)
                feed.post_image = '/post_images/' + image_name
                feed.save()
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'feeds/compose.html',
                      {'form': form})


def feed(request, pk):
    feed = get_object_or_404(Feed, pk=pk)
    return render(request, 'feeds/feed.html', {'feed': feed})


@login_required
@ajax_required
def load(request):
    from_feed = request.GET.get('from_feed')
    page = request.GET.get('page')
    feed_source = request.GET.get('feed_source')
    all_feeds = Feed.get_feeds(from_feed)
    if feed_source != 'all':
        all_feeds = all_feeds.filter(user__id=feed_source)
    paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
    try:
        feeds = paginator.page(page)
    except PageNotAnInteger:
        return HttpResponseBadRequest()
    except EmptyPage:
        feeds = []
    html = ''
    csrf_token = (csrf(request)['csrf_token'])
    for feed in feeds:
        html = '{0}{1}'.format(html,
                               render_to_string('feeds/partial_feed.html',
                                                {
                                                    'feed': feed,
                                                    'user': request.user,
                                                    'csrf_token': csrf_token
                                                    }))

    return HttpResponse(html)

