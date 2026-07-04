from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from encadreur.models import Encadreur





# Create your models here.


class Doctorant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fichier_inscription = models.FileField(upload_to='ficher_inscription/%Y', default=None, null=True)
    validation = models.BooleanField(default=False) 
    annee = models.CharField(max_length=100)
    encadreur = models.ForeignKey(Encadreur, on_delete=models.CASCADE, related_name='doctorants' ,null=True)
    # Add any additional fields specific to the doctorant model
    def __str__(self):
        return self.user.username


class Passage(models.Model):
    doctorant = models.ForeignKey(Doctorant, on_delete=models.CASCADE, related_name='passage' ,null=True)
    passage_annee_validation = models.BooleanField(default=False)
    fichier_reinscription_passage = models.FileField(upload_to='ficher_inscription/%Y', default=None, null=True)
    
class inscription(models.Model):

    doctorant = models.ForeignKey(Doctorant, on_delete=models.CASCADE, related_name='inscription' ,null=True)
    numero_inscription = models.CharField(max_length=50, null=True)
    nom = models.CharField(max_length=100, null=True)
    prenom = models.CharField(max_length=100, null=True)
    titre_sujet = models.CharField(max_length=200, null=True)
    date_premier_inscription = models.CharField(max_length=50, null=True)
    nom_encadreur = models.CharField(max_length=100, null=True)
    nom_co_encadreur = models.CharField(max_length=100, null=True)
    mail_public = models.CharField(max_length=100, null=True)
    mail_institutionnel = models.CharField(max_length=100, null=True)
    fichier_inscription = models.FileField(upload_to='ficher_inscription/%Y', default=None, null=True)
    
    def __str__(self):
        return self.nom    
    
class reinscription(models.Model):
    doctorant = models.ForeignKey(Doctorant, on_delete=models.CASCADE, related_name='reinscription' ,null=True)
    numero_inscription = models.CharField(max_length=50, null=True)
    nom = models.CharField(max_length=100, null=True)
    prenom = models.CharField(max_length=100, null=True)
    titre_sujet = models.CharField(max_length=200, null=True)
    nouveau_titre_sujet = models.CharField(max_length=200, null=True)
    date_premier_inscription = models.CharField(max_length=50, null=True)
    nom_encadreur = models.CharField(max_length=100, null=True)
    nom_co_encadreur = models.CharField(max_length=100, null=True)
    nouveau_nom_encadreur = models.CharField(max_length=100, null=True)
    nouveau_nom_co_encadreur = models.CharField(max_length=100, null=True)
    mail_public = models.CharField(max_length=100, null=True)
    mail_institutionnel = models.CharField(max_length=100, null=True)
    fichier_inscription = models.FileField(upload_to='ficher_inscription/%Y', default=None, null=True)
    pv_csd = models.FileField(upload_to='ficher_inscription/%Y', default=None, null=True)
    
    def __str__(self):
        return self.nom

class edition_pv(models.Model):
    doctorant = models.ForeignKey(Doctorant, on_delete=models.CASCADE, related_name='edition' ,null=True)
    cours_de_spécialité = models.CharField(max_length=50, null=True)
    methodologie = models.CharField(max_length=50, null=True)
    compétences_anglais = models.CharField(max_length=50, null=True)
    communications1 = models.CharField(max_length=50, null=True)
    communications2 = models.CharField(max_length=50, null=True)
    publication1 = models.CharField(max_length=50, null=True)
    publication2 = models.CharField(max_length=50, null=True)
    publication3 = models.CharField(max_length=50, null=True)
    publication4 = models.CharField(max_length=50, null=True)
    publication5 = models.CharField(max_length=50, null=True)
    tic = models.CharField(max_length=50, null=True)
    brevet = models.CharField(max_length=50, null=True)
    total = models.CharField(max_length=50, null=True)

    

    def calculate_total(self):
        # Convert the relevant fields to integers and calculate the total
        fields = [
        self.cours_de_spécialité,
        self.methodologie,
        self.compétences_anglais,
        self.communications1,
        self.communications2,
        self.publication1,
        self.publication2,
        self.publication3,
        self.publication4,
        self.publication5,
        self.tic,
        self.brevet,
        ]
        total = sum(float(field) for field in fields if field and (field.isdigit() or field.replace('.', '', 1).isdigit()))
        self.total = str(total)  # Store the total as a string in the 'total' field
        self.save()  


    

class situation_doctorant(models.Model):
    doctorant = models.ForeignKey(Doctorant, on_delete=models.CASCADE, related_name='situation_doctorant' ,null=True)
    nom_prenom = models.CharField(max_length=100,null=True)
    publication = models.CharField(max_length=100,null=True)    
    communication = models.CharField(max_length=100,null=True)  
    
    

class Soutenance(models.Model):
    doctorant = models.ForeignKey(Doctorant, on_delete=models.CASCADE, related_name='soutenance' ,null=True)
    csd_csf = models.FileField(upload_to='ficher_soutenance/%Y', default=None, null=True)
    autorisation_soutenance = models.FileField(upload_to='ficher_soutenance/%Y', default=None, null=True)
    pv_soutenance = models.FileField(upload_to='ficher_soutenance/%Y', default=None, null=True) 
    action = models.BooleanField(default=False)  
   

    


