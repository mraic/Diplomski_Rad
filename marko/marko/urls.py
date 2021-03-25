from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


from ElektronickoPoslovanje import views

urlpatterns = [
    path('', views.login_view,name='home'),
    path('register/', views.register_view, name= 'register'),
    path('user/', views.user, name='user'),
    path('predmeti/<int:pk>/', views.predmeti_view, name='predmeti'),
    path('nadzornaploca/', views.nadzornaPlocaView, name = 'nadzornaploca'),
    path('logout/',views.logout_view, name = 'logout'),
    path('export/', views.export, name='export'),


    path('apioverview',views.apiOverview, name= 'api-overview'),


    path('admin/', admin.site.urls),
    path("auth/",include('auth.urls')),

    ### Lozinka ###
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='lozinka/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='lozinka/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='lozinka/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'lozinka/password_reset.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='lozinka/password_reset_complete.html'),
     name='password_reset_complete'),


]