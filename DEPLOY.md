# 🚀 Déployer Doctoralis sur Render (gratuit)

Ce projet est prêt pour un déploiement gratuit sur **Render**, avec un **mode démo**
qui laisse les visiteurs explorer tous les espaces sans mot de passe.

---

## 1. Mettre le projet sur GitHub

Le projet n'est pas encore un dépôt Git. Depuis le dossier du projet :

```bash
git init
git add .
git commit -m "Doctoralis — plateforme de suivi doctoral"
```

Crée un dépôt vide sur GitHub (ex. `doctoralis`), puis :

```bash
git branch -M main
git remote add origin https://github.com/<ton-user>/doctoralis.git
git push -u origin main
```

> `db.sqlite3` et `media/` sont **volontairement versionnés** : la démo repart
> toujours avec des données. `staticfiles/` et `__pycache__/` sont ignorés.

---

## 2. Créer le service sur Render

1. Va sur **https://render.com** → connecte-toi avec GitHub (gratuit).
2. **New +** → **Web Service** → sélectionne ton dépôt `doctoralis`.
3. Render détecte le fichier **`render.yaml`** (Blueprint) : accepte-le.
   Il configure automatiquement :
   - Build : `bash build.sh` (installe, `collectstatic`, `migrate`)
   - Start : `gunicorn postgraduation.wsgi:application`
   - Variables : `SECRET_KEY` (généré), `DEBUG=False`, `DEMO_MODE=True`, `PYTHON_VERSION=3.12.7`
4. Plan : **Free**. Clique **Create Web Service**.

⏱️ Le premier build prend 2–4 min. Ton URL sera du type
`https://doctoralis.onrender.com`.

### Configuration manuelle (si tu ne passes pas par le Blueprint)

| Champ | Valeur |
|---|---|
| Build Command | `bash build.sh` |
| Start Command | `gunicorn postgraduation.wsgi:application` |
| Environment | `Python 3` |

Variables d'environnement à ajouter :

| Clé | Valeur |
|---|---|
| `SECRET_KEY` | *(une longue chaîne aléatoire)* |
| `DEBUG` | `False` |
| `DEMO_MODE` | `True` |
| `PYTHON_VERSION` | `3.12.7` |

---

## 3. C'est en ligne 🎉

- **Page d'accueil** : `https://doctoralis.onrender.com`
- Un bandeau **« DÉMO — accès libre »** s'affiche.
- Menu **Se connecter** → chaque espace est accessible **sans mot de passe**
  (le mode démo connecte automatiquement un utilisateur de démonstration).
- Les 4 espaces (Doctorant, Encadreur, CFD, Vice-Doyen), les tableaux de bord
  analytiques et les graphiques restent **100 % dynamiques**.

---

## Notes importantes

- **Mise en veille** : sur le plan gratuit, le service s'endort après 15 min
  d'inactivité. La 1re visite après une pause prend ~50 s (le temps du réveil).
  Pour ton portfolio, mets un mot : *« Le chargement initial peut prendre
  quelques secondes (hébergement gratuit). »*
- **Données** : le disque est éphémère. Toute donnée créée pendant la démo est
  remise à zéro à chaque redéploiement — c'est voulu : la démo reste toujours propre.
- **Sécurité** : `DEBUG=False`, HTTPS forcé, cookies sécurisés, HSTS activés en
  production. L'admin Django (`/admin`) n'a aucun super-utilisateur → inaccessible.
- **Repasser en mode normal** (auth réelle) : mets `DEMO_MODE=False` dans les
  variables d'environnement Render.

---

## Alternative gratuite : PythonAnywhere

Si tu préfères que les **données persistent** (pas de remise à zéro) :
héberge sur **pythonanywhere.com** (SQLite persistant, pas de mise en veille).
Déploiement manuel : upload du code, virtualenv, configuration du fichier WSGI
pointant sur `postgraduation.wsgi`, et `Static files` mappé sur `/static/ → staticfiles/`.
