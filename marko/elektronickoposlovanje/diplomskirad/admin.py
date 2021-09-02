from .models import osobe,uloga,kolegiji,studij, termini, ucionica, evidencija
from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.shortcuts import render
from django import forms

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


class CSVImportForm(forms.Form):
    csv_upload = forms.FileField()

@admin.register(evidencija)
class evidencijaAdmin(admin.ModelAdmin):
    list_display=('predavanja_fk','osoba_fk',)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('csv_upload/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):

        form = CSVImportForm()
        data = {"form":form}
        return render(request, "admin/csv_upload.csv", data)
