"""
Seed a rich, coherent demo dataset so every space of the platform is populated
and every feature is visible to a portfolio visitor.

Usage:  python manage.py seed_demo
Safe to re-run: it wipes the demo data first, then rebuilds it.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from pages.models import (
    Doctorant, inscription, reinscription, Passage,
    edition_pv, situation_doctorant, Soutenance,
)
from encadreur.models import Encadreur
from cfd.models import login_cfd, ApplicationSettings
from doyen.models import login_doyen


ENCADREURS = [
    "Pr. BOUAMRANE Karim",
    "Pr. BELALEM Ghalem",
    "Pr. MERAD Boudia Mohammed",
    "Pr. HADJILA Fethi",
    "Pr. BENSLIMANE Sidi Mohammed",
]

# (nom, prenom, annee, titre, encadreur_idx, co_encadreur)
DOCTORANTS = [
    ("BENALI", "Yacine", 1, "Détection d'anomalies dans les réseaux IoT par apprentissage profond", 0, "Dr. ZAHAF Amine"),
    ("KHELIFI", "Amina", 1, "Systèmes de recommandation équitables pour le e-learning", 0, "Dr. SAÏDI Nadia"),
    ("MEZIANE", "Sofiane", 2, "Ordonnancement énergétiquement efficace dans le cloud computing", 0, "Dr. LARBI Karim"),
    ("BOUDJEMAA", "Lila", 2, "Traitement automatique de la langue arabe dialectale", 0, ""),
    ("HAMDANI", "Rachid", 3, "Sécurité des contrats intelligents sur blockchain", 0, "Dr. TALEB Nassim"),
    ("CHERIF", "Nawel", 1, "Vision par ordinateur pour l'imagerie médicale", 1, "Dr. OUALI Réda"),
    ("SLIMANI", "Bilal", 2, "Optimisation métaheuristique du placement de VNF", 1, ""),
    ("AZZOUZ", "Imene", 3, "Fédération de données pour la santé connectée", 1, "Dr. SAÏDI Nadia"),
    ("DAHMANI", "Walid", 3, "Jumeaux numériques pour la maintenance prédictive", 1, "Dr. TALEB Nassim"),
    ("REMILI", "Sara", 4, "Modèles génératifs pour la synthèse d'images satellites", 1, ""),
    ("GHALEM", "Oussama", 1, "Micro-services résilients et observabilité", 2, "Dr. LARBI Karim"),
    ("TADJER", "Meriem", 2, "Analyse de sentiments multimodale", 2, ""),
    ("BENYAHIA", "Anis", 3, "Réseaux de neurones sur graphes pour la fraude bancaire", 2, "Dr. OUALI Réda"),
    ("FERHAT", "Kenza", 4, "Apprentissage fédéré préservant la vie privée", 2, ""),
    ("MOKRANE", "Riad", 2, "Edge computing pour les villes intelligentes", 3, "Dr. ZAHAF Amine"),
    ("LOUNIS", "Dalila", 3, "Compression de modèles pour l'embarqué", 3, ""),
    ("SAADI", "Hichem", 5, "Ontologies et web sémantique pour l'agriculture", 3, "Dr. TALEB Nassim"),
    ("ZIANE", "Farida", 4, "Détection de deepfakes par analyse fréquentielle", 4, "Dr. SAÏDI Nadia"),
]

YEAR_LABEL = {"2019/2020", "2020/2021", "2021/2022", "2022/2023", "2023/2024"}


class Command(BaseCommand):
    help = "Peuple la base avec un jeu de données de démonstration complet."

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Nettoyage des données existantes…")
        Soutenance.objects.all().delete()
        Passage.objects.all().delete()
        edition_pv.objects.all().delete()
        situation_doctorant.objects.all().delete()
        inscription.objects.all().delete()
        reinscription.objects.all().delete()
        Doctorant.objects.all().delete()
        Encadreur.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # --- Encadreurs ---
        encadreurs = []
        for i, nom in enumerate(ENCADREURS, start=1):
            u = User.objects.create_user(username=f"ENC-{i:03d}", password="demo")
            enc = Encadreur.objects.create(user=u, nom_prenom=nom, validation=True)
            encadreurs.append(enc)
        self.stdout.write(f"  {len(encadreurs)} encadreurs")

        # --- Doctorants + dossiers ---
        first_dates = ["2019/2020", "2020/2021", "2021/2022", "2022/2023", "2023/2024"]
        n_ins = n_rei = n_pv = n_sit = n_pass = n_sout = 0

        for idx, (nom, prenom, annee, titre, enc_idx, co) in enumerate(DOCTORANTS, start=1):
            num = f"2024-D-{idx:03d}"
            enc = encadreurs[enc_idx]
            user = User.objects.create_user(username=num, password="demo")
            doc = Doctorant.objects.create(
                user=user, validation=True, annee=str(annee), encadreur=enc,
            )
            first_date = first_dates[min(annee, len(first_dates)) - 1]
            mail_pub = f"{prenom.lower()}.{nom.lower()}@gmail.com"
            mail_inst = f"{prenom.lower()}.{nom.lower()}@edu.univ-oran1.dz"

            # Year 1 → inscription; others → reinscription (a couple keep an inscription too)
            if annee == 1:
                inscription.objects.create(
                    doctorant=doc, numero_inscription=num, nom=nom, prenom=prenom,
                    titre_sujet=titre, date_premier_inscription=first_date,
                    nom_encadreur=enc.nom_prenom, nom_co_encadreur=co,
                    mail_public=mail_pub, mail_institutionnel=mail_inst,
                )
                n_ins += 1
            else:
                changed = idx % 5 == 0
                reinscription.objects.create(
                    doctorant=doc, numero_inscription=num, nom=nom, prenom=prenom,
                    titre_sujet=titre, date_premier_inscription=first_date,
                    nom_encadreur=enc.nom_prenom, nom_co_encadreur=co,
                    nouveau_titre_sujet=(titre + " (approche révisée)") if changed else "",
                    nouveau_nom_encadreur="", nouveau_nom_co_encadreur="",
                    mail_public=mail_pub, mail_institutionnel=mail_inst,
                )
                n_rei += 1
                # keep an inscription trace for a few, for richer tables
                if idx % 3 == 0:
                    inscription.objects.create(
                        doctorant=doc, numero_inscription=num, nom=nom, prenom=prenom,
                        titre_sujet=titre, date_premier_inscription=first_date,
                        nom_encadreur=enc.nom_prenom, nom_co_encadreur=co,
                        mail_public=mail_pub, mail_institutionnel=mail_inst,
                    )
                    n_ins += 1

            # Évaluation (PV) for 2nd year and above + a few first years
            if annee >= 2 or idx % 4 == 0:
                pv = edition_pv.objects.create(
                    doctorant=doc,
                    cours_de_spécialité=str(min(12, 6 + idx % 7)),
                    methodologie=str(min(6, 3 + idx % 4)),
                    compétences_anglais=str(min(6, 2 + idx % 5)),
                    communications1="10" if idx % 2 else "12.5",
                    communications2="12.5" if idx % 3 == 0 else "0",
                    publication1="40" if annee >= 2 else "0",
                    publication2="50" if idx % 4 == 0 else "0",
                    publication3="0", publication4="0", publication5="0",
                    tic=str(idx % 3), brevet="1" if idx % 6 == 0 else "0",
                )
                pv.calculate_total()
                n_pv += 1

            # Situation (publications / communications déclarées)
            if idx % 2 == 0:
                situation_doctorant.objects.create(
                    doctorant=doc, nom_prenom=f"{prenom} {nom}",
                    publication=f"https://doi.org/10.1000/demo.{idx:03d}",
                    communication=f"Conférence Internationale IA & Systèmes — Communication n°{idx}",
                )
                n_sit += 1

            # Demandes de passage d'année (mix validé / en attente)
            if annee in (2, 3) and idx % 3 == 0:
                Passage.objects.create(
                    doctorant=doc, passage_annee_validation=(idx % 2 == 0),
                )
                n_pass += 1

            # Soutenances (4e/5e année, mix autorisée / en attente)
            if annee >= 4:
                Soutenance.objects.create(doctorant=doc, action=(idx % 2 == 0))
                n_sout += 1

        # --- Comptes de connexion réels (au cas où DEMO_MODE=False) ---
        login_cfd.objects.all().delete()
        login_cfd.objects.create(username="admin", password="admin")
        login_doyen.objects.all().delete()
        login_doyen.objects.create(username="doyen", password="doyen")

        ApplicationSettings.objects.all().delete()
        ApplicationSettings.objects.create(reinscription_open=True)

        self.stdout.write(self.style.SUCCESS(
            f"OK — {len(DOCTORANTS)} doctorants, {n_ins} inscriptions, {n_rei} réinscriptions, "
            f"{n_pv} PV, {n_sit} situations, {n_pass} passages, {n_sout} soutenances."
        ))
