from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.views.generic import ListView #not in use for now#
from .forms import EmailPostForm, CommentForm, SearchForm, UserPostForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from django.utils.text import slugify

# Create your views here.
@login_required
def post_list(request, tag_slug=None):
    post_items = Post.get_published()
    tag = None
    if(tag_slug):
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_items = post_items.filter(tags__in=[tag])
    paginator = Paginator(post_items, 3) # 3 posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    context = {'page': page, 'posts': posts, 'tag': tag}
    return render(request, 'blog/list.html', context)


@login_required
def post_detail(request, slug, year, month, day):
    post = get_object_or_404(Post, slug=slug, status='published', publish__year=year,\
        publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    #1. You retrieve a Python list of IDs for the tags of the current post. 
    # The values_list() QuerySet returns tuples with the values for the given fields. You
    #pass flat=True to it to get single values such as [1, 2, 3, ...] instead
    # of one-tuples such as [(1,), (2,), (3,) ...].
    post_tags_ids = post.tags.values_list('id', flat=True)
    ################Incase i need to use again ########################

    similar_posts = Post.get_published().filter(tags__in=post_tags_ids)\
        .exclude(id=post.id)
    similar_posts = similar_posts.annotate\
            (same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    context = {'post': post, 'comments': comments, 'new_comment': new_comment,\
        'comment_form': comment_form, 'similar_posts': similar_posts}
    return render(request, 'blog/detail.html', context)






"""class PostListView(ListView):
    queryset = Post.get_published()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/list.html'
"""


@login_required
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    
    if(request.method == 'POST'):
        form = EmailPostForm(request.POST)
        if(form.is_valid()):
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {'post': post, 'form':form, 'sent': sent}
    return render(request, 'blog/share.html', context)


@login_required
def comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    ok = Comment.allComments() #Total numbers of all Comments
    comments = post.activePost() #All active comments of this (self) object
    new_comment = None
    if(request.method=="POST"):
        form = CommentForm(request.POST)
        if(form.is_valid):
            comment_form = CommentForm(data=request.POST)

            #Here we create a new instance/object of our model comment with 
            #information from the POSTED request request.POST
            new_comment = comment_form.save(commit=False)

            # the new comment instance or object's post field = the post object
            #as this this a foriegn key we assign it here before saving.
            new_comment.post = post
            #***********************************#

            new_comment.save()
    else:
        form = CommentForm()
    context = {'form': form, 'post': post, 'comments': comments, 'new_comment': new_comment, 'ok': ok}
    return render(request, 'blog/comments.html', context)


@login_required
def post_search(request, query=None):
    form = SearchForm()
    results = []
    if('query' in request.GET):
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.get_published().annotate(similarity=TrigramSimilarity\
                ('title', query),).filter(similarity__gt=0.1).order_by('-similarity')
    context = {'form': form, 'query': query,'results': results}
    return render(request, 'blog/search.html', context)
    #In order to use trigrams in PostgreSQL, you will need to install the pg_trgm
    # extension first. Execute the following command from the shell to connect to your
    # database: psql blog Then, execute the following command to install
    # the pg_trgm extension: CREATE EXTENSION pg_trgm;


@login_required
def createpost(request, obj_id=None):
    post=None
    if obj_id:
        post = get_object_or_404(Post, id=obj_id)
    if((request.method=="POST") and ((request.POST['action']=="Create post") or (request.POST['action']=="Save post"))):
        create_form = UserPostForm(request.POST, instance=post)
        if(create_form.is_valid()):
            new_post_obj = create_form.save(commit=False)
            new_post_obj.author = request.user
            new_post_obj.slug = slugify(new_post_obj.title)
            new_post_obj.save()
            create_form.save_m2m()
            return HttpResponseRedirect(new_post_obj.get_absolute_url())
    elif(request.method=='POST'):
        post.delete()
        posts = Post.get_published()
        paginator = Paginator(posts, 3) # 3 posts per page
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context = {'page': page, 'posts': posts}
        return render(request, 'blog/list.html', context)

    if(request.method=="GET" and request.GET['action']=="delete"):
        context = {'post':post}
        return render(request, 'blog/delete.html', context)
    create_form = UserPostForm(instance = post)
    context = {'create_form': create_form, 'post': post}
    return render(request, 'blog/new_post.html', context)