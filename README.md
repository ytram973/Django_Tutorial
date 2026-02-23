
La racine = dossier où se trouve `manage.py`.

```bash
cd chemin/vers/ton_projet

# Créer l'environnement virtuel 
python -m venv venv

# Activer le venv
venv\Scripts\activate

# Lancer le serveur Django
python manage.py runserver

# Ouvrir le shell Django
python manage.py shell

# Migrations (quand tu modifies les models)
# Créer les migrations :
python manage.py makemigrations


# Appliquer les migrations :
python manage.py migrate