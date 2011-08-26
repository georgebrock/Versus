from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import pysq.apiv2 as psq
import settings

def get_authenticator():
    """
    Returns a pysq.apiv2.FSAuthenticator object that can be used to make
    authenticated queries to the Foursquare API.
    """
    return psq.FSAuthenticator(
        settings.FOURSQUARE_CLIENT_ID,
        settings.FOURSQUARE_SECRET,
        '%s%s' % (
            settings.PROJECT_URL,
            reverse('login-complete'),
        )
    )


class Backend(object):
    """
    An authenitcation backend that uses Foursquare authentication.
    The only login credential required is a Foursquare authorisation code.
    """
    def authenticate(self, auth_code=None):
        authenticator = get_authenticator()
        authenticator.set_token(auth_code)

        foursquare_user = psq.UserFinder(authenticator).findUser('self')
        username = 'foursquare:%s' % foursquare_user.id()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username)
            user.set_unusable_password()

        # Update the user's settings so they stay in sync with Foursquare
        user.email = foursquare_user.email()
        user.first_name = foursquare_user.first_name()
        user.last_name = foursquare_user.last_name()
        user.save()

        # Stash the access token on the user's profile
        profile = user.get_profile()
        profile.access_token = authenticator.access_token
        profile.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

