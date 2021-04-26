from django import template
from ..models import Post
from django.utils import timezone

register = template.Library()

@register.simple_tag
def total_post():
    return Post.get_published().count()



@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.get_published().filter(created__gt = timezone.now() - timezone.timedelta(hours = 24))[:count]
    return {'latest_posts': latest_posts}