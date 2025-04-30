from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'base/home.html')

def projects(request):
    return render(request, 'base/projects.html')

def tasks(request):
    return render(request, 'base/tasks.html')


