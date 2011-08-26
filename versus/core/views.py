from django.db.models import F
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from foursquare.models import Visit

class HomepageView(TemplateView):
    template_name = 'core/homepage.html'


class CompareView(TemplateView):
    template_name = 'core/compare.html'

    def get_context_data(self):
        venue_a, venue_b = self.request.user.get_profile().venue_pair()
        return {
            'venue_a': venue_a,
            'venue_b': venue_b,
        }

    def post(self, request, **kwargs):
        winning_visit = Visit.objects.filter(
            profile=request.user.get_profile(),
            venue=request.POST.get('winner'),
        )
        winning_visit.update(
            score=F('score')+1,
            ranked=True,
        )

        losing_visit = Visit.objects.filter(
            profile=request.user.get_profile(),
            venue=request.POST.get('loser'),
        )
        losing_visit.update(
            score=F('score')-1,
            ranked=True,
        )

        #TODO Record that the user has made a judgement on this pair

        return HttpResponseRedirect(reverse('compare'))

