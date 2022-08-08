from django.urls import re_path
import core.ajax


urlpatterns = [
    re_path(r'^ajax/country$', core.ajax.Country.as_view(), name='country')
]