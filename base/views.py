from django.shortcuts import render

# Create your views here.

def home(request):
    if request.headers.get('HX-Request'):
        return render(request, 'base/partials/home-partial.html')
    return render(request, 'base/home.html')

def projects(request):
    return render(request, 'base/projects.html')

def tasks(request):
    return render(request, 'base/tasks.html')


