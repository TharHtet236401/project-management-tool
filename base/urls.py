from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('projects/create/', views.create_project, name='create_project'),
    path('tasks/', views.tasks, name='tasks'),
    path('team/', views.team, name='team'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('project-detail/<int:pk>/', views.project_detail, name='project_detail'),
    path('signup/', views.signup_view, name='signup'),
]

