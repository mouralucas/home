from django.urls import re_path
from django.views.generic import RedirectView

from finance import views

urlpatterns = [
    re_path(r'^account$', views.BankAccount().as_view(), name='bank_account'),
    re_path(r'^card$', views.CreditCard().as_view(), name='credit_card'),
    re_path(r'^bill$', views.Bill().as_view(), name='fatura'),

    re_path(r'^statement$', views.Statement().as_view(), name='statement'),
    re_path(r'^investmento$', views.Investment.as_view(), name='investment'),
    re_path(r'^fatura/csv$', views.Csv.as_view(), name='csv_fatura'),
    re_path(r'^periodos$', views.Periodos.as_view(), name='periods'),
    re_path(r'^currency$', views.Currency.as_view(), name='currency'),
    re_path(r'^payment/date$', views.PaymentDate.as_view(), name='payment_date'),
    re_path(r'^expenses/fixed$', views.FixedExpenses.as_view(), name='fixed_expenses'),
    re_path(r'^expenses/variable$', views.VariableExpenses.as_view(), name='variable_variable'),
    re_path(r'^expenses/evolution$', views.ExpensesEvolution.as_view(), name='evolution_expenses'),
]
