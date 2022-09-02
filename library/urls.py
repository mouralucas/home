from django.urls import re_path

# from library import ajax
from library import views

urlpatterns = [
    re_path('^item$', views.Item.as_view(), name='item'),
    re_path('^item/author$', views.ItemAuthor.as_view(), name='item_author'),
    re_path('^author$', views.Author.as_view(), name='author'),
    re_path('^status$', views.Status.as_view(), name='status'),
    re_path('^tipo$', views.Type.as_view(), name='tipo'),
    re_path('^format$', views.Formato.as_view(), name='format'),
    re_path('^serie$', views.Serie.as_view(), name='serie'),
    re_path('^collection$', views.Colecao.as_view(), name='colecao'),
    re_path('^publisher$', views.Publisher.as_view(), name='publisher'),
    re_path('^language$', views.Language.as_view(), name='language'),
]
