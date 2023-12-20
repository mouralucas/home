from django.urls import path, re_path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.views import Swagger, SwaggerSchema

urlpatterns = [
    path("schema/", SwaggerSchema.as_view(), name="schema"),
    path("docs/", Swagger.as_view(template_name="swagger-ui.html", url_name='schema'), name="swagger-ui",),

    re_path(r'^core/', include(('core.urls', 'core'), namespace='core')),
    path('user/', include(('core.user.urls', 'core.user'), namespace='user')),
    path('finance/', include(('finance.urls', 'finance'), namespace='finance')),
    path('library/', include(('library.urls', 'library'), namespace='library')),
    path('file/', include(('file.urls', 'file'), namespace='file')),
]
