from django.shortcuts import render
from .models import Project
from django.http import Http404
from django.core.paginator import Paginator
from django.views.generic import ListView

LATEST_PROJECTS_COUNT = 3
PROJECTS_PER_PAGE = 4

class ProjectList(ListView):
    model = Project
    paginate_by = PROJECTS_PER_PAGE
    template_name = 'projects/projects.html'
    context_object_name = 'projects'
    ordering = ['-dt_project']    

def project(request, slug):
    try:
        project = Project.objects.get(slug__iexact=slug)
    except Project.DoesNotExist:
        raise Http404(f"Project does not exist.")
    latest_projects = Project.objects.all()[:LATEST_PROJECTS_COUNT]
    context = {
        'project': project,
        'latest_projects': latest_projects,
    }
    return render(request, 'projects/project.html', context)