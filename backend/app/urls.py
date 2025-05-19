from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

from app.views.custom_token_obtain_pair import CustomTokenObtainPairView
from app.views.user_info import UserInfoView

index_redirect = [path('', RedirectView.as_view(url=settings.FRONTEND_URL))]
index_template = [path('', TemplateView.as_view(template_name='index.html'))]
index_url = index_redirect if settings.ENV == 'development' else index_template

urlpatterns = index_url + [
    path('admin/', admin.site.urls),

    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include('apps.urls')),

    path('api/user_info/', UserInfoView.as_view(), name='user_info'),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),

        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]
