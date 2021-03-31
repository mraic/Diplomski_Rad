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
    #path('export_nastava',views.export_raspored_csv,name = 'exportnastava'),
    path('ispricaj_studenta/',views.ispricaj_studenta, name='ispricajstudenta'),

    path('admin/', admin.site.urls),
    path("auth/",include('auth.urls')),

    path('apioverview/',views.apiOverview, name= 'api-overview'),
    ### API ###
    path('osobe-list/', views.osobeList, name = 'osobelist'),
    path('osobe-detail/<str:pk>', views.osobeDetail, name = 'osobedetail'),
    path('osobe-create/', views.osobeCreate, name = 'osobecreate'),
    path('osobe-update/<str:pk>', views.osobeUpdate, name = 'osobeupdate'),

    path('uloge-list/', views.ulogeList, name = 'ulogelist'),
    path('uloge-detail/<int:pk>', views.ulogeDetail, name = 'ulogedetail'),
    path('uloge-create/', views.ulogeCreate, name = 'ulogecreate'),
    path('uloge-update/<int:pk>', views.ulogeUpdate, name = 'ulogeupdate'),

    path('kolegij-list/', views.kolegijiList, name = 'kolegijilist'),
    path('kolegij-detail/<int:pk>', views.kolegijiDetail, name = 'kolegijdetail'),
    path('kolegij-create/', views.kolegijiCreate, name = 'kolegijcreate'),
    path('kolegij-update/<int:pk>', views.kolegijiUpdate, name = 'kolegijiupdate'),

    path('studij-list/', views.studijList, name = 'studijlist'),
    path('studij-detail/<int:pk>', views.studijDetail, name = 'studijkolegij'),
    path('studij-create/', views.studijCreate, name = 'studijcreate'),
    path('studij-update/<int:pk>', views.studijUpdate, name = 'studijupdate'),

    path('ucionica-list/', views.ucionicaList, name = 'ucionicalist'),
    path('ucionica-detail/<int:pk>', views.ucionicaDetail, name = 'ucionicadetail'),
    path('ucionica-create/', views.ucionicaCreate, name = 'ucionicacreate'),
    path('ucionica-update/<int:pk>', views.ucionicaUpdate, name = 'ucionicaupdate'),

    path('termini-list/', views.terminiList, name = 'terminilist'),
    path('termini-detail/<int:pk>', views.terminiDetail, name = 'terminidetail'),
    path('termini-create/', views.terminiCreate, name = 'terminicreate'),
    path('termini-update/<int:pk>', views.terminiUpdate, name = 'terminiupdate'),

    path('evidencija-list/', views.evidencijaList, name = 'evidencijalist'),
    path('evidencija-detail/<int:pk>', views.evidencijaDetail, name = 'evidencijadetail'),
    path('evidencija-create/', views.evidencijaCreate, name = 'evidencijacreate'),
    path('evidencija-update/<int:pk>', views.evidencijaUpdate, name = 'evidencijaupdate'),




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