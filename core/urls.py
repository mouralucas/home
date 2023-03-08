from django.urls import re_path, include

import core.views

urlpatterns = [
    re_path(r'^temp/', include('core.temp.urls')),

    re_path(r'^module$', core.views.Module.as_view()),
    re_path(r'^category$', core.views.Category.as_view()),
    re_path(r'^status$', core.views.Status.as_view()),
    re_path(r'^period', core.views.Period.as_view()),

    # Country related views
    re_path(r'^country$', core.views.Country.as_view(), name='country'),
    re_path(r'^country/states', core.views.State.as_view(), name='country_state'),

    re_path(r'^integration/', include(('core.integration.urls', 'core.integration'), namespace='core')),
]
