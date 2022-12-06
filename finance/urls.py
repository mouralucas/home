from django.urls import re_path
from django.views.generic import RedirectView

from finance import views

urlpatterns = [
    # Account urls
    re_path(r'^account$', views.BankAccount().as_view()),
    re_path(r'^statement$', views.BankStatement().as_view()),

    # Credit card urls
    re_path(r'^card$', views.CreditCard().as_view()),
    re_path(r'^bill$', views.CreditCardBill.as_view()),
    re_path(r'bill/history', views.BillHistory.as_view()),
    re_path(r'^fatura/csv$', views.Csv.as_view()),  # TODO: remove

    # Investment urls
    re_path(r'^investment$', views.Investment.as_view()),
    re_path(r'^investment/statement/upload$', views.InvestmentStatementUpload.as_view()),

    # Other
    re_path(r'^currency$', views.Currency.as_view()),

    re_path(r'^upload/pdf', views.PdfImport.as_view()),

    re_path(r'^expenses', views.Expense.as_view()),

    re_path(r'^expenses/history$', views.ExpensesHistory.as_view()),
    re_path(r'^payment/date$', views.PaymentDate.as_view()),
]
