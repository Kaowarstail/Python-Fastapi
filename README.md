# M1-CTO TP: Gestion des Étudiants avec FastAPI

Ce projet est une application FastAPI conçue pour gérer les informations des étudiants et leurs notes. Il permet de créer, récupérer, et supprimer des étudiants et leurs notes via une API RESTful. L'utilisation d'un fichier JSON comme base de données simplifie le stockage et la manipulation des données sans nécessiter une base de données relationnelle ou NoSQL complexe. Cela rend le projet plus accessible et facile à configurer pour des fins éducatives ou de petits projets.

## Fonctionnalités

- **Création d'étudiants** : Permet d'ajouter un nouvel étudiant avec ses informations personnelles et ses notes.
- **Récupération d'étudiants** : Permet de récupérer les informations d'un étudiant spécifique par son identifiant.
- **Suppression d'étudiants** : Permet de supprimer un étudiant de la base de données.
- **Gestion des notes** : Permet d'ajouter, récupérer et supprimer les notes d'un étudiant.
- **Exportation des données** : Supporte l'exportation des données des étudiants en format JSON ou CSV.

## Technologies Utilisées

- FastAPI : Un framework web moderne et rapide pour construire des APIs avec Python 3.7+.
- Pydantic : Utilisé pour la validation des données et la gestion des modèles.
- Uvicorn : Un serveur ASGI léger pour exécuter l'application FastAPI.
- JSON : Utilisé comme format de stockage de données pour sa simplicité et sa facilité d'utilisation avec Python.

## Installation

1. Clonez ce dépôt :

```bash
git clone <url_du_dépôt>
```

2. Créez un environnement virtuel :

```bash
python -m venv venv
```

3. Activez l'environnement virtuel :

- Sur Windows :

```bash
.\venv\Scripts\activate
```

- Sur Unix ou MacOS :

```bash
source venv/bin/activate
```

4. Installez les dépendances nécessaires :

```bash
pip install fastapi uvicorn
```

## Démarrage

Pour démarrer le serveur, exécutez la commande suivante :

```bash
uvicorn main:app --reload
```

Le serveur sera accessible à l'adresse `http://127.0.0.1:8000`.

## Utilisation

Vous pouvez interagir avec l'API via l'interface de documentation automatique générée par FastAPI en accédant à `http://127.0.0.1:8000/docs`.

### Endpoints

- `GET /` : Accueil, retourne un message de bienvenue.
- `POST /student/` : Crée un nouvel étudiant.
- `GET /student/{student_id}` : Récupère les informations d'un étudiant spécifique.
- `DELETE /student/{student_id}` : Supprime un étudiant.
- `GET /student/{student_id}/grades/{grade_id}` : Récupère une note spécifique d'un étudiant.
- `DELETE /student/{student_id}/grades/{grade_id}` : Supprime une note spécifique d'un étudiant.
- `GET /export` : Exporte les données des étudiants en format JSON ou CSV.