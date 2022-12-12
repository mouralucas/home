from django.urls import re_path

import core.temp.views

urlpatterns = [
    re_path('bill', core.temp.views.MigrateFaturaToBill.as_view()),
]
