from django.urls import re_path
from django.views.generic import RedirectView

from finance import views

urlpatterns = [
    re_path(r'^account$', views.BankAccount().as_view(), name='bank_account'),
    re_path(r'^card$', views.CreditCard().as_view(), name='credit_card'),
    re_path(r'^bill$', views.CreditCardBill.as_view(), name='fatura'),
    re_path(r'bill/history', views.BillHistory.as_view()),

    re_path(r'^statement$', views.BankStatement().as_view(), name='statement'),
    re_path(r'^investmento$', views.Investment.as_view(), name='investment'),
    re_path(r'^fatura/csv$', views.Csv.as_view(), name='csv_fatura'),
    re_path(r'^currency$', views.Currency.as_view(), name='currency'),

    re_path(r'^upload/pdf', views.PdfImport.as_view()),

    re_path(r'^expenses', views.Expense.as_view()),

    re_path(r'^expenses/history$', views.ExpensesHistory.as_view()),
    re_path(r'^payment/date$', views.PaymentDate.as_view(), name='payment_date'),
]
