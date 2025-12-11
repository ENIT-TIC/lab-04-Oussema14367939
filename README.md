[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/R2PmiUNr)

# 📚 Docker Lab 04 - Flask Books API avec SQLite et Docker Compose

## 🎯 Objectifs du Lab

Ce lab étend le Lab 03 en ajoutant les fonctionnalités suivantes :

1. ✅ **Utilisation d'une base de données SQLite** dans un conteneur Docker
2. ✅ **Fichier docker-compose.yaml** pour orchestrer tous les conteneurs de l'application
3. ✅ **Script Python `db-test.py`** pour tester l'accès de l'API à la base de données SQLite

## 🎬 Démonstration Vidéo

[![Démonstration du Lab 04](https://img.shields.io/badge/Vidéo-Demo-red?style=for-the-badge&logo=youtube)](./screen/demo.mp4)

**Vidéo de démonstration** : [/screen/demo.mp4](./screen/demo.mp4)

La vidéo montre :
- Le démarrage des conteneurs avec Docker Compose
- Les tests de l'API avec la base de données SQLite
- La persistance des données entre les redémarrages
- Les opérations CRUD complètes

## 📋 Contenu du Projet

### Fichiers Principaux

| Fichier | Description |
|---------|-------------|
| `app.py` | API Flask basique avec SQLite |
| `app_with_logging.py` | API Flask avec logging et SQLite |
| `init_db.sql` | Script d'initialisation de la base de données |
| `db-test.py` | Script de test automatisé de la BD |
| `test_api.py` | Script de test de l'API |
| `docker-compose.yaml` | Orchestration des services Docker |
| `Dockerfile` | Image Docker pour l'API basique |
| `Dockerfile-with-logs` | Image Docker pour l'API avec logging |
| `requirements.txt` | Dépendances Python |

## 🚀 Démarrage Rapide

### Prérequis
- Docker Desktop installé
- Docker Compose installé
- Python 3.11+ (pour les tests locaux optionnels)

### 1️⃣ Cloner le dépôt

```bash
git clone <votre-repo>
cd lab-04-Mahdyy02
```

### 2️⃣ Démarrer les services

```bash
docker-compose up -d
```

Cette commande démarre :
- **API basique** sur le port `5000`
- **API avec logging** sur le port `5001`

### 3️⃣ Vérifier l'état des services

```bash
docker-compose ps
```

### 4️⃣ Tester l'accès à la base de données

```bash
python db-test.py
```

## 🏗️ Architecture

### Services Docker

```
┌─────────────────────────────────────────────────────┐
│                Docker Compose                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────┐    ┌──────────────────┐       │
│  │  api-basic       │    │ api-with-logging │       │
│  │  Port: 5000      │    │  Port: 5001      │       │
│  │  ┌────────────┐  │    │  ┌────────────┐  │       │
│  │  │  Flask API │  │    │  │  Flask API │  │       │
│  │  └────────────┘  │    │  └────────────┘  │       │
│  │  ┌────────────┐  │    │  ┌────────────┐  │       │
│  │  │ books.db   │  │    │  │ books.db   │  │       │
│  │  └────────────┘  │    │  └────────────┘  │       │
│  └──────────────────┘    │  ┌────────────┐  │       │
│                          │  │   logs/    │  │       │
│                          │  └────────────┘  │       │
│                          └──────────────────┘       │
│                                                     │
│  Volumes:                                           │
│  • db-data (API basique)                            │
│  • db-data-logs (API avec logging)                  │
│  • logs-data (Fichiers de logs)                     │
└─────────────────────────────────────────────────────┘
```

### Base de Données SQLite

**Schéma de la table `books`** :

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL
);
```

**Données initiales** :

```sql
INSERT INTO books (title, author, year) VALUES
    ('1984', 'George Orwell', 1949),
    ('To Kill a Mockingbird', 'Harper Lee', 1960),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925);
```

## 📊 Fonctionnalités Implémentées

### ✅ Changements par rapport au Lab 03

| Fonctionnalité | Lab 03 | Lab 04 |
|----------------|---------|---------|
| Stockage | Dictionnaire en mémoire | Base de données SQLite |
| Persistance | ❌ Non | ✅ Oui (volumes Docker) |
| Orchestration | Commandes docker multiples | Docker Compose |
| Initialisation BD | N/A | Script SQL automatique (`init_db.sql`) |
| Tests BD | N/A | Script `db-test.py` |
| Isolation des données | N/A | Volumes séparés par service |

### 🔧 API Endpoints

| Méthode | Endpoint | Description | Exemple |
|---------|----------|-------------|---------|
| GET | `/` | Page d'accueil | `curl http://localhost:5000/` |
| GET | `/health` | Health check | `curl http://localhost:5000/health` |
| GET | `/books` | Liste tous les livres | `curl http://localhost:5000/books` |
| GET | `/books/<id>` | Obtenir un livre | `curl http://localhost:5000/books/1` |
| POST | `/books` | Ajouter un livre | `curl -X POST -H "Content-Type: application/json" -d '{"title":"Test","author":"Author","year":2025}' http://localhost:5000/books` |
| PUT | `/books/<id>` | Mettre à jour un livre | `curl -X PUT -H "Content-Type: application/json" -d '{"year":2024}' http://localhost:5000/books/1` |
| DELETE | `/books/<id>` | Supprimer un livre | `curl -X DELETE http://localhost:5000/books/1` |

## 🧪 Tests et Validation

### Test de la Base de Données

Le script `db-test.py` effectue les tests suivants :

```bash
python db-test.py
```

**Tests effectués** :
1. ✅ Connexion à la base de données via l'API
2. ✅ Opérations CRUD (Create, Read, Update, Delete)
3. ✅ Persistance des données

**Résultats des tests** :

```
======================================================================
✅ TOUS LES TESTS SONT PASSÉS!
La base de données SQLite fonctionne correctement avec l'API.
======================================================================

🔸 BASIC:
   Connexion BD:  ✅
   Opérations CRUD: ✅
   Persistance:   ✅

🔸 WITH_LOGGING:
   Connexion BD:  ✅
   Opérations CRUD: ✅
   Persistance:   ✅
```

### Test de l'API

```bash
python test_api.py
```

Ce script teste les opérations suivantes :
- Ajout de livres
- Lecture de livres
- Mise à jour de livres
- Suppression de livres

## 🔍 Commandes Utiles

### Gestion des Services

```bash
# Démarrer tous les services
docker-compose up -d

# Arrêter tous les services
docker-compose down

# Voir les logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f api-basic
docker-compose logs -f api-with-logging

# Redémarrer un service
docker-compose restart api-basic

# Reconstruire les images
docker-compose build --no-cache

# Arrêter et supprimer les volumes (⚠️ perte de données)
docker-compose down -v
```

### Accès aux Conteneurs

```bash
# Accéder au shell d'un conteneur
docker-compose exec api-basic /bin/bash

# Accéder à la base de données SQLite
docker-compose exec api-basic sqlite3 /app/data/books.db

# Commandes SQLite utiles
.tables                    # Lister les tables
SELECT * FROM books;       # Voir tous les livres
.schema books             # Voir le schéma de la table
.exit                     # Quitter
```

### Tests manuels avec curl

```bash
# Health check
curl http://localhost:5000/health

# Liste des livres
curl http://localhost:5000/books

# Ajouter un livre
curl -X POST http://localhost:5000/books \
  -H "Content-Type: application/json" \
  -d '{"title":"The Hobbit","author":"J.R.R. Tolkien","year":1937}'

# Mettre à jour un livre
curl -X PUT http://localhost:5000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"year":1950}'

# Supprimer un livre
curl -X DELETE http://localhost:5000/books/1
```

## 💾 Persistance des Données

### Volumes Docker

Les données sont stockées dans des volumes Docker :

```yaml
volumes:
  db-data:          # Base de données pour l'API basique
  db-data-logs:     # Base de données pour l'API avec logging
  logs-data:        # Fichiers de logs
```

### Avantages

✅ **Persistance** : Les données survivent aux redémarrages des conteneurs  
✅ **Isolation** : Chaque API a sa propre base de données  
✅ **Performance** : Optimisé pour Docker  
✅ **Sécurité** : Les données sont isolées du système hôte

### ⚠️ Important

- Les données persistent après `docker-compose down`
- Les données sont **supprimées** avec `docker-compose down -v`
- Les logs sont stockés dans le volume `logs-data`

## 🐛 Dépannage

### Les conteneurs ne démarrent pas

```bash
# Vérifier les logs
docker-compose logs

# Reconstruire sans cache
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Erreur de connexion à la BD

```bash
# Vérifier les volumes
docker volume ls

# Vérifier les permissions
docker-compose exec api-basic ls -la /app/data
```

### Réinitialiser complètement

```bash
# Tout supprimer et recommencer
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 📈 Améliorations Futures

- [ ] Ajouter une interface web
- [ ] Implémenter l'authentification
- [ ] Ajouter des tests unitaires
- [ ] Migrer vers PostgreSQL pour la production
- [ ] Ajouter un cache Redis
- [ ] Implémenter la pagination
- [ ] Ajouter des métrics Prometheus

## 📚 Technologies Utilisées

- **Python 3.11** - Langage de programmation
- **Flask 3.0.0** - Framework web
- **SQLite** - Base de données
- **Docker** - Conteneurisation
- **Docker Compose** - Orchestration
- **Werkzeug 3.0.1** - WSGI utilities

## 👨‍💻 Auteur

**Mahdyy02**

## 📄 Licence

Ce projet est à des fins éducatives dans le cadre du cours de Docker.

---

## 📖 Documentation Complémentaire

Pour plus de détails techniques, consultez [README-LAB04.md](README-LAB04.md)

**Note** : Ce projet démontre l'utilisation de SQLite avec Docker. Pour des applications en production, considérez l'utilisation de bases de données plus robustes comme PostgreSQL ou MySQL.
