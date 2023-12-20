from django.urls import path, re_path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    re_path("^$", SpectacularSwaggerView.as_view(template_name="swagger-ui.html", url_name='schema'), name="swagger-ui",),

    re_path(r'^core/', include(('core.urls', 'core'), namespace='core')),
    path('user/', include(('core.user.urls', 'core.user'), namespace='user')),
    path('finance/', include(('finance.urls', 'finance'), namespace='finance')),
    path('library/', include(('library.urls', 'library'), namespace='library')),
    path('file/', include(('file.urls', 'file'), namespace='file')),
]
