from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from auth import get_authenticator
import pysq.apiv2 as psq

class UserProfile(models.Model):
    """
    User profile model which stores extra data specific to a Foursquare user.
    """
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=128)

    def display_name(self):
        """
        Returns the user's name, in the same style Foursquare uses.
        """
        return "%s %s." % (self.user.first_name, self.user.last_name[0])

    def foursquare_user(self):
        """
        Returns a pysq.apiv2.User instance for this user.
        """
        authenticator = get_authenticator(self.access_token)
        finder = psq.UserFinder(authenticator)
        return finder.findUser('self')

    def checkins(self):
        """
        Returns all checkins for this user.
        """
        return self.foursquare_user().all_checkins()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

