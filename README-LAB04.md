# Lab 04 - Flask Books API avec SQLite et Docker Compose

## Aperçu

Ce lab étend le Lab 03 en ajoutant une base de données SQLite persistante dans les conteneurs Docker, ainsi qu'une orchestration complète avec Docker Compose.

### Nouveautés du Lab 04

- Base de données SQLite au lieu d'un dictionnaire en mémoire
- Persistance des données avec Docker volumes
- Docker Compose pour orchestrer tous les services
- Script de test de base de données (db-test.py)
- Initialisation automatique de la BD avec init_db.sql

## Structure du Projet

```
lab-04/
├── app.py                      # API Flask basique avec SQLite
├── app_with_logging.py         # API Flask avec logging et SQLite
├── init_db.sql                 # Script d'initialisation de la BD
├── db-test.py                  # Script de test de la BD
├── test_api.py                 # Tests de l'API
├── requirements.txt            # Dépendances Python
├── Dockerfile                  # Dockerfile pour l'API basique
├── Dockerfile-with-logs        # Dockerfile pour l'API avec logging
├── docker-compose.yaml         # Orchestration des services
└── README.md                   # Documentation
```

## Démarrage Rapide

### Prérequis

- Docker installé
- Docker Compose installé
- Python 3.11+ (pour les tests locaux)

### 1. Construire et démarrer tous les services

```bash
docker-compose up -d
```

Cette commande démarre:
- API basique sur le port 5000
- API avec logging sur le port 5001
- Volumes Docker pour la persistance des données

### 2. Vérifier l'état des services

```bash
docker-compose ps
```

### 3. Tester l'accès à la base de données

```bash
python db-test.py
```

Ce script teste automatiquement:
- La connexion à la base de données
- Les opérations CRUD (Create, Read, Update, Delete)
- La persistance des données

## Architecture

### Services Docker

#### 1. API Basique (api-basic)
- Port: 5000
- Image: Construite depuis Dockerfile
- Volume: db-data pour la base de données
- Base de données: /app/data/books.db

#### 2. API avec Logging (api-with-logging)
- Port: 5001
- Image: Construite depuis Dockerfile-with-logs
- Volumes: 
  - db-data-logs pour la base de données
  - logs-data pour les fichiers de logs
- Base de données: /app/data/books.db
- Logs: /app/logs/flask_api.log

### Volumes Docker

```yaml
volumes:
  db-data:          # Base de données pour l'API basique
  db-data-logs:     # Base de données pour l'API avec logging
  logs-data:        # Fichiers de logs
```

### Réseau

- Réseau personnalisé: books-network (bridge)
- Permet la communication entre conteneurs si nécessaire

## Base de Données SQLite

### Schema

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL
);
```

### Données initiales

```sql
INSERT INTO books (title, author, year) VALUES
    ('1984', 'George Orwell', 1949),
    ('To Kill a Mockingbird', 'Harper Lee', 1960),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925);
```

## Commandes Utiles

### Gestion des services

```bash
# Démarrer tous les services
docker-compose up -d

# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes (attention: perte de données)
docker-compose down -v

# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f api-basic
docker-compose logs -f api-with-logging

# Redémarrer un service
docker-compose restart api-basic
```

### Accès aux conteneurs

```bash
# Accéder au shell d'un conteneur
docker-compose exec api-basic /bin/bash

# Accéder à la base de données SQLite
docker-compose exec api-basic sqlite3 /app/data/books.db
```

### Requêtes SQLite dans le conteneur

```bash
# Se connecter à la BD
docker-compose exec api-basic sqlite3 /app/data/books.db

# Commandes SQLite
.tables                    # Lister les tables
SELECT * FROM books;       # Voir tous les livres
.schema books             # Voir le schéma de la table
.exit                     # Quitter
```

## Tests

### Test de l'API basique (port 5000)

```bash
# Health check
curl http://localhost:5000/health

# Lister tous les livres
curl http://localhost:5000/books

# Obtenir un livre spécifique
curl http://localhost:5000/books/1

# Ajouter un livre
curl -X POST http://localhost:5000/books \
  -H "Content-Type: application/json" \
  -d '{"title":"New Book","author":"Author Name","year":2025}'

# Mettre à jour un livre
curl -X PUT http://localhost:5000/books/1 \
  -H "Content-Type: application/json" \
  -d '{"year":2024}'

# Supprimer un livre
curl -X DELETE http://localhost:5000/books/1
```

### Test de l'API avec logging (port 5001)

Mêmes commandes mais sur le port 5001:

```bash
curl http://localhost:5001/books
```

### Script de test automatisé

```bash
# Test complet de la base de données
python db-test.py

# Test de l'API avec le script existant
python test_api.py
```

## Endpoints de l'API

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Page d'accueil avec la liste des endpoints |
| GET | /health | Vérification de l'état de l'API |
| GET | /books | Lister tous les livres |
| GET | /books/\<id\> | Obtenir un livre spécifique |
| POST | /books | Ajouter un nouveau livre |
| PUT | /books/\<id\> | Mettre à jour un livre |
| DELETE | /books/\<id\> | Supprimer un livre |

## Sécurité

### API avec logging
- Utilise un utilisateur non-root (apiuser)
- Permissions correctement configurées
- Logs sécurisés dans un volume dédié

## Persistance des Données

Les données sont stockées dans des volumes Docker, ce qui signifie:

- Les données persistent après l'arrêt des conteneurs
- Les données survivent aux redémarrages
- Les données sont isolées par service (chaque API a sa propre BD)

ATTENTION: Utiliser docker-compose down -v supprime les volumes et TOUTES LES DONNÉES

## Dépannage

### Les conteneurs ne démarrent pas

```bash
# Vérifier les logs
docker-compose logs

# Reconstruire les images
docker-compose build --no-cache
docker-compose up -d
```

### Erreur de connexion à la BD

```bash
# Vérifier que les volumes existent
docker volume ls

# Vérifier les permissions dans le conteneur
docker-compose exec api-basic ls -la /app/data
```

### Réinitialiser complètement le projet

```bash
# Arrêter et supprimer tout
docker-compose down -v

# Supprimer les images
docker-compose rm -f
docker rmi lab-04-api-basic lab-04-api-with-logging

# Reconstruire
docker-compose up -d --build
```

## Différences avec Lab 03

| Aspect | Lab 03 | Lab 04 |
|--------|---------|---------|
| Stockage | Dictionnaire en mémoire | Base de données SQLite |
| Persistance | Non | Oui (volumes Docker) |
| Orchestration | Commandes docker multiples | Docker Compose |
| Initialisation BD | N/A | Script SQL automatique |
| Tests BD | N/A | Script db-test.py |
| Volumes | Non configurés | Volumes dédiés |

## Objectifs Pédagogiques

Ce lab permet d'apprendre:

1. Utilisation de SQLite dans une application Flask
2. Persistance des données avec Docker volumes
3. Orchestration multi-conteneurs avec Docker Compose
4. Initialisation automatique de base de données
5. Tests de connectivité et d'opérations CRUD
6. Gestion de plusieurs instances d'API

## Ressources

- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation SQLite](https://www.sqlite.org/docs.html)
- [Documentation Docker Compose](https://docs.docker.com/compose/)
- [Documentation Docker Volumes](https://docs.docker.com/storage/volumes/)

---

Note: Ce projet est à des fins éducatives. En production, considérez l'utilisation de bases de données plus robustes comme PostgreSQL ou MySQL pour des applications à grande échelle.
