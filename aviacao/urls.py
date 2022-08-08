from django.urls import re_path, path, include
from django.views.generic import RedirectView
from aviacao import views

urlpatterns = [
    # path('dashboard/', include(('finance.financeiro_dashboard.urls', 'finance.financeiro_dashboard'), namespace='dashboard')),

    re_path(r'^home$', views.Home.as_view(), name='home'),
    re_path('^import/voo/csv$', views.ImportVooCsv.as_view(), name='impot_voo_csv'),
    re_path(r'^tamanho/csv', views.TamanhoCSV.as_view(), name='tamanho_csv'),
    re_path('^geral$', views.Geral.as_view(), name='impot_voo_csv'),
    re_path(r'^import/aeroporto/csv/(?P<file>[-:\w]+)$', views.ImportAeroportoCsv.as_view(), name='impot_aeroporto_csv'),
]
