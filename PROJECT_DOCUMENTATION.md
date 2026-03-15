# 🚀 Transport Platform API - Documentation Complète

## 📋 Vue d'ensemble

**Transport Platform API** est une plateforme complète de réservation de transports construite avec Django REST Framework. Le projet offre une architecture modulaire, production-ready avec authentification, paiements et notifications.

## 🏗️ Architecture du Projet

```
api_transport_platform/
├── api_transport_platform/        # Configuration principale du projet
│   ├── settings.py               # Configuration Django & DRF
│   ├── urls.py                   # URLs principales & routing API
│   ├── wsgi.py
│   ├── asgi.py
│   └── __init__.py
│
├── core/                         # Utilitaires & configuration partagée
│   ├── permissions.py            # Permissions personnalisées
│   ├── pagination.py             # Paginateurs
│   ├── exceptions.py             # Gestion d'erreurs
│   ├── utils.py                  # Helpers & utilitaires
│   └── __init__.py
│
├── users/                        # App Gestion des utilisateurs
│   ├── models.py                 # CustomUser avec rôles
│   ├── serializers.py            # Serializers utilisateur
│   ├── views.py                  # ViewSets & endpoints
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── vehicules/                    # App Gestion des véhicules
│   ├── models.py                 # Modèle Vehicule
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── trajets/                      # App Gestion des trajets
│   ├── models.py                 # Modèle Trajet
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── reservations/                 # App Gestion des réservations
│   ├── models.py                 # Modèle Reservation
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── paiements/                    # App Gestion des paiements
│   ├── models.py                 # Modèle Paiement
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── notifications/                # App Gestion des notifications
│   ├── models.py                 # Modèle Notification
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── transports/                   # App existante de transports
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   └── tests.py
│
├── manage.py
├── .env.example                  # Variables d'environnement
├── .gitignore
├── requirements.txt              # Dépendances Python
├── README.md                     # Ce fichier
└── db.sqlite3                    # Base de données (dev)
```

## 🎯 Modèles de Données

### 1. **CustomUser** (users.models)

- Modèle utilisateur personnalisé avec rôles
- Rôles: `client`, `driver`, `admin`
- Champs: phone_number, role, profile_picture, bio, is_verified

### 2. **Vehicule** (vehicules.models)

- Représente un véhicule de transport
- Types: Bus, Minibus, Voiture, Van
- Statuts: Disponible, En trajet, Maintenance, Inactif
- Champs: marque, modèle, plaque, capacité, assurance, etc.

### 3. **Trajet** (trajets.models)

- Représente un trajet planifié
- Statuts: Planifié, En cours, Terminé, Annulé
- Champs: départ, arrivée, distance, durée, prix, places disponibles

### 4. **Reservation** (reservations.models)

- Représente une réservation de place
- Statuts: En attente, Confirmée, Payée, En cours, Terminée, Annulée
- Lien: Client + Trajet

### 5. **Paiement** (paiements.models)

- Représente une transaction de paiement
- Méthodes: Carte bancaire, Mobile Money, Virement, Espèces
- Statuts: En attente, Traitement, Réussi, Échoué, Remboursé

### 6. **Notification** (notifications.models)

- Représente une notification utilisateur
- Types: Réservation, Paiement, Trajet, Annulation, Alerte, Info
- Champs: titre, message, lien, is_read

## 🔌 Endpoints API

### Base URL: `http://localhost:8000/api/v1/`

### Authentication Endpoints

```
POST   /api-token-auth/                 # Obtenir un token
GET    /api-auth/                       # Auth browsable API
```

### Users

```
GET    /users/users/                    # Lister les utilisateurs
POST   /users/users/                    # Créer un utilisateur
GET    /users/users/{id}/               # Détail utilisateur
PUT    /users/users/{id}/               # Modifier utilisateur
DELETE /users/users/{id}/               # Supprimer utilisateur
GET    /users/users/me/                 # Mon profil
POST   /users/users/change_password/    # Changer mot de passe
```

### Vehicles

```
GET    /vehicules/vehicules/            # Lister
POST   /vehicules/vehicules/            # Créer
GET    /vehicules/vehicules/{id}/       # Détail
PUT    /vehicules/vehicules/{id}/       # Modifier
DELETE /vehicules/vehicules/{id}/       # Supprimer
```

### Routes/Trajets

```
GET    /trajets/trajets/                # Lister tous
POST   /trajets/trajets/                # Créer
GET    /trajets/trajets/{id}/           # Détail
GET    /trajets/trajets/disponibles/    # Trajets disponibles uniquement
```

### Reservations

```
GET    /reservations/reservations/      # Mes réservations
POST   /reservations/reservations/      # Créer réservation
GET    /reservations/reservations/{id}/ # Détail
POST   /reservations/reservations/{id}/annuler/  # Annuler
```

### Payments

```
GET    /paiements/paiements/            # Mes paiements (lecture seule)
GET    /paiements/paiements/{id}/       # Détail paiement
```

### Notifications

```
GET    /notifications/notifications/    # Mes notifications
POST   /notifications/notifications/{id}/marquer_comme_lue/    # Marquer lue
POST   /notifications/notifications/marquer_tous_comme_lus/    # Marquer tous
GET    /notifications/notifications/non_lues/                   # Non lues seulement
```

## 🔐 Authentification & Permissions

### Types d'Authentification

1. **Session Authentication** - Pour le browsable API
2. **Token Authentication** - Pour les applications mobiles/SPA

### Permissions Personnalisées

- `IsAdminOrReadOnly` - Admin modifie, autres lisent
- `IsOwnerOrReadOnly` - Propriétaire modifie, autres lisent
- `IsClient` - Utilisateur doit être client
- `IsDriver` - Utilisateur doit être conducteur

## 📦 Installation & Configuration

### Prérequis

- Python 3.9+
- pip
- PostgreSQL (optionnel, SQLite par défaut)

### 1. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 2. Configuration des variables d'environnement

```bash
cp .env.example .env
# Éditer .env avec vos valeurs
```

### 3. Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Créer un superutilisateur

```bash
python manage.py createsuperuser
```

### 5. Lancer le serveur

```bash
python manage.py runserver
```

L'API sera disponible sur `http://localhost:8000/api/v1/`

## 🗄️ Configuration Base de Données

### SQLite (Développement - défaut)

```
USE_POSTGRESQL=False
```

### PostgreSQL (Production)

```bash
# Installer PostgreSQL et créer une base de données
createdb transport_platform

# Variables d'environnement
USE_POSTGRESQL=True
DB_NAME=transport_platform
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```

## 🧪 Tests

```bash
# Exécuter tous les tests
python manage.py test

# Tests d'une app spécifique
python manage.py test users

# Avec couverture
coverage run --source='.' manage.py test
coverage report
```

## 📊 Filtering, Search & Ordering

### Filtering

```
GET /trajets/trajets/?status=planifie&depart=Paris
```

### Search

```
GET /vehicules/vehicules/?search=Toyota
```

### Ordering

```
GET /trajets/trajets/?ordering=-date_depart
```

### Pagination

```
GET /users/users/?page=2&page_size=50
```

## 🔄 Workflow Réservation Typique

1. **Client cherche des trajets**

   ```
   GET /api/v1/trajets/trajets/?depart=Paris&arrivee=Lyon
   ```

2. **Client crée une réservation**

   ```
   POST /api/v1/reservations/reservations/
   {
     "trajet": 1,
     "nombre_places": 2,
     "prix_total": 50.00
   }
   ```

3. **Système crée un paiement**

   ```
   POST /api/v1/paiements/paiements/
   {
     "reservation": 1,
     "montant": 50.00,
     "methode_paiement": "carte_bancaire"
   }
   ```

4. **Après paiement réussi**
   - Reservation status → "payee"
   - Trajet.places_disponibles décrément
   - Notification envoyée au client

5. **Au départ du trajet**
   - Trajet status → "en_cours"
   - Notifications aux passagers

6. **Après arrivée**
   - Trajet status → "termine"
   - Reservation status → "terminee"

## 🚀 Bonnes Pratiques Implémentées

✅ **Architecture modulaire** - Apps découplées & réutilisables
✅ **DRY Principle** - Core pour permissions, paginateurs, exceptions
✅ **Validation robuste** - Serializers avec validation métier
✅ **Permissions granulaires** - Basées sur les rôles
✅ **Pagination configurée** - Pour les grandes listes
✅ **Filtering & Search** - Sur les endpoints appropriés
✅ **Logging structuré** - Configuration production-ready
✅ **CORS configuré** - Pour les requêtes cross-origin
✅ **Rate limiting** - Throttling d'API
✅ **Exception handling** - Réponses d'erreur cohérentes
✅ **Indexes DB** - Sur les champs fréquemment interrogés

## 📈 Déploiement

### Verifications pré-production

```bash
# Checker la configuration Django
python manage.py check --deploy

# Collecter les fichiers statiques
python manage.py collectstatic

# Charger les fixtures (données initiales)
python manage.py loaddata fixture_name
```

### Serveurs recommandés

- **Gunicorn** - Serveur WSGI
- **Nginx** - Reverse proxy
- **Supervisor** - Process management
- **PostgreSQL** - Base de données

### Variables d'environnement production

```
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
SECRET_KEY=generez-une-vraie-clé-secrète
USE_POSTGRESQL=True
CORS_ALLOWED_ORIGINS=https://votre-domaine.com
```

## 📚 Ressources Additionnelles

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Postman](https://www.postman.com/) - Test API

## 📞 Support & Contribuer

Pour toute question ou amélioration, veuillez ouvrir une issue ou un pull request.

---

**Version:** 1.0.0  
**Dernière mise à jour:** March 2026  
**Status:** Production-Ready ✅
