from django.urls import re_path
from django.views.generic import RedirectView

from finance import views
from finance import views_investment
from finance import views_account
from finance import views_credit_card

urlpatterns = [
    # Account
    re_path(r'^account$', views_account.Account().as_view()),
    re_path(r'^account/statement$', views.AccountStatement().as_view()),

    # Credit card
    re_path(r'^credit-card$', views_credit_card.CreditCard().as_view()),
    re_path(r'^credit-card/bill$', views.CreditCardBill.as_view()),
    re_path(r'^credit-card/bill/history$', views.BillHistory.as_view()),

    # Investment
    re_path(r'^investment$', views_investment.Investment.as_view()),
    re_path(r'^investment/type$', views_investment.InvestmentType.as_view()),
    re_path(r'^investment/proportion$', views_investment.Proportion.as_view()),
    re_path(r'^investment/statement$', views.InvestmentStatement.as_view()),
    re_path(r'^investment/statement/upload$', views.InvestmentStatementUpload.as_view()),

    # Dashboard
    re_path(r'summary', views.Summary.as_view()),

    # Other
    re_path(r'^currency$', views.Currency.as_view()),
    re_path(r'^bank$', views.Bank.as_view()),

    re_path(r'^upload/pdf', views.PdfImport.as_view()),

    re_path(r'^expense$', views.Expense.as_view()),
    re_path(r'^expense/category$', views.ExpenseCategory.as_view()),
    re_path(r'^expenses/history$', views.ExpensesHistory.as_view()),
    re_path(r'^payment/date$', views.PaymentDate.as_view()),

    # File content uploads for some banks
    re_path('file/upload/excel/pagbank', views.ImportExcelPagBank.as_view())
]
