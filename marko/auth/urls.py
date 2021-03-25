from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .api import RegisterAPI,LoginAPI, UserAPI
from knox import views as knox_views


urlpatterns = [
    path('api/', include('knox.urls')),
    path('register/', RegisterAPI.as_view(), name='auth_register'),
    path('login/',LoginAPI.as_view(),name='auth_login'),
    path('korisnik', UserAPI.as_view(), name = 'user_api' )
]
