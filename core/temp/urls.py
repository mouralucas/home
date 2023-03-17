from django.urls import re_path

import core.temp.views

urlpatterns = [
    re_path('balance', core.temp.views.Balance.as_view()),
]
