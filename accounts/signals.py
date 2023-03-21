from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def user_create(sender, **kwargs):
    user = kwargs['instance']
    if kwargs['created']:
        Profile.objects.create(
            email=user.email,
            profUser=user,
        )
