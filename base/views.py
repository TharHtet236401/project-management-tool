from django.shortcuts import render
from .models import Project, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import LoginForm, SignupForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ProjectForm
from django.contrib import messages
from django.http import HttpResponse
from django.core.cache import cache
# Create your views here.

@login_required(login_url='login')
def home(request):
    try:
        projects = Project.objects.all()
        team_members = Profile.objects.select_related('user').all()
        project_count = projects.count()
        team_count = team_members.count()
        
        # Try to get cached recent projects
        try:
            cache_key = 'recent_projects'
            print(f"Attempting to get cache with key: {cache_key}")
            cached_projects = cache.get(cache_key)
            print(f"Cache get result: {cached_projects}")
            
            if cached_projects is not None:
                recent_projects = cached_projects
                print("Using cached projects")
            else:
                # If not in cache, get from database and cache it
                recent_projects = list(projects.order_by('-id')[:5])
                print(f"Setting cache with key: {cache_key}")
                print(f"Projects to cache: {recent_projects}")
                cache_result = cache.set(cache_key, recent_projects, timeout=300)
                print(f"Cache set result: {cache_result}")
                
                # Verify cache was set
                verify_cache = cache.get(cache_key)
                print(f"Verification of cache after set: {verify_cache}")
                
        except Exception as cache_error:
            print(f"Cache error: {cache_error}")
            recent_projects = projects.order_by('-id')[:5]  # Fallback to database query
        
        context = {
            'projects': recent_projects,
            'team_members': team_members,
            'project_count': project_count,
            'team_count': team_count,
            'recent_projects': recent_projects,
        }
        return render(request, 'base/home.html', context)
    except Exception as e:
        print(f"Error in home view: {e}")
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
        print("login view is called")
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
        elif request.headers.get('HX-Request'):
            response = HttpResponse(render(request, 'partials/login-form.html', {'form': form}))
            response['hx-retarget'] = '#auth-container'
            print("retarget is true")
            return response
        else:
            print("retarget is false")
            return render(request, 'base/login.html', {'form': form})
    except Exception as e:
        context = {
            'form': form,
        }
        messages.error(request, 'An unexpected error occurred. Please try again.')
        return render(request, 'base/login.html', context)


def signup_view(request):
    try:
        if request.user.is_authenticated:
            return redirect('home')
            
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('login')
            else:
                messages.error(request, 'An error occurred: Please check your form this is from signup view.')
                print("error in signup view")
                response = HttpResponse(render(request, 'partials/signup-form.html', {'form': form}))
                response['hx-retarget'] = '#auth-container'
                return response
                
                
        else:
            form = SignupForm()
        
        return render(request, 'partials/signup-form.html', {'form': form})
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return render(request, 'partials/signup-form.html', {'form': form})

def logout_view(request):
    try:
        logout(request)
        if request.headers.get('HX-Request'):
            print("HX-Request is true")
            response = HttpResponse()
            response['HX-Redirect'] = '/login/'
            return response
    except Exception as e:
        if request.headers.get('HX-Request'):
            print("HX-Request is true")
            response = HttpResponse()
            response['HX-Redirect'] = '/login/'
            return response
        return redirect('login')


@login_required(login_url='login')
def create_project(request):
    try:
        if request.method == 'POST':
            form = ProjectForm(request.POST)
            if form.is_valid():
                project = form.save(commit=False)
                user = request.user
                try:
                    profile = Profile.objects.get(user=user)
                    project.save()  # Save the project first
                    project.members.add(profile)#add the profile to the project
                    profile.projects_assigned.add(project)  #add the project to the profile
                    return redirect('projects')
                except Profile.DoesNotExist:
                    messages.error(request, 'Profile not found. Please contact administrator.')
                    return render(request, 'base/project-create-form.html', {'form': form})
            else:
                return render(request, 'base/project-create-form.html', {'form': form})
        else:
            form = ProjectForm()
            return render(request, 'base/project-create-form.html', {'form': form})
    except Exception as e:
        form = ProjectForm(request.POST if request.method == 'POST' else None)
        messages.error(request, f'Error creating project: {str(e)}')
        return render(request, 'base/project-create-form.html', {'form': form})
