from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('indexEncadreur/',views.index_encadreur,name='indexEncadreur'),
    path('loginEncadreur/',views.encadreur_login,name='loginEncadreur'),
    path('demandeCompteEncadreur/',views.demande_compte_encadreur,name='demandeCompteEncadreur'),
    path('situations/',views.situations,name='situations'),
    path('listeDoctorans/',views.liste_doctorants,name='listeDoctorans'),
    path('demandeSoutenance/',views.demande_soutenance,name='demandeSoutenance'),
    path('etat/',views.etat,name='etat'),
    
    
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)