from django.urls import path, re_path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

FINANCE_SWAGGER_SETTINGS = {
    'TITLE': 'Finance Module',
    'DESCRIPTION': 'This page describes all finance URLs',
    'VERSION': '0.0.1'
}

LIBRARY_SWAGGER_SETTINGS = {
    'TITLE': 'Library App',
    'DESCRIPTION': 'This page describes all library URLs',
    'VERSION': '0.0.1'
}

urlpatterns = [
    # Swagger/Schemas URL
    re_path(r'^schema/$', SpectacularAPIView.as_view(), name='schema'),
    re_path("^$", SpectacularSwaggerView.as_view(template_name='swagger-ui.html', url_name='schema'), name='swagger-ui'),

    re_path(r'schema/core$', SpectacularAPIView.as_view(urlconf='core.urls', custom_settings=LIBRARY_SWAGGER_SETTINGS), name='schema-core'),
    re_path(r'^core$', SpectacularSwaggerView.as_view(url_name='schema-core', template_name='swagger-ui.html'), name='swagger-ui-core'),

    re_path(r'schema/user$', SpectacularAPIView.as_view(urlconf='core.user.urls', custom_settings=LIBRARY_SWAGGER_SETTINGS), name='schema-user'),
    re_path(r'^user$', SpectacularSwaggerView.as_view(url_name='schema-user', template_name='swagger-ui.html'), name='swagger-ui-user'),

    re_path(r'^schema/finance$', SpectacularAPIView.as_view(urlconf='finance.urls', custom_settings=FINANCE_SWAGGER_SETTINGS), name='schema-finance'),
    re_path(r'^finance$', SpectacularSwaggerView.as_view(url_name='schema-finance', template_name='swagger-ui.html'), name='swagger-ui-finance'),

    re_path(r'schema/library$', SpectacularAPIView.as_view(urlconf='library.urls', custom_settings=LIBRARY_SWAGGER_SETTINGS), name='schema-library'),
    re_path(r'^library$', SpectacularSwaggerView.as_view(url_name='schema-library', template_name='swagger-ui.html'), name='swagger-ui-library'),

    # Project APPs URLs
    re_path(r'^core/', include(('core.urls', 'core'), namespace='core')),
    re_path(r'^user/', include(('core.user.urls', 'core.user'), namespace='user')),
    re_path(r'^finance/', include(('finance.urls', 'finance'), namespace='finance')),
    re_path(r'^library/', include(('library.urls', 'library'), namespace='library')),
    re_path(r'^file/', include(('file.urls', 'file'), namespace='file')),

]
