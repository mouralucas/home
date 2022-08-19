from django.urls import re_path

import core.temp.views

urlpatterns = [
    re_path('bill', core.temp.views.MigrateFaturaToBill.as_view()),
    re_path('statement', core.temp.views.MigrateExtratoToStatement.as_view()),
    re_path('author', core.temp.views.MigrateAutorToAuthor.as_view()),
]