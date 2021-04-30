from django.urls import path
from .feeds import LatestPostsFeed
from . views import (post_detail, post_share, post_list,
            comment_view, post_search, createpost
                )    #PostListView

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='published_posts'),
    #path('', PostListView.as_view(), name='published_posts'),
    path('<slug:slug>/<int:year>/<int:month>/<int:day>/',\
        post_detail, name='published_post_detail'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('<int:post_id>/comment', comment_view, name='comments'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', post_search, name='post_search'),
    path('create/<int:obj_id>', createpost, name='edit_post'),
    path('create/', createpost, name='create_post'),

]