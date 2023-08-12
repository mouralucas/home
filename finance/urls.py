from django.urls import re_path

from finance import views
from finance.views import account, credit_card, investment, views_deprecated, integration

urlpatterns = [
    # Account
    re_path(r'^account$', account.Account().as_view()),
    re_path(r'^account/statement$', account.AccountStatement().as_view()),

    # Credit card
    re_path(r'^credit-card$', credit_card.CreditCard().as_view()),
    re_path(r'^credit-card/bill$', credit_card.CreditCardBill.as_view()),
    re_path(r'^credit-card/bill/history$', views_deprecated.BillHistory.as_view()),

    # Investment
    re_path(r'^investment$', investment.Investment.as_view()),
    re_path(r'^investment/type$', investment.InvestmentType.as_view()),
    re_path(r'^investment/proportion$', investment.Proportion.as_view()),
    re_path(r'^investment/statement$', views_deprecated.InvestmentStatement.as_view()),
    re_path(r'^investment/statement/upload$', views_deprecated.InvestmentStatementUpload.as_view()),

    # Dashboard
    re_path(r'summary', views_deprecated.Summary.as_view()),

    # Other
    re_path(r'^currency$', views_deprecated.Currency.as_view()),
    re_path(r'^bank$', views_deprecated.Bank.as_view()),

    re_path(r'^upload/pdf', views_deprecated.PdfImport.as_view()),

    re_path(r'^expense$', views_deprecated.Expense.as_view()),
    re_path(r'^expense/category$', views_deprecated.ExpenseCategory.as_view()),
    re_path(r'^expenses/history$', views_deprecated.ExpensesHistory.as_view()),
    re_path(r'^payment/date$', views_deprecated.PaymentDate.as_view()),

    re_path(r'^interest$', investment.Interest.as_view()),

    # Integration
    re_path('integration/historical', integration.Historical.as_view()),

    # File content uploads for some banks
    re_path('file/upload/excel/pagbank', views_deprecated.ImportExcelPagBank.as_view())
]
