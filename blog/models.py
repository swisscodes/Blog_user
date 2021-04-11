from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



#class PublishedManager(models.Manager):
    #def get_queryset(self):
        #return super(PublishedManager, self).get_queryset()\
            #.filter(status='published')

# We could achieve the same thing with a method.
#so am using the get_published() method




class Post(models.Model):
    #objects = models.Manager() # The default manager.
    #published = PublishedManager() # Our custom manager.

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
        unique_for_date='publish')
    author = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
        choices=STATUS_CHOICES,
        default='draft')


    def get_published():
        return Post.objects.all().filter(status='published')
    

    def get_absolute_url(self):
        return reverse('blog:published_post_detail', args=[self.slug, self.publish.year,\
            self.publish.month, self.publish.day])


    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title