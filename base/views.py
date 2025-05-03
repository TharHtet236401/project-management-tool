from django.shortcuts import render
from .models import Project, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import LoginForm
# Create your views here.

@login_required(login_url='login')
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

@login_required(login_url='login')
def projects(request):
    projects = Project.objects.all()
    return render(request, 'base/projects.html', {'projects': projects})

@login_required(login_url='login')
def tasks(request):
    return render(request, 'base/tasks.html')

@login_required(login_url='login')
def team(request):
    try:
        team_members = Profile.objects.select_related('user').all()
        context = {
            'team_members': team_members,
        }
        return render(request, 'base/team.html', context)
    except Exception as e:
        return render(request, 'base/team.html', {'error': str(e)})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'base/login.html', {'error': 'Invalid username or password'})
    form = LoginForm()
    return render(request, 'base/login.html', {'form': form})

