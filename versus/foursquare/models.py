from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from auth import get_authenticator
import pysq.apiv2 as psq
import itertools
import random

class UserProfile(models.Model):
    """
    User profile model which stores extra data specific to a Foursquare user.
    """
    user = models.OneToOneField(User)
    access_token = models.CharField(max_length=128)
    last_checkin_update = models.IntegerField(null=True)

    visited_venues = models.ManyToManyField('Venue', through='Visit')

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

    def update_visited_venues(self):
        """
        Uses the user's current checkins to create venue and visit objects.
        """

        # On the initial update we get all of the user's checkins.
        # After that we only want the new ones.
        if self.last_checkin_update:
            foursquare_checkins = self.foursquare_user().get_checkins({
                'afterTimestamp': self.last_checkin_update,
            })
        else:
            foursquare_checkins = self.foursquare_user().all_checkins()

        # Keep track of the most recent checkin we have.
        self.last_checkin_update = foursquare_checkins[0].createdAt()
        self.save()

        # Create venues (as required) and checkins in our DB so we don't
        # need to hit the API in future.
        for foursquare_checkin in foursquare_checkins:
            foursquare_venue = foursquare_checkin.venue()
            try:
                venue = Venue.objects.get(fsq_id=foursquare_venue.id())
            except Venue.DoesNotExist:
                venue = Venue.objects.create(
                    fsq_id=foursquare_venue.id(),
                    name=foursquare_venue.name(),
                    city=foursquare_venue.data.get('location',{}).get('city',''),
                )
                venue.save()

            try:
                visit = Visit.objects.get(
                    profile=self,
                    venue=venue,
                )
            except Visit.DoesNotExist:
                visit = Visit.objects.create(
                    profile=self,
                    venue=venue,
                )
                visit.save()

    def venue_pair(self):
        """
        Returns a pair of venues that the user has visited.
        """
        #TODO: Limit to pairs that the user has not already seen
        #TODO: Prefer venues that the user hasn't seen at all
        venues = self.visited_venues.all()
        pairs = itertools.permutations(venues, 2)
        return random.choice(list(pairs))

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Venue(models.Model):
    fsq_id = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=32)

    visitors = models.ManyToManyField(UserProfile, through='Visit')

    def __unicode__(self):
        return self.name


class Visit(models.Model):
    profile = models.ForeignKey(UserProfile)
    venue = models.ForeignKey(Venue)
    score = models.IntegerField(default=0)
    ranked = models.BooleanField(default=False)

