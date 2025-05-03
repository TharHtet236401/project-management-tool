from django.contrib.auth.models import User
from django.db import models

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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.name
    

