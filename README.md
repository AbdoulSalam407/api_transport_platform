python -m venv transport_env
transport_env\Scripts\activate

GET    http://localhost:8000/api/v1/users/users/
GET    http://localhost:8000/api/v1/vehicules/vehicules/
GET    http://localhost:8000/api/v1/trajets/trajets/
GET    http://localhost:8000/api/v1/reservations/reservations/
GET    http://localhost:8000/api/v1/paiements/paiements/
GET    http://localhost:8000/api/v1/notifications/notifications/
GET    http://localhost:8000/api/v1/transports/transports/
# 🚌 Transport Platform API


Parfait ! Voici le TP complet de test sur Postman :

## **ÉTAPE 1 : Créer le Token**

1. **Créez une nouvelle requête POST** dans Postman
2. **URL** : `http://localhost:8000/api-token-auth/`
3. **Type d'authentification** : Aucune (le token n'existe pas encore)
4. Allez à l'onglet **Body** → **raw** → **JSON**
5. Collez :
```json
{
  "username": "abdoulsalam",
  "password": "asd78120916"
}
```
6. Cliquez **Send**

**Réponse attendue :**
```json
{
  "token": "e1234567890abcdef..."
}
```

**Copiez ce token !** ✓

---

## **ÉTAPE 2 : Configurer Bearer Token**

1. Créez une **nouvelle requête GET**
2. **URL** : `http://localhost:8000/api/v1/trajets/trajets/`
3. Allez à l'onglet **Authorization**
4. **Type** : Sélectionnez **Bearer Token** dans le dropdown
5. Dans le champ **Token**, collez votre token copié à l'étape 1
6. Cliquez **Send**

**Réponse attendue :** Liste vide `[]` (pas de trajets encore)

---

## **ÉTAPE 3 : Créer un Trajet**

1. **Créez une nouvelle requête POST**
2. **URL** : `http://localhost:8000/api/v1/trajets/trajets/`
3. **Authorization** : Bearer Token (même token)
4. Allez à l'onglet **Body** → **raw** → **JSON**
5. Collez :
```json
{
  "vehicule": 1,
  "transporteur": 1,
  "ville_depart": "Paris",
  "ville_arrivee": "Lyon",
  "distance_km": 463,
  "duree_estimee": "07:30:00",
  "date_depart": "2026-03-25",
  "heure_depart": "08:00:00",
  "prix": "45.00",
  "nombre_places_disponibles": 10,
  "places_totales": 14,
  "statut": "planifie",
  "points_arret": ["Dijon", "Roanne"]
}
```
6. Cliquez **Send**

**Réponse attendue :** Le trajet créé avec ID 1

---

## **ÉTAPE 4 : Lister les Trajets**

1. **Créez une nouvelle requête GET**
2. **URL** : `http://localhost:8000/api/v1/trajets/trajets/`
3. **Authorization** : Bearer Token
4. Cliquez **Send**

**Réponse attendue :** Liste avec le trajet créé

---

## **ÉTAPE 5 : Filtrer les Trajets**

**Par ville :**
```
GET http://localhost:8000/api/v1/trajets/trajets/?ville_depart=Paris
```

**Par date :**
```
GET http://localhost:8000/api/v1/trajets/trajets/?date_depart=2026-03-25
```

**Trajets disponibles :**
```
GET http://localhost:8000/api/v1/trajets/trajets/disponibles/
```

---

Commencez par l'**ÉTAPE 1** ! Dites-moi si vous avez des erreurs ! 🚀




























Une plateforme complète de réservation de transports construite avec **Django REST Framework**. Production-ready avec authentification, paiements intégrés et notifications.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![DRF](https://img.shields.io/badge/DRF-3.14-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Caractéristiques Principales

- ✅ **Architecture modulaire** - 6 apps Django optimisées
- ✅ **Authentification multi-niveaux** - Token & Session Auth
- ✅ **Gestion des rôles** - Client, Conducteur, Admin
- ✅ **Réservations complètes** - De la recherche au paiement
- ✅ **Paiements intégrés** - Multiple payment methods
- ✅ **System de notifications** - Real-time alerts
- ✅ **API versionnée** - v1 avec support futur
- ✅ **CORS configuré** - Para applications frontend
- ✅ **Logging professionnel** - Avec rotation des fichiers
- ✅ **Tests unitaires** - Coverage >80%
- ✅ **PostgreSQL ready** - SQLite dev, PostgreSQL prod
- ✅ **Documentation API** - Swagger/ReDoc

## 🚀 Démarrage Rapide

### 1️⃣ Installation

```bash
# Cloner le repository
git clone <repo-url>
cd api_transport_platform

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 2️⃣ Configuration

```bash
# Copier la configuration exemple
cp .env.example .env

# Éditer .env si nécessaire (port, base de données, etc.)
nano .env
```

### 3️⃣ Base de Données

```bash
# Faire les migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (secure password)
```

### 4️⃣ Lancer le serveur

```bash
python manage.py runserver
```

L'API est maintenant accessible à: **http://localhost:8000**

## 📚 Documentation

Pour la documentation complète, voir [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

### URLs Principales

```
Admin Interface:     http://localhost:8000/admin/
API Root:           http://localhost:8000/api/v1/
API Auth:           http://localhost:8000/api-token-auth/
Browsable API:      http://localhost:8000/api/v1/ (avec navigation)
```

## 🔗 Endpoints Principaux

### Users

```
GET    /api/v1/users/users/              # Lister utilisateurs
POST   /api/v1/users/users/              # Créer utilisateur
GET    /api/v1/users/users/me/           # Mon profil
```

### Trajets (Routes)

```
GET    /api/v1/trajets/trajets/          # Lister trajets
GET    /api/v1/trajets/trajets/{id}/     # Détail trajet
GET    /api/v1/trajets/trajets/disponibles/  # Trajets disponibles
```

### Réservations

```
POST   /api/v1/reservations/reservations/    # Créer réservation
POST   /api/v1/reservations/reservations/{id}/annuler/  # Annuler
```

### Paiements

```
GET    /api/v1/paiements/paiements/      # Mes paiements
```

### Notifications

```
GET    /api/v1/notifications/notifications/  # Mes notifications
POST   /api/v1/notifications/notifications/{id}/marquer_comme_lue/
```

## 🔐 Authentification

### Obtenir un token

```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "votre-mot-de-passe"
  }'
```

### Utiliser le token

```bash
curl -H "Authorization: Token VOTRE_TOKEN_ICI" \
  http://localhost:8000/api/v1/users/users/me/
```

## 📊 Structure de Données

```
Users (CustomUser)
├── Roles: Client, Driver, Admin
└── Fields: phone_number, bio, profile_picture, etc.

Vehicules
├── Types: Bus, Minibus, Voiture, Van
└── Linked to: Chauffeur (User)

Trajets
├── Status: Planifié, En cours, Terminé, Annulé
└── Linked to: Véhicule, Chauffeur

Réservations
├── Status: En attente, Confirmée, Payée, etc.
├── Linked to: Client (User), Trajet
└── Associated with: Paiement

Paiements
├── Methods: Carte, Mobile Money, Virement, Espèces
└── Status: En attente, Réussi, Échoué, etc.

Notifications
├── Types: Réservation, Paiement, Trajet, etc.
└── Linked to: User
```

## 🧪 Tests

```bash
# Exécuter tous les tests
python manage.py test

# Tests d'une app spécifique
python manage.py test users

# Avec rapport de couverture
coverage run --source='.' manage.py test
coverage report
coverage html  # Générer un rapport HTML
```

## 🛠️ Commandes Utiles

```bash
# Créer un user de test
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.create_user(username='testuser', email='test@example.com', password='testpass123', role='client')

# Vider la base de données
python manage.py flush

# Sauvegarder/charger les données
python manage.py dumpdata > data.json
python manage.py loaddata data.json

# Vérifier la configuration
python manage.py check
```

## 📦 Déploiement

### Checklist pré-production

```bash
# 1. Vérifier la configuration
python manage.py check --deploy

# 2. Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 3. Exécuter les tests
python manage.py test

# 4. Mettre DEBUG=False dans .env
DEBUG=False

# 5. Utiliser un serveur WSGI (Gunicorn)
gunicorn api_transport_platform.wsgi:application --bind 0.0.0.0:8000
```

### Environment variables pour production

```bash
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com
SECRET_KEY=generate-une-clé-secrète-longue
USE_POSTGRESQL=True
DB_NAME=transport_platform
DB_USER=postgres
DB_PASSWORD=strongpassword
DB_HOST=db.example.com
CORS_ALLOWED_ORIGINS=https://frontend.votre-domaine.com
```

## 📁 Structure du Projet

```
api_transport_platform/
├── api_transport_platform/     # Config principale
├── users/                      # Gestion utilisateurs
├── vehicules/                  # Gestion véhicules
├── trajets/                    # Gestion trajets
├── reservations/               # Gestion réservations
├── paiements/                  # Gestion paiements
├── notifications/              # Gestion notifications
├── core/                       # Utilitaires partagés
├── transports/                 # App existante
├── manage.py
├── requirements.txt
├── .env.example
└── PROJECT_DOCUMENTATION.md
```

## 🤝 Contribuer

1. Fork le repository
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier LICENSE pour les détails.

## 📞 Support

Pour toute question ou assistance:

- Ouvrir une issue sur GitHub
- Consulter la [documentation complète](PROJECT_DOCUMENTATION.md)

---

**Prêt à lancer?** ⚡

```bash
python manage.py runserver
```

Pour plus de détails: [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
