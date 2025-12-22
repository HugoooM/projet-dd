# Scripts PostgreSQL

## Installation

1. Installer les dépendances :

```bash
pip install -r requirements.txt
```

2. Créer le fichier `.env` :

```bash
cp env.example .env
```

Puis modifier les valeurs dans `.env` .

## Initialisation de la base de données

Lancer le script SQL pour créer la base et les tables :

```bash
psql -U postgres -f postgresql/schema/script_init.sql
```

Ça va créer :

- L'utilisateur `blog_user`
- La base `blog_db`
- Toutes les tables avec les données de test

## Utilisation

Lancer les requêtes :

```bash
python scripts/queries.py
```

Le script exécute différentes requêtes et affiche le temps d'exécution de chacune.

## Les requêtes

1. Récupérer un article avec ses commentaires (jointures)
2. Ajouter une note à un article (ALTER TABLE)
3. Récupérer les articles par tag (jointure N:M)
4. Hiérarchie des commentaires (CTE récursive)
5. Statistiques par utilisateur (agrégations)
6. Requête complexe avec plusieurs jointures
