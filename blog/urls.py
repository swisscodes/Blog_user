from django.urls import path
from django.urls.resolvers import URLPattern
from . views import PostListView, post_detail, post_share #post_list,

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='published_posts'),
    path('<slug:slug>/<int:year>/<int:month>/<int:day>/',\
        post_detail, name='published_post_detail'),
    path('<int:post_id>/share/', post_share, name='post_share'),
]