from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Role, Job, JobStep, ProcessStepTemplate
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role=Role.ADMIN if instance.is_superuser else Role.STAFF)
@receiver(post_save, sender=Job)
def create_job_steps(sender, instance, created, **kwargs):
    if created and instance.process_type:
        for t in ProcessStepTemplate.objects.filter(process_type=instance.process_type).order_by('order'):
            JobStep.objects.create(job=instance, name=t.name)
