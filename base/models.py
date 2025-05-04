from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = [
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('designer', 'Designer'),
    ]
    role = models.CharField(max_length=20, choices=roles)
    phone = models.CharField(max_length=20, blank=True)
    projects_assigned = models.ManyToManyField('Project', blank=True)

    def __str__(self):
        return self.user.username + ' - ' + self.role
    
    def projects_count(self):
        return self.projects_assigned.count()

class Project(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True,default=timezone.now)
    end_date = models.DateField(null=True, blank=True,default=timezone.now)
    status = models.CharField(max_length=20, choices=status_choices,default='pending')
    members = models.ManyToManyField(Profile, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

