from django.urls import re_path, include

import core.integration.views as views

urlpatterns = [
    re_path(r'^rate$', views.CurrencyRate.as_view())
]
