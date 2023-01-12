from django.urls import re_path

import core.temp.views

urlpatterns = [
    re_path('update', core.temp.views.UpdateDateTime.as_view()),
]
