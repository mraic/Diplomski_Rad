from django.shortcuts import render, redirect
from django.http import JsonResponse, response

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

	#broj_st = evidencija.objects.raw('SELECT COUNT(*) FROM public."ElektronickoPoslovanje_evidencija" as e LEFT JOIN public."ElektronickoPoslovanje_termini"  as t ON e.predavanja_fk_id = t.id WHERE t.naziv_kolegija_id = 3')
	broj_st = evidencija.objects.all().count()

	#predmeti1 = kolegiji.objects.all()

	context = {'koleg': koleg, 'broj_st': broj_st}
	return render(request, 'user.html', context)


@login_required
def predmeti_view(request, pk):

	user_id = request.user.id
	koleg = kolegiji.objects.all().filter(osobeFK=user_id)

	predmeti = termini.objects.get(naziv_kolegija_id=pk)

	predmeti1 = kolegiji.objects.all().order_by('naziv_kolegija')

	
	broj_studenata_na_kolegiju = evidencija.objects.filter(predavanja_fk_id = predmeti).count()

	context = {'koleg': koleg, 'predmeti1': predmeti1,
               'broj_studenata_na_kolegiju': broj_studenata_na_kolegiju}

	
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

    context = {'koleg': koleg}
    return render(request, 'nadzorna_ploca.html', context)


## za CSV export
def export(request):
	response = HttpResponse(content_type = 'text/csv')

	response.write(u'\ufeff'.encode('utf8'))
	writer = csv.writer(response)
	writer.writerow(['Ime', 'Prezime', 'Broj indeksa', 'Email'])

	for osoba in osobe.objects.all().values_list('ime','prezime', 'broj_indeksa','email'):
		writer.writerow(osoba)

	response['Content-Disposition'] = 'attachment; filename="osobe.csv"'

	return response




@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List osobe': '/osobe-list/',
        'Detail View osobe': "/osobe-detail/<str:pk>",
        "Create osobe": "/osobe-create/",
        "Update osobe": "/osobe-update/<str:pk>",
        "Delete osobe": "/osobe-delete/<str:pk>",
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
