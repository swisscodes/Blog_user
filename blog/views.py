from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm
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
    context = {'post': post}
    
    return render(request, 'blog/detail.html', context)



class PostListView(ListView):
    queryset = Post.get_published()
    context_object_name = 'posts'
    paginate_by = 4
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