from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from account.models import CustomUserModel
from django.urls import reverse
from taggit.managers import TaggableManager
import datetime


# class PublishedManager(models.Manager):
# def get_queryset(self):
# return super(PublishedManager, self).get_queryset()\
# .filter(status='published')

# We could achieve the same thing with a method.
# so am using the get_published() method


class Post(models.Model):
    # objects = models.Manager() # The default manager.
    # published = PublishedManager() # Our custom manager.

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    tags = TaggableManager()

    # next i need to setup imagefiled for each post.
    # post_image = models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return self.title

    def get_published():
        return Post.objects.all().filter(status="published")

    def activePost(self):
        return self.comments.all().filter(active=True)

    def daily_post():
        post_in_24hrs = Post.get_published().filter(
            created__gt=datetime.datetime.now() - datetime.timedelta(hours=24)
        )
        for post in post_in_24hrs:
            return post

    def get_absolute_url(self):
        return reverse(
            "blog:published_post_detail",
            args=[self.slug, self.publish.year, self.publish.month, self.publish.day],
        )


# Comments Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"

    def allComments():
        return Comment.objects.all()
