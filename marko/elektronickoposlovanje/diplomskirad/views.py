from django.shortcuts import render, redirect
from django.http import JsonResponse, response

from django.core import serializers
import csv
from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

from rest_framework.response import Response
from .forms import UserCreationForm, RegistrationForm, AccountAuthenticationForm
from .models import *
from .serializers import *

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("Već ste logirani kao " + str(user.email))

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)


def login_view(request, *args, **kwargs):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("user")

    destination = get_redirect_if_exists(request)
    print("destination: " + str(destination))

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect("user")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    return render(request, "login.html", context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def user(request):

    user_id = request.user.id
    koleg = kolegiji.objects.all().filter(
        osobeFK=user_id).order_by('naziv_kolegija')

    chartKolegiji = []
    chartPrisutnost = []

    for k in koleg:
        chartKolegiji.append(k.naziv_kolegija)
        termin_1 = termini.objects.all().filter(naziv_kolegija_id=k.id)
        evidencija_1 = evidencija.objects.all().filter(
            predavanja_fk_id__in=termin_1).count()
        chartPrisutnost.append(evidencija_1)

    kolegiji_1 = kolegiji.objects.all().filter(
        osobeFK=user_id)
    termin_1 = termini.objects.all().filter(naziv_kolegija_id__in=kolegiji_1)
    evidencija_1 = evidencija.objects.all().filter(
        predavanja_fk_id__in=termin_1).count()

    context = {'koleg': koleg, 'evidencija_1': evidencija_1,
               'chartKolegiji': chartKolegiji, 'chartPrisutnost': chartPrisutnost}

    return render(request, 'user.html', context)


@login_required
def predmeti_view(request, pk):

    user_id = request.user.id
    koleg = kolegiji.objects.all().filter(osobeFK=user_id)

    chartKolegiji = []
    chartPrisutnost = []

    for k in koleg:
        chartKolegiji.append(k.naziv_kolegija)
        termin_1 = termini.objects.all().filter(naziv_kolegija_id=k.id)
        evidencija_1 = evidencija.objects.all().filter(
            predavanja_fk_id__in=termin_1).count()
        chartPrisutnost.append(evidencija_1)

    #predmeti = termini.objects.get(naziv_kolegija_id=pk)

    predmeti1 = koleg = kolegiji.objects.all().filter(
        osobeFK=user_id).order_by('naziv_kolegija')

    try:
        predmeti = termini.objects.get(naziv_kolegija_id=pk)
        broj_studenata_na_kolegiju = evidencija.objects.filter(
            predavanja_fk_id=predmeti).count()
    except:
        broj_studenata_na_kolegiju = 0

    context = {'koleg': koleg, 'predmeti1': predmeti1,
               'broj_studenata_na_kolegiju': broj_studenata_na_kolegiju, 'chartKolegiji': chartKolegiji, 'chartPrisutnost': chartPrisutnost}

    return render(request, 'predmeti.html', context)


@login_required
def logoutUser(request):
    logout(request)
    return redirect('login.html')


@login_required
def nadzornaPlocaView(request):

    user_id = request.user.id
    koleg = kolegiji.objects.all().filter(
        osobeFK=user_id).order_by('naziv_kolegija')

    chartKolegiji = []
    chartPrisutnost = []

    for k in koleg:
        chartKolegiji.append(k.naziv_kolegija)
        termin_1 = termini.objects.all().filter(naziv_kolegija_id=k.id)
        evidencija_1 = evidencija.objects.all().filter(
            predavanja_fk_id__in=termin_1).count()
        chartPrisutnost .append(evidencija_1)

    kolegiji_1 = kolegiji.objects.all().filter(
        osobeFK=user_id)
    termin_1 = termini.objects.all().filter(naziv_kolegija_id__in=kolegiji_1)

    evidencija_1 = evidencija.objects.all().filter(
        predavanja_fk_id__in=termin_1).count

    context = {'koleg': koleg, 'chartKolegiji': chartKolegiji,
               'chartPrisutnost': chartPrisutnost}
    return render(request, 'nadzorna_ploca.html', context)


@login_required
def ispricaj_studenta(request):
    user_id = request.user.id
    koleg = kolegiji.objects.all().filter(
        osobeFK=user_id).order_by('naziv_kolegija')

    chartKolegiji = []
    chartPrisutnost = []

    for k in koleg:
        chartKolegiji.append(k.naziv_kolegija)
        termin_1 = termini.objects.all().filter(naziv_kolegija_id=k.id)
        evidencija_1 = evidencija.objects.all().filter(
            predavanja_fk_id__in=termin_1).count()
        chartPrisutnost.append(evidencija_1)

    kolegiji_1 = kolegiji.objects.all().filter(
        osobeFK=user_id)
    termin_1 = termini.objects.all().filter(naziv_kolegija_id__in=kolegiji_1)

    evidencija_1 = evidencija.objects.all().filter(
        predavanja_fk_id__in=termin_1).count

    ispricaj_studenta_1 = 0

    context = {'koleg': koleg, 'evidencija_1': evidencija_1, 'chartKolegiji': chartKolegiji,
               'chartPrisutnost': chartPrisutnost, 'ispricaj_studenta_1': ispricaj_studenta_1}
    return render(request, 'ispricani_student.html', context)


# za CSV export
def export(request):
    response = HttpResponse(content_type='text/csv')

    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response)
    writer.writerow(['Ime', 'Prezime', 'Broj indeksa', 'Email'])

    for osoba in osobe.objects.all().values_list('ime', 'prezime', 'broj_indeksa', 'email'):
        writer.writerow(osoba)

    response['Content-Disposition'] = 'attachment; filename="osobe.csv"'

    return response


# def export_raspored_csv(request):
# 	response = HttpResponse(content_type='text/csv')
# 	response['Content-Disposition'] = "attachment; filename = 'Predmet.csv'"
# 	return response


@api_view(['GET'])
def apiOverview(request):
    api_urls = {

        "Popis osobe": "/osobe-list/",
        "Detaljan pregled osobe": "/osobe-detail/<str:pk>",
        "Stvori osobe": "/osobe-create/",
        "Ažuriraj osobe": "/osobe-update/<str:pk>",

        "Popis uloge": "/uloge-list/",
        "Detaljan pregled uloge": "/uloge-detail/<str:pk>",
        "Stvori uloge": "/uloge-create/",
        "Ažuriraj uloge": "/uloge-update/<str:pk>",

        "Popis kolegija": "/kolegij-list/",
        "Detaljan pregled kolegija": "/kolegij-detail/<str:pk>",
        "Stvori kolegij": "/kolegij-create/",
        "Ažuriraj kolegij": "/kolegij-update/<str:pk>",

        "Popis studija": "/studij-list/",
        "Detaljan pregled studij": "/studij-detail/<str:pk>",
        "Stvori studij": "/studij-create/",
        "Ažuriraj studij": "/studij-update/<str:pk>",

        "Popis ucionica": "/ucionica-list/",
        "Detaljan pregled ucionica": "/ucionica-detail/<str:pk>",
        "Stvori ucionicu": "/ucionica-create/",
        "Ažuriraj ucionicu": "/ucionica-update/<str:pk>",

        "Popis termina": "/termini-list/",
        "Detaljan pregled termina": "/termini-detail/<str:pk>",
        "Stvori termin": "/termini-create/",
        "Ažuriraj termini": "/termini-update/<str:pk>",

        "Popis evidencija": "/evidencija-list/",
        "Detaljan pregled evidencija": "/evidencija-detail/<str:pk>",
        "Stvori evidenciju": "/evidencija-create/",
        "Ažuriraj evidenciju": "/evidencija-update/<str:pk>",


    }

    return Response(api_urls)


@api_view(['GET'])
def osobeList(request):
    osobes = osobe.objects.all()
    serializer = osobeSerializer(osobes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def osobeDetail(request, pk):
    osobes = osobe.objects.get(broj_indeksa=pk)
    serializer = osobeSerializer(osobes, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def osobeCreate(request):
    serializer = osobeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def osobeUpdate(request, pk):
    osobes = osobe.objects.get(broj_indeksa=pk)
    serializer = osobeSerializer(instance=osobes, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def ulogeList(request):
    uloges = uloga.objects.all()
    serializer = ulogeSerializer(uloges, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def ulogeDetail(request, pk):
    uloges = uloga.objects.get(id=pk)
    serializer = ulogeSerializer(uloges, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def ulogeCreate(request):
    serializer = ulogeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def ulogeUpdate(request, pk):
    uloges = uloga.objects.get(id=pk)
    serializer = ulogeSerializer(instance=uloges, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def kolegijiList(request):
    kolegijis = kolegiji.objects.all()
    serializer = kolegijiSerializer(kolegijis, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def kolegijiDetail(request, pk):
    kolegijs = kolegiji.objects.get(id=pk)
    serializer = kolegijiSerializer(kolegijs, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def kolegijiCreate(request):
    serializer = kolegijiSerializer(data=request.data)

    if serializer.is_valid():
        serializers.save()

    return Response(serializer.data)


@api_view(['POST'])
def kolegijiUpdate(request, pk):
    kolegijis = kolegiji.objects.get(id=pk)
    serializer = kolegijiSerializer(instance=kolegijis, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def studijList(request):
    studijs = studij.objects.all()
    serializer = studijSerializer(studijs, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def studijDetail(request, pk):
    studijs = studij.objects.get(id=pk)
    serializer = studijSerializer(studijs, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def studijCreate(request):
    serializer = studijSerializer(data=request.data)

    if serializer.is_valid():
        serializers.save()

    return Response(serializer.data)


@api_view(['POST'])
def studijUpdate(request, pk):
    studijs = studij.objects.get(id=pk)
    serializer = studijSerializer(instance=studijs, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def terminiList(request):
    terminis = termini.objects.all()
    serializer = terminiSerializer(terminis, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def terminiDetail(request, pk):
    terminis = termini.objects.get(id=pk)
    serializer = terminiSerializer(terminis, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def terminiCreate(request):
    serializer = terminiSerializer(data=request.data)

    if serializer.is_valid():
        serializers.save()

    return Response(serializer.data)


@api_view(['POST'])
def terminiUpdate(request, pk):
    terminis = termini.objects.get(id=pk)
    serializer = terminiSerializer(instance=terminis, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def ucionicaList(request):
    ucionicas = ucionica.objects.all()
    serializer = ucionicaSerializer(ucionicas, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def ucionicaDetail(request, pk):
    ucionicas = ucionica.objects.get(id=pk)
    serializer = ucionicaSerializer(ucionicas, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def ucionicaCreate(request):
    serializer = ucionicaSerializer(data=request.data)

    if serializer.is_valid():
        serializers.save()

    return Response(serializer.data)


@api_view(['POST'])
def ucionicaUpdate(request, pk):
    ucionicas = ucionica.objects.get(id=pk)
    serializer = ucionicaSerializer(instance=ucionicas, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def evidencijaList(request):
    evidencijas = evidencija.objects.all()
    serializer = evidencijaSerializer(evidencijas, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def evidencijaDetail(request, pk):
    evidencijas = evidencija.objects.get(id=pk)
    serializer = evidencijaSerializer(evidencijas, many=False)

    return Response(serializer.data)


@api_view(['POST'])
def evidencijaCreate(request):
    serializer = evidencijaSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def evidencijaUpdate(request, pk):
    evidencijas = evidencija.objects.get(id=pk)
    serializer = evidencijaSerializer(instance=evidencijas, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)
