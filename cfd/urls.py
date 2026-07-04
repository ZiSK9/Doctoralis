from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('loginCFD/',views.login_CFD,name='loginCFD'),
    path('indexCFD/',views.indexCFD,name='indexCFD'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('controlReinscription/',views.control_reinscription,name='controlReinscription'),
    path('editionPV/',views.edition_PV,name='editionPV'),
    path('demandesComptes/',views.demandes_comptes,name='demandesComptes'),
    path('etatDavencement/',views.etat_Avencement,name='etatDavencement'),
    path('listeReinscription/',views.liste_reinscription,name='listeReinscription'),
    path('listeinscription/',views.liste_inscription,name='listeinscription'),
    path('ajouterEncadreur/',views.ajouterEncadreur,name='ajouterEncadreur'),
    path('edition_PV_2/',views.edition_PV_2,name='edition_PV_2'),
    path('demandesSoutenances/',views.demandes_soutenances,name='demandesSoutenances'),
    path('demandesPassage/',views.passages_annees,name='demandesPassage'),




    
    
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)