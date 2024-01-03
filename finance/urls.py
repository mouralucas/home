from django.urls import re_path

from finance.views import account, credit_card, investment, views_deprecated, integration, core, pos


urlpatterns = [
    # Account
    re_path(r'^account$', account.Account().as_view()),
    re_path(r'^account/statement$', account.Statement().as_view()),
    re_path(r'balance', account.Balance.as_view()),

    # Credit card
    re_path(r'^credit-card$', credit_card.CreditCard().as_view()),
    re_path(r'^credit-card/bill$', credit_card.CreditCardBill.as_view()),
    # re_path(r'^credit-card/bill/history/aggregated$', credit_card.BillHistoryAggregated.as_view()),
    re_path(r'^credit-card/bill/history$', credit_card.BillHistory.as_view()),

    # Investment
    re_path(r'^investment$', investment.Investment.as_view()),
    re_path(r'^investment/type$', investment.Type.as_view()),
    re_path(r'^investment/allocation$', investment.Allocation.as_view()),
    re_path(r'^investment/statement$', investment.Statement.as_view()),
    re_path(r'^investment/statement/upload$', views_deprecated.InvestmentStatementUpload.as_view()),
    re_path(r'^investment/profit', investment.Profit.as_view()),

    # Point os Sales (PagSeguro)
    re_path(r'^pos/import/pag-seguro', pos.PagSeguroStatement.as_view()),

    # Dashboard
    re_path(r'summary', core.Summary.as_view()),

    # Other
    re_path(r'^currency$', core.Currency.as_view()),
    re_path(r'^cash-flow$', core.CashFlow.as_view()),
    re_path(r'^bank$', core.Bank.as_view()),

    re_path(r'^upload/pdf', views_deprecated.PdfImport.as_view()),

    re_path(r'^transaction/category/list$', core.TransactionByCategoryList.as_view()),
    re_path(r'^transaction/category/aggregated$', core.TransactionsByCategoryAggregated.as_view()),
    # re_path(r'^expenses/history$', views_deprecated.ExpensesHistory.as_view()),
    re_path(r'^payment/date$', views_deprecated.PaymentDate.as_view()),

    re_path(r'^interest$', investment.Interest.as_view()),
    re_path(r'^interest/accumulated$', investment.InterestAccumulated.as_view()),

    # Integration
    re_path('integration/historical', integration.Historical.as_view()),

    # File content uploads for some banks
    re_path('file/upload/excel/pagbank', views_deprecated.ImportExcelPagBank.as_view())
]
