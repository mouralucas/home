from django.urls import re_path, include

import core.views

urlpatterns = [
    re_path(r'^temp/', include('core.temp.urls')),

    re_path(r'^module$', core.views.Module.as_view(), name='module'),
    re_path(r'^category$', core.views.Category.as_view(), name='category'),

    # Country related views
    re_path(r'^country$', core.views.Country.as_view(), name='country'),
    re_path(r'^country/states', core.views.State.as_view(), name='country_state'),
]
