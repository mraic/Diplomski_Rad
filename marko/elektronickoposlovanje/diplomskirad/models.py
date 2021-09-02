
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime, timedelta, time




class uloga(models.Model):
    naziv = models.CharField(max_length=15,null=False)
    datum_dodjele = models.TimeField(auto_now_add=True,null=False)

    def __str__(self):
        return self.naziv

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, broj_indeksa, password,  **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        

        return self.create_user(email, broj_indeksa, password, **other_fields)

    def create_user(self, email,broj_indeksa, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', False)
        other_fields.setdefault('is_active', True)

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, broj_indeksa=broj_indeksa, **other_fields)
        
        user.set_password(password)
        user.save()
        
        return user


class osobe(AbstractBaseUser, PermissionsMixin):
    broj_indeksa = models.CharField(
        max_length=50, unique=True, null=False)
    username = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=256)
    ime = models.CharField(max_length=15, null=False)
    prezime = models.CharField(max_length=15, null=False)
    email = models.EmailField(max_length=50, null=False, unique=True)
    ulogaFK = models.ForeignKey(uloga,on_delete=models.CASCADE,default=2)
    datum_kreiranja = models.DateField(auto_now_add=True, null=False)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['broj_indeksa', 'username', ]

    objects = CustomAccountManager()

    def __str__(self):
        return self.broj_indeksa
    
    def __str__(self):
        return self.email


class kolegiji(models.Model):
    prvaGodina = '1. godina'
    drugaGodina = '2. godina'
    trecaGodina = '3. godina'
    cetvrtaGodina = '4. godina'
    petaGodina = '5. godina'

    akademska_godina_choices = [
        (prvaGodina, '1. godina'),
        (drugaGodina, '2. godina'),
        (trecaGodina, '3. godina'),
        (cetvrtaGodina, '4. godina'),
        (petaGodina, '5. godina'),
    ]
    naziv_kolegija = models.CharField(max_length=40,null=False)
    akademska_godina = models.CharField(max_length=9,null=False,choices=akademska_godina_choices,default=prvaGodina)
    osobeFK = models.ForeignKey(osobe,max_length=15,null=False,on_delete=models.CASCADE)

    def __str__(self):
        return self.naziv_kolegija

class studij(models.Model):
    prvaGodina = '1. godina'
    drugaGodina = '2. godina'
    trecaGodina = '3. godina'
    cetvrtaGodina = '4. godina'
    petaGodina = '5. godina'

    godina_studija_choices = [
        (prvaGodina, '1. godina'),
        (drugaGodina, '2. godina'),
        (trecaGodina, '3. godina'),
        (cetvrtaGodina, '4. godina'),
        (petaGodina, '5. godina'),
    ]
    naziv_studija = models.CharField(max_length=40, null=False)
    godina_studija = models.CharField(max_length=9,null=False,choices=godina_studija_choices,default=prvaGodina)
    url = models.URLField(max_length=200)

    def __str__(self):
       return self.naziv_studija

class ucionica(models.Model):
    broj_ucionice = models.IntegerField(null=False)
    broj_mjesta = models.IntegerField(null=False)
    kat = models.IntegerField(null=False)
    slobodna_ucionica = models.BooleanField(default=True)

    def __str__(self):
        return str(self.broj_ucionice)


class termini(models.Model):

    

    datum = models.DateField(auto_now=True)
    vrijeme_pocetka = models.TimeField(auto_now_add=False, auto_now = False)
    zavrsetak = models.TimeField(auto_now_add=False, auto_now = False)

    trajanje = models.DurationField()
    naziv_kolegija = models.ForeignKey(kolegiji,max_length=30, null=False, on_delete=models.CASCADE)
    studij_fk = models.ForeignKey(studij, max_length= 30,null=False,on_delete=models.CASCADE)
    broj_ucionce_fk = models.ForeignKey(ucionica, max_length=30,null=False,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.naziv_kolegija)


class evidencija(models.Model):
    predavanja_fk = models.ForeignKey(termini,max_length=20,null=False,on_delete=models.CASCADE)
    osoba_fk = models.ForeignKey(osobe,max_length=20,null=False,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.predavanja_fk)