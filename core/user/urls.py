from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

import core.user.views

urlpatterns = [
    re_path(r'^login$', csrf_exempt(core.user.views.Login.as_view()), name='login'),
    re_path(r'^account$', csrf_exempt(core.user.views.Account.as_view()), name='create'),
]
