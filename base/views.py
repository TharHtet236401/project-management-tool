from django.shortcuts import render
from .models import Project
# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def projects(request):
    projects = Project.objects.all()
    return render(request, 'base/projects.html', {'projects': projects})

def tasks(request):
    return render(request, 'base/tasks.html')


