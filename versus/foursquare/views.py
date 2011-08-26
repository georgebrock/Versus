from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib import auth
from django.core.urlresolvers import reverse
from auth import get_authenticator

class StartAuthView(View):
    """
    Responsible for the first part of the OAuth dance: redirects the
    user to Foursquare so that they can authorise versus.
    """
    def get(self, request):
        auth = get_authenticator()
        uri = auth.authorize_uri()
        return HttpResponseRedirect(uri)


class CompleteAuthView(View):
    """
    Responsible for the final part of the OAuth dance: takes the temporary
    token from Foursquare and uses it to get an access token.
    """
    def get(self, request):
        try:
            auth_code = request.GET['code']
        except KeyError:
            return HttpResponseBadRequest(content='Bad request; no auth code')

        user = auth.authenticate(auth_code=auth_code)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('compare'))
        else:
            return HttpResponseBadRequest(content='Bad request; no such user')

