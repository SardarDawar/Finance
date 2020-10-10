from django.shortcuts import render
from .models import Blog
from django.http import Http404
from django.core.paginator import Paginator
from django.views.generic import ListView

LATEST_BLOGS_COUNT = 3
BLOGS_PER_PAGE = 6

class BlogList(ListView):
    model = Blog
    paginate_by = BLOGS_PER_PAGE
    template_name = 'blogs/blogs.html'
    context_object_name = 'blogs'
    ordering = ['-dt_creation']    

def blog(request, slug):
    try:
        blog = Blog.objects.get(slug__iexact=slug)
    except Blog.DoesNotExist:
        raise Http404(f"Blog does not exist.")
    latest_blogs = Blog.objects.all()[:LATEST_BLOGS_COUNT]
    context = {
        'blog': blog,
        'latest_blogs': latest_blogs,
    }
    return render(request, 'blogs/blog.html', context)