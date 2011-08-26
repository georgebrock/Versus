from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    """
    User profile model which stores extra data specific to a Foursquare user.
    """
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=128)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

