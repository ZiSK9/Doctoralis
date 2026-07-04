from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('loginDoyen/',views.doyen_login,name='loginDoyen'),
    path('dashboards/',views.dashboards,name='dashboards'),
    path('indexDoyen/',views.index_doyen,name='indexDoyen'),
    path('liste_inscription_doyen/',views.liste_inscription_doyen,name='liste_inscription_doyen'),
    path('liste_reinscription_doyen/',views.liste_reinscription_doyen,name='liste_reinscription_doyen'),
    path('etat_avencement_doyen/',views.etat_Avencement_doyen,name='etat_avencement_doyen'),
    path('editionPVdoyen/',views.editionPVdoyen,name='editionPVdoyen'),
    path('soutenanceDoyen/',views.soutenances,name='soutenanceDoyen'),

    
    
    
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)