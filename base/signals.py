from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Project

print("base.signals imported")

@receiver(post_save, sender=Project)
def update_project_cache(sender, instance, created, **kwargs):
    from django.core.cache import cache
    cache_key = 'recent_projects'
    recent_projects = list(Project.objects.order_by('-id')[:5])
    print("cached cleared final check")
    cache.set(cache_key, recent_projects, timeout=300)

@receiver(pre_delete, sender=Project)
def delete_project_cache(sender, instance, **kwargs):
    from django.core.cache import cache
    cache_key = 'recent_projects'
    cache.delete(cache_key)

