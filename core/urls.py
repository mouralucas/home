from django.urls import re_path, include
import core.ajax


urlpatterns = [
    re_path(r'^temp/', include('core.temp.urls')),

    re_path(r'^ajax/country$', core.ajax.Country.as_view(), name='country')
]