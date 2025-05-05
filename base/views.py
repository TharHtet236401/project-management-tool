from django.shortcuts import render
from .models import Project, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import LoginForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ProjectForm
from django.contrib import messages
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
    try:
        projects = Project.objects.all().order_by('-created_at')
        paginator = Paginator(projects, 10)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
        # If page is not an integer, deliver first page
            page_obj = paginator.page(1)
        except EmptyPage:
        # If page is out of range, deliver last page of results
            page_obj = paginator.page(paginator.num_pages)
        context = {
            'projects': page_obj,
        }
        return render(request, 'base/projects.html', context)
    except Exception as e:
        context = {
            'error': str(e)
        }
        return render(request, 'base/projects.html', context)

@login_required(login_url='login')
def project_detail(request, pk):
    try:
        project = Project.objects.get(id=pk)
        context = {
            'project': project
        }
        return render(request, 'base/project-detail.html', context)
    except Exception as e:
        context = {
            'error': str(e)
        }
        return render(request, 'base/project-detail.html', context)


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
    try:
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect('home')
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password test')
            
            context = {
                'form': form,
            }
            return render(request, 'base/login.html', context)
        
        return render(request, 'base/login.html', {'form': form})
    except Exception as e:
        context = {
            'form': form,
        }
        messages.error(request, 'An unexpected error occurred. Please try again.')
        return render(request, 'base/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def create_project(request):
    try:
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            if form.is_valid():
                project = form.save(commit=False)
                user = request.user
                profile = Profile.objects.get(user=user)
                project.members.add(profile)
                project.save()
                return redirect('projects')
            else:
                print("Form validation errors:", form.errors)
        else:
            form = ProjectForm()
        
        return render(request, 'base/project-create-form.html', {'form': form})
    except Exception as e:
        print("Exception occurred:", str(e))
        form = ProjectForm()
        form.add_error(None, f'Error creating project: {str(e)}')
        return render(request, 'base/project-create-form.html', {'form': form})
