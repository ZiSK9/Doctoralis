from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('',views.index,name='index'),
    path('loginDoctorant/',views.doctorantlogin,name='loginDoctorant'),
    path('indexDoctorant/',views.index_doctorant,name='indexDoctorant'),
    path('inscription/',views.inscriptions,name='inscription'),
    path('reinscription/',views.reinscription_doctorat,name='reinscription'),
    path('changement/',views.changement,name='changement'),
    path('etat_d`avencement/',views.etat_avencement,name='etat_d`avencement'),
    path('point/', views.test_points, name='point'),
    path('testPoint/', views.test_points, name='testPoint'),
    path('demandeCompte/', views.demande_compte, name='demandeCompte'),
    path('passage_annee/', views.passage_annee, name='passage_annee'),
    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)