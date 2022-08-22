from django.urls import re_path

from library import ajax
from library import views

urlpatterns = [
    re_path('^$', views.LandingPage.as_view(), name='home'),
    re_path('^settings$', views.Settings.as_view(), name='settings'),
    
    
    re_path('^ajax/item$', ajax.Item.as_view(), name='item'),
    re_path('^ajax/item/teste$', ajax.ItemTeste.as_view(), name='item'),
    re_path('^ajax/item/author$', ajax.ItemAuthor.as_view(), name='item_author'),
    # re_path('^ajax/book$', ajax.Book.as_view(), name='book'),
    # re_path('^ajax/manga$', ajax.Manga.as_view(), name='manga'),
    re_path('^ajax/author$', ajax.Author.as_view(), name='author'),
    re_path('^ajax/status$', ajax.Status.as_view(), name='status'),
    re_path('^ajax/tipo$', ajax.Type.as_view(), name='tipo'),
    re_path('^ajax/format$', ajax.Formato.as_view(), name='format'),
    re_path('^ajax/serie$', ajax.Serie.as_view(), name='serie'),
    re_path('^ajax/collection$', ajax.Colecao.as_view(), name='colecao'),
    re_path('^ajax/editora$', ajax.Publisher.as_view(), name='publisher'),
    re_path('^ajax/language$', ajax.Language.as_view(), name='language'),
    # re_path('^ajax/country$', ajax.Country.as_view(), name='country'),
    # re_path('^ajax/categorias$', ajax.Categoria().as_view(), name='categorias'),
    # re_path('^ajax/fatura$', ajax.Fatura().as_view(), name='faturas'),
    # re_path('^ajax/extrato$', ajax.Extrato().as_view(), name='extrato'),
]
