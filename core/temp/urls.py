from django.urls import re_path

import core.temp.views

urlpatterns = [
    re_path('bill', core.temp.views.MigrateFaturaToBill.as_view()),
    re_path('statement', core.temp.views.MigrateExtratoToStatement.as_view()),
    re_path('author', core.temp.views.MigrateAutorToAuthor.as_view()),
    re_path('collection', core.temp.views.MigrateColecaoToCollectiontem.as_view()),
    re_path('publisher', core.temp.views.MigrateEdtoraToPublisher.as_view()),
    re_path('serie', core.temp.views.MigrateSerieToSerie.as_view()),
    re_path(r'^item$', core.temp.views.MigrateLivroToItem.as_view()),
    re_path(r'^item/autor$', core.temp.views.MigrateLivroAutorToItemAuthor.as_view()),
    re_path(r'^item/status$', core.temp.views.MigrateLivroLogStatusrToItemLogStatus.as_view()),
]
