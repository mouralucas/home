from django.urls import re_path
from django.views.generic import RedirectView

from finance import views

urlpatterns = [
    # path('dashboard/', include(('finance.financeiro_dashboard.urls', 'finance.financeiro_dashboard'), namespace='dashboard')),

    re_path('^$', views.Home.as_view(), name='home'),
    re_path('^configracoes$', views.Configuracoes.as_view(), name='configuracoes'),

    # Ajax functions
    re_path(r'^contas$', views.BankAccount().as_view(), name='conta'),
    re_path(r'^cartoes$', views.CreditCard().as_view(), name='credit_card'),
    re_path(r'^categorias$', views.Category().as_view(), name='categoria'),
    re_path(r'^fatura$', views.Bill().as_view(), name='fatura'),
    # re_path('^ajax/fatura/evolucao$', views.FaturaEvolucao.as_view(), name='fatura_evolucao'),
    re_path(r'^extrato$', views.Statement().as_view(), name='statement'),
    re_path(r'^ajax/investmento$', views.Investment.as_view(), name='investment'),
    re_path(r'^ajax/fatura/csv', views.Csv.as_view(), name='csv_fatura'),
    re_path(r'^ajax/periodos', views.Periodos.as_view(), name='periods'),
    re_path(r'^ajax/currency', views.Currency.as_view(), name='currency'),
    re_path(r'^ajax/payment/date', views.PaymentDate.as_view(), name='payment_date'),
    re_path(r'^ajax/expenses/fixed', views.FixedExpenses.as_view(), name='fixed_expenses')
]
