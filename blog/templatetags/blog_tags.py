from django import template
from ..models import Post
from django.utils import timezone
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

# simple_tag: Processes the data and returns a string
@register.simple_tag
def total_post():
    return Post.get_published().count()


# inclusion_tag: Processes the data and returns a rendered template
@register.inclusion_tag("blog/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.get_published().filter(
        created__gt=timezone.now() - timezone.timedelta(hours=24)
    )[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return (
        Post.get_published()
        .annotate(total_comments=Count("comments"))
        .order_by("-total_comments")[:count]
    )


# Creating a custom filter tag
@register.filter(name="markdown_tag")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag
def current_year():
    return "2021-" + timezone.now().strftime("%Y")
