from django.urls import re_path
import file.views

urlpatterns = [
    re_path(r'^upload$', file.views.Upload.as_view()),
    re_path(r'^extract$', file.views.Extract.as_view())
]
