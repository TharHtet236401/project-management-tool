from django.shortcuts import render
from .models import Project, Profile
# Create your views here.

def home(request):
    try:
        projects = Project.objects.all()
        team_members = Profile.objects.select_related('user').all()
        project_count = projects.count()
        team_count = team_members.count()
        recent_projects = projects.order_by('-id')[:5]  # Show 5 most recent projects
        context = {
            'projects': projects,
            'team_members': team_members,
            'project_count': project_count,
            'team_count': team_count,
            'recent_projects': recent_projects,
        }
        return render(request, 'base/home.html', context)
    except Exception as e:
        # Optionally, log the error or show a friendly message
        return render(request, 'base/home.html', {'error': str(e)})

def projects(request):
    projects = Project.objects.all()
    return render(request, 'base/projects.html', {'projects': projects})

def tasks(request):
    return render(request, 'base/tasks.html')


