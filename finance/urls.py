from django.urls import re_path
from django.views.generic import RedirectView

from finance import views
from finance import ajax

urlpatterns = [
    # path('dashboard/', include(('finance.financeiro_dashboard.urls', 'finance.financeiro_dashboard'), namespace='dashboard')),

    re_path('^$', views.Home.as_view(), name='home'),
    re_path('^configracoes$', views.Configuracoes.as_view(), name='configuracoes'),

    # Ajax functions
    re_path(r'^account$', ajax.BankAccount().as_view(), name='bank_account'),
    re_path(r'^card$', ajax.CreditCard().as_view(), name='credit_card'),
    # re_path(r'^category$', ajax.Category().as_view(), name='category'),
    re_path(r'^fatura$', ajax.Bill().as_view(), name='fatura'),

    re_path(r'^extrato$', ajax.Statement().as_view(), name='statement'),
    re_path(r'^ajax/investmento$', ajax.Investment.as_view(), name='investment'),
    re_path(r'^ajax/fatura/csv$', ajax.Csv.as_view(), name='csv_fatura'),
    re_path(r'^ajax/periodos$', ajax.Periodos.as_view(), name='periods'),
    re_path(r'^ajax/currency$', ajax.Currency.as_view(), name='currency'),
    re_path(r'^ajax/payment/date$', ajax.PaymentDate.as_view(), name='payment_date'),
    re_path(r'^ajax/expenses/fixed$', ajax.FixedExpenses.as_view(), name='fixed_expenses'),
    re_path(r'^ajax/expenses/evolution$', ajax.ExpensesEvolution.as_view(), name='evolution_expenses'),
]
