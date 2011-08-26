from django.views.generic import TemplateView

class HomepageView(TemplateView):
    template_name = 'core/homepage.html'


class CompareView(TemplateView):
    template_name = 'core/compare.html'

