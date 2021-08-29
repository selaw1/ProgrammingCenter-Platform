from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, UserBase

# We want a user profile created for each new user

# We have a signal of (post_save) so...
# When a user is saved we send a signal which will be received by the (receiver = the create_profile function)
@receiver(post_save, sender=UserBase)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Just saves the profile each time the user object gets saved
@receiver(post_save, sender=UserBase)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

