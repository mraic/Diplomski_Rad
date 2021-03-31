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
from .forms import RegistrationForm, AccountAuthenticationForm
from .models import *
from .serializers import *

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


def register_view(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated:
		return HttpResponse("You are already authenticated as " + str(user.email))

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


def logout_view(request):
	logout(request)
	return redirect("home")


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
		termin_1 = termini.objects.all().filter(naziv_kolegija_id = k.id)
		evidencija_1 = evidencija.objects.all().filter(predavanja_fk_id__in = termin_1).count()
		chartPrisutnost .append(evidencija_1)


	kolegiji_1 = kolegiji.objects.all().filter(
		osobeFK=user_id)
	termin_1 = termini.objects.all().filter(naziv_kolegija_id__in =kolegiji_1)
	evidencija_1 = evidencija.objects.all().filter(predavanja_fk_id__in = termin_1).count

	context = {'koleg': koleg,'evidencija_1': evidencija_1,  'chartKolegiji': chartKolegiji, 'chartPrisutnost': chartPrisutnost}

	return render(request, 'user.html', context)


@login_required
def predmeti_view(request, pk):

	user_id = request.user.id
	koleg = kolegiji.objects.all().filter(osobeFK=user_id)

	chartKolegiji = []
	chartPrisutnost = []

	for k in koleg:
		chartKolegiji.append(k.naziv_kolegija)
		termin_1 = termini.objects.all().filter(naziv_kolegija_id = k.id)
		evidencija_1 = evidencija.objects.all().filter(predavanja_fk_id__in = termin_1).count()
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
            'broj_studenata_na_kolegiju': broj_studenata_na_kolegiju,'chartKolegiji' : chartKolegiji, 'chartPrisutnost' : chartPrisutnost }

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
		termin_1 = termini.objects.all().filter(naziv_kolegija_id = k.id)
		evidencija_1 = evidencija.objects.all().filter(predavanja_fk_id__in = termin_1).count()
		chartPrisutnost .append(evidencija_1)

	kolegiji_1 = kolegiji.objects.all().filter(
		osobeFK=user_id)
	termin_1 = termini.objects.all().filter(naziv_kolegija_id__in =kolegiji_1)

	evidencija_1 = evidencija.objects.all().filter(predavanja_fk_id__in = termin_1).count

	context = {'koleg': koleg, 'chartKolegiji': chartKolegiji, 'chartPrisutnost':chartPrisutnost}
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
		termin_1 = termini.objects.all().filter(naziv_kolegija_id = k.id)
		evidencija_1 = evidencija.objects.all().filter(predavanja_fk_id__in = termin_1).count()
		chartPrisutnost.append(evidencija_1)

	kolegiji_1 = kolegiji.objects.all().filter(
		osobeFK=user_id)
	termin_1 = termini.objects.all().filter(naziv_kolegija_id__in =kolegiji_1)

	evidencija_1 = evidencija.objects.all().filter(predavanja_fk_id__in = termin_1).count

	ispricaj_studenta_1 = 0

	context = {'koleg': koleg,'evidencija_1':evidencija_1, 'chartKolegiji': chartKolegiji, 'chartPrisutnost':chartPrisutnost,'ispricaj_studenta_1':ispricaj_studenta_1}
	return render(request,'ispricani_student.html' ,context)




## za CSV export
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
	serializer = ulogeSerializer(uloges, many = True)

	return Response(serializer.data)

@api_view(['GET'])
def ulogeDetail(request, pk):
	uloges = uloga.objects.get(id = pk)
	serializer = ulogeSerializer(uloges, many = False)

	return Response(serializer.data)

@api_view(['POST'])
def ulogeCreate(request):
	serializer = ulogeSerializer(data = request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def ulogeUpdate(request, pk):
	uloges = uloga.objects.get(id = pk)
	serializer = ulogeSerializer(instance = uloges, data = request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['GET'])
def kolegijiList(request):
	kolegijis = kolegiji.objects.all()
	serializer = kolegijiSerializer(kolegijis, many = True)

	return Response(serializer.data)

@api_view(['GET'])
def kolegijiDetail(request,pk):
	kolegijs = kolegiji.objects.get(id = pk)
	serializer = kolegijiSerializer(kolegijs, many = False)

	return Response(serializer.data)

@api_view(['POST'])
def kolegijiCreate(request):
	serializer = kolegijiSerializer(data = request.data)

	if serializer.is_valid():
		serializers.save()

	return Response(serializer.data)

@api_view(['POST'])
def kolegijiUpdate(request, pk):
	kolegijis = kolegiji.objects.get(id = pk)
	serializer = kolegijiSerializer(instance=kolegijis, data = request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)



@api_view(['GET'])
def studijList(request):
	studijs = studij.objects.all()
	serializer = studijSerializer(studijs, many = True)

	return Response(serializer.data)

@api_view(['GET'])
def studijDetail(request,pk):
	studijs = studij.objects.get(id = pk)
	serializer = studijSerializer(studijs, many = False)

	return Response(serializer.data)

@api_view(['POST'])
def studijCreate(request):
	serializer = studijSerializer(data = request.data)

	if serializer.is_valid():
		serializers.save()

	return Response(serializer.data)

@api_view(['POST'])
def studijUpdate(request, pk):
	studijs = studij.objects.get(id = pk)
	serializer = studijSerializer(instance=studijs, data = request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)




@api_view(['GET'])
def terminiList(request):
	terminis = termini.objects.all()
	serializer = terminiSerializer(terminis, many = True)

	return Response(serializer.data)

@api_view(['GET'])
def terminiDetail(request,pk):
	terminis = termini.objects.get(id = pk)
	serializer = terminiSerializer(terminis, many = False)

	return Response(serializer.data)

@api_view(['POST'])
def terminiCreate(request):
	serializer = terminiSerializer(data = request.data)

	if serializer.is_valid():
		serializers.save()

	return Response(serializer.data)

@api_view(['POST'])
def terminiUpdate(request, pk):
	terminis = termini.objects.get(id = pk)
	serializer = terminiSerializer(instance=terminis, data = request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)



@api_view(['GET'])
def ucionicaList(request):
	ucionicas = ucionica.objects.all()
	serializer = ucionicaSerializer(ucionicas, many = True)

	return Response(serializer.data)

@api_view(['GET'])
def ucionicaDetail(request,pk):
	ucionicas = ucionica.objects.get(id = pk)
	serializer = ucionicaSerializer(ucionicas, many = False)

	return Response(serializer.data)

@api_view(['POST'])
def ucionicaCreate(request):
	serializer = ucionicaSerializer(data = request.data)

	if serializer.is_valid():
		serializers.save()

	return Response(serializer.data)

@api_view(['POST'])
def ucionicaUpdate(request, pk):
	ucionicas = ucionica.objects.get(id = pk)
	serializer = ucionicaSerializer(instance=ucionicas, data = request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)



@api_view(['GET'])
def evidencijaList(request):
	evidencijas = evidencija.objects.all()
	serializer = evidencijaSerializer(evidencijas, many = True)

	return Response(serializer.data)

@api_view(['GET'])
def evidencijaDetail(request,pk):
	evidencijas = evidencija.objects.get(id = pk)
	serializer = evidencijaSerializer(evidencijas, many = False)

	return Response(serializer.data)

@api_view(['POST'])
def evidencijaCreate(request):
	serializer = evidencijaSerializer(data = request.data)

	if serializer.is_valid():
		serializers.save()

	return Response(serializer.data)

@api_view(['POST'])
def evidencijaUpdate(request, pk):
	evidencijas = evidencija.objects.get(id = pk)
	serializer = evidencijaSerializer(instance=evidencijas, data = request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)




#                                 ###### API #######


# # uloge
# def getUloge (request):
#     qs=models.uloga.objects.all()
#     qs_json = serializers.serialize('json', qs)
#     return HttpResponse(qs_json, content_type='application/json')

# ## post uloge ##
# def postUloge(request):
#     naziv=request.POST.get('naziv')
#     uloga_create = models.uloga.objects.create(naziv = naziv)
#     return HttpResponse(naziv)

# ## delete uloge ##
# def deleteUloge(request):
#     naziv = request.POST.get("naziv")
#     models.uloga.objects.filter(naziv=naziv).delete()
#     return HttpResponse ("Uloga naziva "+naziv+" je izbrisana!")

# ## update uloge ##
# def updateUloge (request):
#     naziv=request.POST.get('naziv')
#     uloga_updated = models.uloga(
#         naziv = naziv
#         )
#     uloga_updated = models.uloga.objects.create(naziv=naziv)
#     uloga_updated.save()
#     return HttpResponse ("Edit sucessfull")


# ## get za studenta
# def getStudent (request, br_indeksa):
#     qs=models.osobe.objects.filter(broj_indeksa=br_indeksa)
#     qs_json = serializers.serialize('json', qs)
#     return HttpResponse(qs_json, content_type='application/json')

# ## create studenta
# def postStudent (request):
#     broj_indeksa=request.POST.get('broj_indeksa')
#     ime=request.POST.get('ime')
#     prezime=request.POST.get('prezime')
#     email=request.POST.get('email')
#     uloga=request.POST.get('uloga')
#     ulogaFK=models.uloga.objects.get(id=uloga)

#     student = models.osobe.objects.create(broj_indeksa=broj_indeksa, ime=ime, prezime=prezime, email=email, ulogaFK=ulogaFK)

#     return HttpResponse("Student s brojem indeksa " + broj_indeksa +" je uspješno dodan !")

# ## delete za studenta
# def deleteStudent (request):
#     broj_indeksa = request.POST.get("broj_indeksa")
#     models.osobe.objects.filter(broj_indeksa=broj_indeksa).delete()
#     return HttpResponse ("Student je izbrisan!")

# ## update za studenta
# def updateStudent (request):

#     broj_indeksa=request.POST.get('broj_indeksa')
#     ime=request.POST.get('ime')
#     prezime=request.POST.get('prezime')
#     email=request.POST.get('email')
#     uloga=request.POST.get('uloga')
#     user = models.osobe(
#             broj_indeksa = broj_indeksa,
#             ime = ime,
#             prezime = prezime,
#             email = email,
#             ulogaFK=models.uloga.objects.get(id=uloga),
#             datum_kreiranja=datetime.now()

#         )
#     user.save()
#     return HttpResponse ("Student je uspješno updatean ! ")


# #get studija
# def getStudija (request):
#     qs=models.studij.objects.all()
#     qs_json = serializers.serialize('json', qs)
#     return HttpResponse(qs_json, content_type='application/json')

# ## create studija
# def postStudija (request):
#     naziv_studija=request.POST.get('naziv_studija')
#     godina_studija=request.POST.get('godina_studija')
#     url=request.POST.get('url')

#     naziv_studija_create = models.studij.objects.create(naziv_studija=naziv_studija, godina_studija=godina_studija, url=url)

#     return HttpResponse(naziv_studija)


# ## delete studija
# def deleteStudija (request):
#     naziv_studija = request.POST.get("naziv_studija")
#     models.studij.objects.filter(naziv_studija=naziv_studija).delete()
#     return HttpResponse ("Naziv studija "+naziv_studija+" je izbrisan!")

# ## update studija
# def updateStudija (request):
#     pk = request.POST.get('pk')
#     naziv_studija=request.POST.get('naziv_studija')
#     godina_studija=request.POST.get('godina_studija')
#     url=request.POST.get('url')
#     studij_update = models.studij(
#             pk = pk,
#             naziv_studija = naziv_studija,
#             godina_studija = godina_studija,
#             url = url
#         )
#     studij_update.save()
#     return HttpResponse ("Edit sucessfull")


# #get getkolegija
# def getKolegija (request):
#     qs=models.kolegiji.objects.all()
#     qs_json = serializers.serialize('json', qs)
#     return HttpResponse(qs_json, content_type='application/json')

# ## create kolegija
# def postKolegija (request):
#     naziv_kolegija=request.POST.get('naziv_kolegija')
#     akademska_godina=request.POST.get('akademska_godina')
#     broj_indeksa = request.POST.get('broj_indeksa')
#     osobeFK=models.osobe.objects.get(broj_indeksa = broj_indeksa)

#     naziv_kolegija_create = models.kolegiji.objects.create(
#         naziv_kolegija=naziv_kolegija,
#         akademska_godina=akademska_godina,
#         osobeFK=osobeFK
#         )

#     return HttpResponse(naziv_kolegija_create)

# ## delete kolegija
# def deleteKolegija (request):
#     naziv_kolegija = request.POST.get("naziv_kolegija")
#     models.kolegiji.objects.filter(naziv_kolegija=naziv_kolegija).delete()
#     return HttpResponse ("Naziv studija "+naziv_kolegija+" je izbrisan!")

# ## update kolegija
# def updateKolegija (request):
#     pk = request.POST.get('pk')
#     naziv_kolegija=request.POST.get('naziv_kolegija')
#     akademska_godina=request.POST.get('akademska_godina')
#     broj_indeksa = request.POST.get('broj_indeksa')
#     kolegij = models.kolegiji(
#             pk = pk,
#             naziv_kolegija = naziv_kolegija,
#             akademska_godina = akademska_godina,
#             osobeFK=models.osobe.objects.get(broj_indeksa=broj_indeksa)
#         )
#     kolegij.save()
#     return HttpResponse ("Edit sucessfull")


# #get ucionice
# def getUcionice (request):
#     qs=models.ucionica.objects.all()
#     qs_json = serializers.serialize('json', qs)
#     return HttpResponse(qs_json, content_type='application/json')

# ## create ucionice
# def postUcionice (request):
#     broj_ucionice=request.POST.get('broj_ucionice')
#     broj_mjesta=request.POST.get('broj_mjesta')
#     kat=request.POST.get('kat')
#     slobodna_ucionica=request.POST.get('slobodna_ucionica')

#     broj_ucionice_create = models.ucionica.objects.create(broj_ucionice=broj_ucionice, broj_mjesta=broj_mjesta, kat=kat,slobodna_ucionica=slobodna_ucionica)

#     return HttpResponse(broj_ucionice_create, content_type='application/json')

# ## delete ucionice
# def deleteUcionice (request):
#     broj_ucionice = request.POST.get("broj_ucionice")
#     models.ucionica.objects.filter(broj_ucionice=broj_ucionice).delete()
#     return HttpResponse ("Ucionica je uspješno izbrisana!")

# ## update kolegija
# def updateUcionice (request):
#     pk = request.POST.get('pk')
#     broj_ucionice=request.POST.get('broj_ucionice')
#     broj_mjesta=request.POST.get('broj_mjesta')
#     kat=request.POST.get('kat')
#     slobodna_ucionica=request.POST.get('slobodna_ucionica')
#     ucionica_create = models.ucionica(
#             broj_ucionice = broj_ucionice,
#             broj_mjesta = broj_mjesta,
#             kat=kat,
#             slobodna_ucionica=slobodna_ucionica
#         )
#     ucionica_create.save()
#     return HttpResponse ("Edit sucessfull")


# #gettermina
# def getTermina (request):
#     qs=models.termini.objects.all()
#     qs_json = serializers.serialize('json', qs)
#     return HttpResponse(qs_json, content_type='application/json')

# ## create termina
# def postTermina (request):
#     datum=request.POST.get('datum')
#     vrijeme_pocetka=request.POST.get('vrijeme_pocetka')
#     zavrsetak=request.POST.get('zavrsetak')
#     trajanje = request.POST.get('trajanje')

#     naziv_kolegija = request.POST.get('naziv_kolegija')
#     studij = request.POST.get('naziv_studija')
#     id_ucionice = request.POST.get('id_ucionice')

#     naziv_kolegija=models.kolegiji.objects.get(naziv_kolegija=naziv_kolegija)
#     studij_fk = models.studij.objects.get(id = studij)
#     broj_ucionce_fk = models.ucionica.objects.get(id=id_ucionice)

#     termini_create = models.termini.objects.create(datum=datum, vrijeme_pocetka=vrijeme_pocetka, zavrsetak=zavrsetak,trajanje=trajanje,naziv_kolegija=naziv_kolegija,studij_fk=studij_fk,broj_ucionce_fk=broj_ucionce_fk)

#     return HttpResponse(termini_create)

# ## delete termina
# def deleteTermina(request):
#     naziv_kolegija = request.POST.get("naziv_kolegija")
#     models.kolegiji.objects.filter(naziv_kolegija=naziv_kolegija).delete()
#     return HttpResponse ("Termin s nazivom "+naziv_kolegija+"i datumom je izbrisan!")

# ## update termina
# def updateTermina (request):
#     datum=request.POST.get('datum')
#     vrijeme_pocetka=request.POST.get('vrijeme_pocetka')
#     zavrsetak=request.POST.get('zavrsetak')
#     trajanje = request.POST.get('trajanje')
#     naziv_kolegija=request.POST.get('naziv_kolegija')
#     naziv_studija = request.POST.get('naziv_studija')
#     broj_ucionice = request.POST.get('broj_ucionice')
#     termin_create = models.termini(
#             vrijeme_pocetka = vrijeme_pocetka,
#             zavrsetak = zavrsetak,
#             trajanje=trajanje,
#             naziv_kolegija=naziv_kolegija,
#             studij_fk=models.studij.objects.get(naziv_studija=naziv_studija),
#             broj_ucionce_fk=models.ucionica.objects.get(broj_ucionice=broj_ucionice)
#         )
#     termin_create.save()
#     return HttpResponse ("Edit sucessfull")


# ### evidencija ###


# def getEvidencije (request):
#     qs=models.evidencija.objects.all()
#     qs_json = serializers.serialize('json', qs)
#     return HttpResponse(qs_json, content_type='application/json')

# def postEvidencije (request):
#     predavanja_fk=request.POST.get('predavanja_fk')
#     broj_indeksa=request.POST.get('broj_indeksa')

#     predavanja_fk = models.termini.objects.get(id = predavanja_fk)
#     osoba_fk = models.osobe.objects.get(broj_indeksa=broj_indeksa)

#     evidencija_create = models.evidencija.objects.create(predavanja_fk=predavanja_fk, osoba_fk=osoba_fk)

#     return HttpResponse("Evidencija je dodana")
