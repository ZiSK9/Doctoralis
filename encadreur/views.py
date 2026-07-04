from django.shortcuts import render,redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login
from pages.models import edition_pv,Soutenance,situation_doctorant
from django.contrib.auth.models import User
from.models import Encadreur
from pages.models import Doctorant
from django.contrib.auth.decorators import login_required
from django.db.models import Q



# Create your views here.


def encadreur_login(request):
    return render(request,'encadreur/login.html')


def demande_soutenance(request):
    encadreur = Encadreur.objects.get(user=request.user)
    doctorants = Doctorant.objects.filter(encadreur=encadreur)
    if request.method == 'POST':
        doctorant_id = request.POST.get('doctorant')
        doctorant = Doctorant.objects.get(id=doctorant_id)
        new_demande = Soutenance(
            doctorant=doctorant,
        )
        new_demande .save()        
        messages.success(request, 'Votre demande a été effectuée avec succès')
        return redirect('demandeSoutenance')  

    return render(request, 'encadreur/demande_soutenance.html', {'doctorants': doctorants})


def index_encadreur(request):
    if request.method == 'POST':
        username = request.POST.get('username_encadreur')
        password = request.POST.get('password_encadreur')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            encadreur = Encadreur.objects.filter(user=user).first()
            if encadreur.validation:
              login(request, user)
              return redirect('situations')
            else:
                # Account is not valid
                messages.error(request, 'Votre compte n`est pas validé par l`administration')
        else:
            # Authentication failed
            messages.error(request, 'Numéro inscription ou mot de passe incorrect.')    

    return render(request, 'encadreur/login.html')

def demande_compte_encadreur(request):
    if request.method == 'POST':
        nom_prenom = request.POST.get('nomPrenom_encadreur')
        username = request.POST.get('username_encadreur')
        password = request.POST.get('password_encadreur')

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            error_message = "Numéro d'inscription existe déjà"
            messages.error(request, error_message)
            return redirect('demandeCompte')

        # Create the user account
        user = User.objects.create_user(username=username, password=password)

        # Debugging: Print the values of all fields
        print("username:", username)
        print("password:", password)

        encadreur = Encadreur(user=user, nom_prenom=nom_prenom)

        # Save the file if it was uploaded
        
        encadreur.save()

        messages.success(request, "Votre demande a été envoyée à l'administration")

        # Redirect or render a success message
        return redirect('demandeCompteEncadreur')

    return render(request, 'encadreur/demande_compte_encadreur.html')

def situations(request):
    encadreur = Encadreur.objects.get(user=request.user)  # Retrieve the Encadreur instance of the currently logged-in user
    doctorants = encadreur.doctorants.all()  # Retrieve doctorants associated with the encadreur
    editions = edition_pv.objects.filter(doctorant__in=doctorants)  # Filter editions based on the doctorants
    return render(request, 'encadreur/situation_doctorants.html', {'doctorants': doctorants, 'editions': editions})
def etat(request):
    encadreur = Encadreur.objects.get(user=request.user)  # Retrieve the Encadreur instance of the currently logged-in user
    doctorants = encadreur.doctorants.all()  # Retrieve doctorants associated with the encadreur
    etats = situation_doctorant.objects.filter(doctorant__in=doctorants)  # Filter editions based on the doctorants
    return render(request, 'encadreur/etat.html', {'doctorants': doctorants, 'etats': etats})

def liste_doctorants(request):
    encadreur = Encadreur.objects.get(user=request.user)
    doctorants = Doctorant.objects.filter(encadreur=encadreur)
    return render(request, 'encadreur/liste_doctorants.html', {'doctorants': doctorants})





