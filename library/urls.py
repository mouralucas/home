from django.urls import re_path

# from library import ajax
from library import views

urlpatterns = [
    re_path('^item$', views.Item.as_view(), name='item'),
    re_path('^item/author$', views.ItemAuthor.as_view(), name='item_author'),
    re_path('^author$', views.Author.as_view(), name='author'),
    re_path('^status$', views.Status.as_view(), name='status'),
    re_path('^type$', views.Type.as_view()),
    re_path('^format$', views.Format.as_view()),
    re_path('^serie$', views.Serie.as_view()),
    re_path('^collection$', views.Collection.as_view()),
    re_path('^publisher$', views.Publisher.as_view()),
    re_path('^language$', views.Language.as_view(), name='language'),
]
