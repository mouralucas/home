from django.urls import re_path

# from library import ajax
from library.views import views_deprecated, item

urlpatterns = [
    # Items
    re_path('^item$', item.Item.as_view(), name='item'),
    re_path('^item/author$', views_deprecated.ItemAuthor.as_view(), name='item_author'),
    re_path('^item/reading$', views_deprecated.ItemReading.as_view()),

    # Others
    re_path('^author$', views_deprecated.Author.as_view(), name='author'),
    re_path('^status$', views_deprecated.Status.as_view(), name='status'),
    re_path('^type$', views_deprecated.Type.as_view()),
    re_path('^format$', views_deprecated.Format.as_view()),
    re_path('^serie$', views_deprecated.Serie.as_view()),
    re_path('^collection$', views_deprecated.Collection.as_view()),
    re_path('^publisher$', views_deprecated.Publisher.as_view()),
    re_path('^language$', views_deprecated.Language.as_view(), name='language'),
]
