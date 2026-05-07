# 🚀 QUICK START - DÉMARRAGE EN 5 MINUTES

## ⚡ Checklist de Démarrage Rapide

### ✅ Step 1: Installation (2 min)

```bash
# 1. Aller dans le dossier projet
cd api_transport_platform

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Linux/Mac:
source venv/bin/activate
# ou Windows:
venv\Scripts\activate

# 4. Installer les dépendances essentielles
pip install Django==6.0.3 djangorestframework==3.14.0 django-filter corsheaders
```

### ✅ Step 2: Configuration (1 min)

```bash
# Créer le fichier .env (optional pour dev)
cp .env.example .env

# La configuration par défaut (SQLite) fonctionne directement!
```

### ✅ Step 3: Base de Données (1 min)

```bash
# Créer les tables
python manage.py makemigrations
python manage.py migrate

# ✅ Voilà! Base de données prête
```

### ✅ Step 4: Admin (1 min)

```bash
# Créer l'utilisateur admin
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (entrer un mot de passe)
```

### ✅ Step 5: Démarrer le serveur (0 min)

```bash
# Lancer le serveur
python manage.py runserver

# ✨ L'API est maintenant disponible!
```

## 🔗 URLs Disponibles Immédiatement

### Après démarrage du serveur:

| URL                                     | Description               |
| --------------------------------------- | ------------------------- |
| `http://localhost:8000/admin/`          | 🔐 Admin Django           |
| `http://localhost:8000/api/v1/`         | 📡 API Root (browsable)   |
| `http://localhost:8000/api-token-auth/` | 🔑 Authentification Token |

## 🧪 Test Immédiat de l'API

### 1. Obtenir un Token

```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "votre-password"}'

# Réponse:
# {"token": "abc123def456..."}
```

### 2. Utiliser le Token

```bash
# Récupérer votre profil
curl -H "Authorization: Token abc123def456" \
  http://localhost:8000/api/v1/users/users/me/

# ou dans les headers Postman:
# Authorization: Token abc123def456
```

### 3. Parcourir l'API

```
http://localhost:8000/api/v1/
```

L'API est auto-documentée via le browsable API de DRF!

## 📊 Endpoints Disponibles Dans le Projet

```
📍 Users
   GET    /api/v1/users/users/
   POST   /api/v1/users/users/
   GET    /api/v1/users/users/me/
   POST   /api/v1/users/users/change_password/

📍 Vehicules
   GET    /api/v1/vehicules/vehicules/
   POST   /api/v1/vehicules/vehicules/
   GET    /api/v1/vehicules/vehicules/{id}/

📍 Trajets
   GET    /api/v1/trajets/trajets/
   GET    /api/v1/trajets/trajets/disponibles/
   POST   /api/v1/trajets/trajets/

📍 Reservations
   GET    /api/v1/reservations/reservations/
   POST   /api/v1/reservations/reservations/
   POST   /api/v1/reservations/reservations/{id}/annuler/

📍 Paiements
   GET    /api/v1/paiements/paiements/

📍 Notifications
   GET    /api/v1/notifications/notifications/
   POST   /api/v1/notifications/notifications/{id}/marquer_comme_lue/
```

## 🎯 Cas d'Usage - Flow Complet

### Scenario: Réserver un trajet Paris → Lyon

**1. Login & Get Token**

```bash
curl -X POST http://localhost:8000/api-token-auth/ \
  -d '{"username": "admin", "password": "admin"}'
```

**2. List Available Routes**

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  "http://localhost:8000/api/v1/trajets/trajets/disponibles/"
```

**3. Create Reservation** (if needed, create trajet first)

```bash
curl -X POST http://localhost:8000/api/v1/reservations/reservations/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "trajet": 1,
    "nombre_places": 2,
    "prix_total": 50.00
  }'
```

**4. View My Reservations**

```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/v1/reservations/reservations/
```

## 🛠️ Commandes Utiles

```bash
# Voir TOUS les users
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.all()

# Créer un test user
>>> User.objects.create_user(
>>>   username='testuser',
>>>   email='test@example.com',
>>>   password='testpass123',
>>>   role='client'
>>> )

# Voir les trajectoires
>>> from trajets.models import Trajet
>>> Trajet.objects.all()

# Exécuter un test
python manage.py test users

# Vérifier configuration Django
python manage.py check
```

## 📝 Structure Fichiers Importants

```
api_transport_platform/
├── manage.py                    ← Point d'entrée
├── db.sqlite3                   ← DB (créée auto)
├── settings.py                  ← Configuration MAIN
├── urls.py                      ← Routes API
├── requirements.txt             ← Dépendances
├── .env.example                 ← Variables d'env
├── README.md                    ← Quick start
├── PROJECT_DOCUMENTATION.md     ← Full docs
└── [apps]/                      ← Chaque app Django
    ├── models.py               ← Données
    ├── serializers.py          ← API payload
    ├── views.py                ← Endpoints logic
    └── urls.py                 ← Routes app
```

## 🔐 First Time Troubleshooting

### ❌ Erreur: "No module named 'django'"

```bash
# Solution: Installer Django
pip install django==6.0.3
```

### ❌ Erreur: "ModuleNotFoundError: No module named 'rest_framework'"

```bash
# Solution: Installer DRF
pip install djangorestframework==3.14.0
```

### ❌ Erreur: "django has no attribute 'setup'"

```bash
# Solution: La commande est correcte, vérifier env virtuel activé
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### ❌ Erreur "port already in use"

```bash
# Solution: Utiliser un autre port
python manage.py runserver 8001
```

## 💡 Tips & Tricks

### 🎯 Browsable API (super pratique!)

- Aller sur `http://localhost:8000/api/v1/`
- Saisir les credentials
- Tester les endpoints directement
- Voir les réponses formatées

### 🔑 Token Authentication

- À conserver précieusement
- À envoyer dans header: `Authorization: Token abc123`
- Valable tant que pas supprimé

### 📱 Postman Setup

1. Créer une environment "dev"
2. Variable: `token` = value du token
3. Auth header: `Authorization: Token {{token}}`
4. Sauvegarder les requests pour réutilisation

### 🚀 Productivité

```bash
# Watch for changes (si nodemon installé)
watch -n 2 python manage.py runserver

# Test rapide pendant dev
python manage.py test --keepdb

# Format code automatiquement
black .
```

## 📚 Documentation Interne

Tous les fichiers à lire (par priorité):

1. **Urgent**
   - README.md (vous êtes ici!)
   - QUICK_START.md (ce fichier)

2. **Important**
   - PROJECT_DOCUMENTATION.md (40+ pages)
   - PROJET_RESUME.md (architecture)

3. **Référence**
   - MIGRATION_SUMMARY.md
   - CARTE_1_GUIDE.md

## 🎓 Prochaines Étapes

### Niveau 1 - Découverte (Jour 1)

- [ ] Lancer le serveur
- [ ] S'authentifier
- [ ] Explorer les endpoints
- [ ] Lire README.md

### Niveau 2 - Utilisation (Jour 2-3)

- [ ] Créer des données de test
- [ ] Faire requêtes API complètes
- [ ] Comprendre flow réservation
- [ ] Lire PROJECT_DOCUMENTATION.md

### Niveau 3 - Développement (Semaine 1)

- [ ] Lire le code des models
- [ ] Ajouter un endpoint custom
- [ ] Écrire des tests
- [ ] Deployer en local

### Niveau 4 - Production (Semaine 2+)

- [ ] Setup PostgreSQL
- [ ] Setup Gunicorn
- [ ] Setup Nginx
- [ ] Deploy sur serveur

## ✨ Bon à Savoir

### Ce qui fonctionne MAINTENANT

✅ Toute l'API REST  
✅ Authentification Token  
✅ Permissions par rôle  
✅ Admin interface  
✅ Filtrage & Search  
✅ Pagination

### Ce qui est PRÊT pour ajout

⏳ WebSockets (django-channels)  
⏳ JWT Auth (simplejwt)  
⏳ Stripe Payments  
⏳ SMS Notifications  
⏳ Email Templates

### À Customiser

🎨 Admin interface  
🎨 Serializers pour ajouter champs  
🎨 Permissions additionnelles  
🎨 Validations métier

---

## 🎉 You're All Set!

```bash
# Juste une commande pour démarrer:
python manage.py runserver

# Et aller à:
http://localhost:8000/api/v1/
```

**Bon développement!** 🚀

For more details: See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
