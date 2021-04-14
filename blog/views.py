from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail


# Create your views here.

"""def post_list(request):
    post_items = Post.get_published()
    paginator = Paginator(post_items, 3) # 3 posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'page': page, 'posts': posts}

    return render(request, 'blog/list.html', context)
"""

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

    context = {'post': post, 'comments': comments, 'new_comment': new_comment,\
        'comment_form': comment_form}
    return render(request, 'blog/detail.html', context)






class PostListView(ListView):
    queryset = Post.get_published()
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/list.html'



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



def comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    ok = Comment.allComments()
    comments = post.activePost()
    new_comment = None
    if(request.method=="POST"):
        form = CommentForm(request.POST)
        if(form.is_valid):
            comment_form = CommentForm(data=request.POST)
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        form = CommentForm()
    context = {'form': form, 'post': post, 'comments': comments, 'new_comment': new_comment, 'ok': ok}
    return render(request, 'blog/comments.html', context)