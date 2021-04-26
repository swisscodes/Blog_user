import datetime
from .models import Post
from django.utils import timezone

def daily_post(request):
    post_in_24hrs = Post.get_published().filter(created__gt = timezone.now() - timezone.timedelta(hours = 24))[:5]
    context = {'post_in_24hrs': post_in_24hrs}
    return context