# Projet : Comparaison des architectures SGBD (NoSQL vs Relationnel)

**Groupe**
CHARRIER Evan, GAULTIER Mathis , MONTIÈGE Hugo, KOUMBA Elisia

**Sujet** :
Mettre en évidence les avantages et inconvénients liés au choix de l'architecture du SGBD (NoSQL/Relationnel) d'un point de vue développement, conception et performance.

---

## Objectifs du projet
- Comparer les approches NoSQL (MongoDB) et relationnelle (PostgreSQL) pour un cas d'usage concret : un système de blog avec articles, commentaires, utilisateurs, etc.
- Illustrer les forces et faiblesses de chaque architecture en termes de :
  - Flexibilité du schéma
  - Complexité de développement
  - Évolutivité
- Produire un notebook synthétique pour présenter les résultats.

---

## Organisation du projet
Pour ce projet, nous avons simulé une base de données d'un blog avec des données utilisateurs (`users`) et des données 
articles (`posts`). Ces données sont enregistrées dans le répertoire `datasets`.

Le répertoire `mongodb` contient les scripts spécifiques à l'utilisation de *mongodb* ainsi qu'un fichier 
`requirements.txt` afin de créer un environnement virtuel Python pour les scripts.
Le répertoire `postgresql` contient les scripts spécifiques à l'utilisation de *PostgreSQL* ainsi qu'un fichier 
`requirements.txt` afin de créer un environnement virtuel Python pour les scripts. Ce répertoire contient aussi un 
fichier `README.md` détaillant le fonctionnement et l'utilisation des scripts.


### 1. Génération des datasets
- **Données utilisateurs** (`users`) et **Données articles** (`posts`):

### 2. Implémentation MongoDB

- **Scripts Python** :

    - `import.py` : Création et import de la base de données.
    - `queries.py` : Exemples de requêtes pour ajouter une note ou un commentaire à un article, illustrant la flexibilité de MongoDB lors de l'évolution du schéma.

- **Cas d'usage** :

    - Ajout dynamique de champs (ex: note) sans migration de schéma.
    - Gestion des commentaires imbriqués.

### 3. Implémentation PostgreSQL
- Script SQL :
  - `script_init.sql` : Création des tables et insertion des données.
  - Schéma relationnel classique (tables users, posts, comments, etc.).

---

## Ce qu'il reste à faire
1. **Compléter les scripts existants**

- **MongoDB** :
    - Ajouter des requêtes complexes.

- **PostgreSQL**:

    - Mettre en évidence les jointures et leur impact sur la performance.

2. **Créer un dataset adapté au relationnel**

    - Générer un nouveau jeu de données optimisé pour PostgreSQL 
    - Montrer les limites de MongoDB pour ce type de données.
   

3. **Benchmark et analyse**

- **Mesurer les performances** :

    - Temps d'exécution des requêtes courantes (ex: récupérer un article avec ses commentaires).
    - Comparaison de la consommation mémoire et CPU.

- **Analyser la complexité** :

    - Nombre de lignes de code pour implémenter les mêmes fonctionnalités.
    - Complexité des requêtes (lors du développement).

4. **Notebook synthétique**

- **Structure proposée** :

    - Introduction au sujet et aux objectifs.
    - Présentation des datasets et des schémas.
    - Comparaison des implémentations (code + résultats de benchmark).
    - Conclusion : quand choisir NoSQL ou relationnel ?

- **Liens vers le code source** :

- Référencer les fichiers Python et SQL pour les détails techniques.

5. **Poster**

- Basé sur le notebook, avec :

    - Des graphiques de performance.
    - Des extraits de code clés.
    - Une comparaison NoSQL vs Relationnel.


