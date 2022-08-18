from django.urls import re_path, include

import core.ajax

urlpatterns = [
    re_path(r'^temp/', include('core.temp.urls')),

    re_path(r'^ajax/module$', core.ajax.Module.as_view(), name='module'),
    re_path(r'^ajax/category$', core.ajax.Category.as_view(), name='category'),

    # Country related views
    re_path(r'^ajax/country$', core.ajax.Country.as_view(), name='country'),
    re_path(r'^ajax/country/states', core.ajax.State.as_view(), name='country_state'),
]
