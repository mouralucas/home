from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

import core.user.views

urlpatterns = [
    re_path(r'^login$', csrf_exempt(core.user.views.Login.as_view()), name='login'),
    re_path(r'^login/refresh$', csrf_exempt(core.user.views.Refresh.as_view()), name='login'),
    re_path(r'^account$', csrf_exempt(core.user.views.Account.as_view()), name='create'),

    # URL to test login module
    re_path(r'test/login/no-auth', core.user.views.TestViewWithoutAuth.as_view()),
    re_path(r'test/login/auth', core.user.views.TestViewWithoutAuth.as_view())
]
