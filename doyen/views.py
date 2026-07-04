from django.shortcuts import render,redirect
from pages.models import inscription,reinscription,edition_pv,Doctorant,situation_doctorant,Soutenance
from .models import login_doyen
from django.contrib import messages
from encadreur.models import Encadreur
import json

# Create your views here.
def doyen_login(request):
    return render(request,'doyen/login.html')


def dashboards(request):
    """Strategic overview for the vice-dean."""
    doctorants = Doctorant.objects.select_related('user', 'encadreur').all()
    total = doctorants.count()
    valides = doctorants.filter(validation=True).count()

    nb_inscriptions = inscription.objects.count()
    nb_reinscriptions = reinscription.objects.count()
    nb_pv = edition_pv.objects.count()
    nb_soutenances = Soutenance.objects.count()
    soutenances_validees = Soutenance.objects.filter(action=True).count()
    nb_encadreurs = Encadreur.objects.count()

    year_labels = ['1re', '2e', '3e', '4e', '5e+']
    year_counts = [0, 0, 0, 0, 0]
    for d in doctorants:
        try:
            n = int(float((d.annee or '').strip()))
        except (TypeError, ValueError):
            n = 0
        if 1 <= n <= 4:
            year_counts[n - 1] += 1
        elif n >= 5:
            year_counts[4] += 1

    context = {
        'total': total,
        'valides': valides,
        'nb_encadreurs': nb_encadreurs,
        'nb_soutenances': nb_soutenances,
        'soutenances_validees': soutenances_validees,
        'nb_pv': nb_pv,
        'funnel_labels': json.dumps(['Inscription', 'Réinscription', 'Évaluation (PV)', 'Soutenance']),
        'funnel_values': json.dumps([nb_inscriptions or total, nb_reinscriptions, nb_pv, nb_soutenances]),
        'year_labels': json.dumps(year_labels),
        'year_values': json.dumps(year_counts),
    }
    return render(request, 'doyen/dashboards.html', context)

def index_doyen(request) :
    if request.method == 'POST':
        username = request.POST.get('username_doyen')
        password = request.POST.get('password_doyen')
        try:
            user=login_doyen.objects.get(username=username)
            if user.authenticate(username, password):
                # Authentication successful, redirect to the "demande_etat_avancement" page
                return redirect('dashboards')
            else:
                # Authentication failed, set an error message
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        except login_doyen.DoesNotExist:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        except login_doyen.MultipleObjectsReturned:
            messages.error(request, "Plusieurs comptes avec ce nom d'utilisateur existent. Veuillez contacter l'administration.")

    return render(request, 'doyen/login.html')
    

def liste_inscription_doyen(request):
    inscriptions = inscription.objects.all()
    return render(request, 'doyen/inscription.html', {'inscriptions': inscriptions})

def liste_reinscription_doyen(request):
    reinscriptions = reinscription.objects.all()
    return render(request, 'doyen/reinscription.html', {'reinscriptions': reinscriptions})


def editionPVdoyen(request):
    doctorants = Doctorant.objects.prefetch_related('inscription', 'reinscription', 'edition').all()
    editions=edition_pv.objects.all()
    return render(request, 'doyen/editionPVDoyen.html', {'doctorants': doctorants, 'editions': editions})
    


def etat_Avencement_doyen(request) :
    doctorants = Doctorant.objects.prefetch_related('inscription', 'reinscription', 'situation_doctorant').all()
    situations = situation_doctorant.objects.all()
    return render(request,'doyen/etat_d`avencement.html', {'doctorants': doctorants,'situations': situations})


def soutenances(request):
    doctorants = Doctorant.objects.prefetch_related('inscription', 'reinscription', 'soutenance').all()
    encadreurs = Encadreur.objects.all()
    return render(request, 'doyen/soutenancesDoyen.html', {'doctorants': doctorants, 'encadreurs': encadreurs})


#affiche les instance des inscription



    


