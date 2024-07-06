from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Donor

@receiver(post_save, sender=User)
def create_donor(sender, instance, created, **kwargs):
    if created:
        Donor.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_donor(sender, instance, **kwargs):
    instance.donor.save()
