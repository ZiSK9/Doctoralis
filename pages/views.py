
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import reinscription,situation_doctorant,edition_pv,inscription,Passage
from cfd.models import ApplicationSettings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from pages.models import Doctorant
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import get_user
from django.core.exceptions import ObjectDoesNotExist




# Create your views here.

def index(request):
    return render(request,'index.html')

def doctorantlogin(request):
    return render(request,'login.html')

def demande_compte(request):
    if request.method == 'POST':
        username = request.POST.get('numero_inscription')
        password = request.POST.get('password')
        annee = request.POST.get('select_annee')
        fichier_inscription = request.FILES.get('fichier_inscription')

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            error_message = "Numéro d'inscription existe déjà"
            messages.error(request, error_message)
            return redirect('demandeCompte')

        # Create the user account
        user = User.objects.create_user(username=username, password=password)
        doctorant = Doctorant(user=user, annee=annee)

        # Save the file if it was uploaded
        if fichier_inscription:
            doctorant.fichier_inscription = fichier_inscription
        doctorant.save()
        print("User ID:", user.id)
        print("Doctorant ID:", doctorant.id)


        messages.success(request, "Votre demande a été envoyée à l'administration")

        # Redirect or render a success message
        return redirect('demandeCompte')

    return render(request, 'demande_compte.html')



def index_doctorant(request):
    if request.method == 'POST':
        username = request.POST.get('numero_inscription')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            doctorant = Doctorant.objects.filter(user=user).first()

            if doctorant.validation:
                # Check if doctorant exists in inscription or reinscription
                inscription_exists = inscription.objects.filter(doctorant=doctorant).exists()
                reinscription_exists = reinscription.objects.filter(doctorant=doctorant).exists()
                passage = Passage.objects.filter(doctorant=doctorant).first()
                reinscription_open=ApplicationSettings.objects.first()

                if passage is None:
    # User not found in Passage model, skip the operation
                     pass
                elif inscription_exists or reinscription_exists and passage.passage_annee_validation:
                     if reinscription_open.reinscription_open :
                        login(request, user)
                        return redirect('reinscription')
                     else : 
                          messages.error(request, "la réinscription elle est fermé maintenant contacter l'administration")
                          return redirect('indexDoctorant')
                         
                         
                

                if inscription_exists or reinscription_exists:
                    # Doctorant exists in inscription or reinscription, redirect to etat_d`avencement
                    login(request, user)
                    return redirect('etat_d`avencement')
                
                if doctorant.annee == '1':
                    if reinscription_open.reinscription_open  :
                        login(request, user)
                        return redirect('inscription')
                    else : 
                          messages.error(request, "l`inscription elle est fermé maintenant contacter l'administration")
                          return redirect('indexDoctorant')  

                else:
                     if reinscription_open.reinscription_open  :
                        login(request, user)
                        return redirect('reinscription')
                     else : 
                          messages.error(request, "la réinscription elle est fermé maintenant contacter l'administration")
                          return redirect('indexDoctorant')

            else:
                # Account is not valid
                messages.error(request, 'Votre compte n`est pas validé par l`administration')

        else:
            # Authentication failed
            messages.error(request, 'Numéro inscription ou mot de passe incorrect.')

    return render(request, 'login.html')





@login_required
def test_points(request):
    try:
        doctorant = Doctorant.objects.get(user=request.user)
        editions = edition_pv.objects.filter(doctorant=doctorant)    
    except Doctorant.DoesNotExist:
        editions = None
    
    return render(request, 'point.html', { 'editions': editions})





@login_required
def inscriptions(request):
    if request.method == 'POST':
        numero_inscription = request.POST.get('numero_inscription')
        nom = request.POST.get('Nom')
        prenom = request.POST.get('prenom')
        titre_sujet = request.POST.get('titre_sujet')
        date_premier_inscription = request.POST.get('date_1ere_inscription')
        nom_encadreur = request.POST.get('nom_encadreur')
        nom_co_encadreur = request.POST.get('nom_co_encadreur')
        mail_public = request.POST.get('mail_public')
        mail_institutionnel = request.POST.get('mail_institutionnel')
        fichier_inscription = request.FILES.get('fichier_inscription')

        # Get the current user and create a new inscription object associated with the user
        user = request.user
        doctorant = user.doctorant
        if Passage.objects.filter(doctorant=doctorant).exists():
            # Delete the doctorant from the Passage model
            Passage.objects.filter(doctorant=doctorant).delete()
        new_inscription = inscription(
            doctorant=doctorant,
            numero_inscription=numero_inscription,
            nom=nom,
            prenom=prenom,
            titre_sujet=titre_sujet,
            date_premier_inscription=date_premier_inscription,
            nom_encadreur=nom_encadreur,
            nom_co_encadreur=nom_co_encadreur,
            mail_public=mail_public,
            mail_institutionnel=mail_institutionnel,
            fichier_inscription=fichier_inscription
        )
        new_inscription.save()        
        messages.success(request, 'Votre inscription a été effectuée avec succès.')
        return redirect('etat_d`avencement')
    else:
        return render(request, 'inscription.html')
    




@login_required
def reinscription_doctorat(request):
    if request.method == 'POST':
        numero_inscription = request.POST.get('numero_inscription')
        nom = request.POST.get('Nom')
        prenom = request.POST.get('prenom')
        select_annee = request.POST.get('select_annee')
        titre_sujet = request.POST.get('titre_sujet')
        nouveau_titre_sujet = request.POST.get('changement_sujet')
        date_premier_inscription = request.POST.get('date_1ere_inscription')
        nom_encadreur = request.POST.get('nom_encadreur')
        nom_co_encadreur = request.POST.get('nom_co_encadreur')
        nouveau_nom_encadreur = request.POST.get('nouveau_nom_encadreur')
        nouveau_nom_co_encadreur = request.POST.get('nouveau_nom_co_encadreur')
        mail_public = request.POST.get('mail_public')
        mail_institutionnel = request.POST.get('mail_institutionnel')
        fichier_inscription = request.FILES.get('fichier_inscription')


        # Get the current user and create a new reinscription object associated with the user
        user = request.user
        doctorant = user.doctorant
        if Passage.objects.filter(doctorant=doctorant).exists():
            # Delete the doctorant from the Passage model
            Passage.objects.filter(doctorant=doctorant).delete()
        doctorant.annee = select_annee
        doctorant.save()
        new_reinscription = reinscription(
            doctorant=doctorant,
            numero_inscription=numero_inscription,
            nom=nom,
            prenom=prenom,
            titre_sujet=titre_sujet,
            nouveau_titre_sujet=nouveau_titre_sujet,
            date_premier_inscription=date_premier_inscription,
            nom_encadreur=nom_encadreur,
            nom_co_encadreur=nom_co_encadreur,
            nouveau_nom_encadreur=nouveau_nom_encadreur,
            nouveau_nom_co_encadreur=nouveau_nom_co_encadreur,
            mail_public=mail_public,
            mail_institutionnel=mail_institutionnel,
            fichier_inscription=fichier_inscription
        )

        # Save the new instance to the database
        new_reinscription.save()   
        try:
            # Check if the user has a Passage object
            passage = Passage.objects.get(doctorant=doctorant)
            passage.delete()  # Delete the Passage object
        except ObjectDoesNotExist:
            pass  # The Passage object doesn't exist, do nothing
        messages.success(request, 'Votre réinscription a été effectuée avec succès.')
        return redirect('changement')     
    else:
        return render(request, 'reinscription.html')
    

@login_required
def changement(request):
    if request.method == 'POST':
        # Get the current user
        user = request.user

        nouveau_titre_sujet = request.POST.get('changement_sujet')
        nouveau_nom_encadreur = request.POST.get('nouveau_nom_encadreur')
        nouveau_nom_co_encadreur = request.POST.get('nouveau_nom_co_encadreur')
        fichier_csd = request.FILES.get('fichier_CSD')

        # Retrieve the existing reinscription object for the current user
        existing_reinscription = reinscription.objects.filter(numero_inscription=user.username).first()

        if existing_reinscription:
            # Update the fields with the new values
            existing_reinscription.nouveau_titre_sujet = nouveau_titre_sujet
            existing_reinscription.nouveau_nom_encadreur = nouveau_nom_encadreur
            existing_reinscription.nouveau_nom_co_encadreur = nouveau_nom_co_encadreur
            existing_reinscription.pv_csd = fichier_csd

            # Save the updated reinscription object
            existing_reinscription.save()
        
        # Redirect or render a success message
        return redirect('etat_d`avencement')
    
    return render(request, 'changement.html')

    
@login_required
def etat_avencement(request):
    if request.method == 'POST':
        communication = request.POST.get('communication')
        publication = request.POST.get('publication')
        user = request.user
        doctorant = Doctorant.objects.get(user=user)
        situation = situation_doctorant(doctorant=doctorant, communication=communication, publication=publication)
        situation.save()
        messages.success(request, 'Merci pour mettre à jour votre situation')
        return redirect('etat_d`avencement')

    return render(request, 'etat_d`avencement.html')
    

@login_required
def passage_annee(request):
    if request.method == 'POST':
        fichier_reinscription_passage = request.FILES.get('fichier_reinscription_passage')
        user = request.user
        doctorant = Doctorant.objects.get(user=user)
        passage = Passage(doctorant=doctorant, fichier_reinscription_passage=fichier_reinscription_passage)
        passage.save()
        messages.success(request, "Votre demande a été envoyée à l'administration")
    
    
    return render(request, 'passage_annee.html')







                    












