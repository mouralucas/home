from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View


class LandingPage(View):
    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        return render(self.request, template_name='library/landingpage.html')


class Settings(View):
    def get(self, *args, **kwargs):

        return render(self.request, template_name='library/settings.html')
