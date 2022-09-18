from django.urls import re_path
import file_manager.views

urlpatterns = [
    re_path(r'^upload$', file_manager.views.Upload.as_view())
]
