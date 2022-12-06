from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # re_path(r'^$', RedirectView.as_view(url='finance/')),
    re_path(r'^core/', include(('core.urls', 'core'), namespace='core')),
    path('user/', include(('core.user.urls', 'core.user'), namespace='user')),
    path('finance/', include(('finance.urls', 'finance'), namespace='finance')),
    path('library/', include(('library.urls', 'library'), namespace='library')),
    path('file/', include(('file.urls', 'file'), namespace='file')),
]
