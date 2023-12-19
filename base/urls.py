import rest_framework_simplejwt
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.authentication import JWTAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="Simple Finance",
        default_version='v0.0.1',
        description="Bem vindo a API do Simple Finance",
        # terms_of_service="https://www.jaseci.org",
        contact=openapi.Contact(email="lucaspenha471@gmail.com"),
        # license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
    authentication_classes=[]
    # authentication_classes=[None],
)

urlpatterns = [
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0)),
    re_path(r'^core/', include(('core.urls', 'core'), namespace='core')),
    path('user/', include(('core.user.urls', 'core.user'), namespace='user')),
    path('finance/', include(('finance.urls', 'finance'), namespace='finance')),
    path('library/', include(('library.urls', 'library'), namespace='library')),
    path('file/', include(('file.urls', 'file'), namespace='file')),
]
