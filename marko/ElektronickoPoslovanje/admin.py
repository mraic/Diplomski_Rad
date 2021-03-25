from .models import osobe,uloga,kolegiji,studij,ucionica,termini,evidencija
from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin


@admin.register(osobe)
class osobeAdmin(admin.ModelAdmin):
    list_display = ('username','email')

@admin.register(uloga)
class ulogaAdmin(admin.ModelAdmin):
    list_display=('naziv','datum_dodjele')

@admin.register(kolegiji)
class kolegijiAdmin(admin.ModelAdmin):
    list_display = ('naziv_kolegija','akademska_godina')

@admin.register(studij)
class studijAdmin(admin.ModelAdmin):
    list_display = ('naziv_studija','godina_studija')

@admin.register(termini)
class terminiAdmin(admin.ModelAdmin):
    list_display = ('naziv_kolegija','datum', 'vrijeme_pocetka','zavrsetak','trajanje')

@admin.register(ucionica)
class ucionicaAdmin(admin.ModelAdmin):
    list_display = ('broj_ucionice','broj_mjesta','kat','slobodna_ucionica')

@admin.register(evidencija)
class evidencijaAdmin(admin.ModelAdmin):
    list_display=('predavanja_fk','osoba_fk',)

    
