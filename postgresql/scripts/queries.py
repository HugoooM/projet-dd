"""
Script de requêtes PostgreSQL pour le projet de comparaison NoSQL vs Relationnel.
Illustre les requêtes complexes avec jointures et leur impact sur la performance.
Tests et benchmarks des requêtes PostgreSQL.
"""

import os
import sys
import time
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Charger les variables d'environnement depuis .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Configuration de la connexion depuis les variables d'environnement
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'blog_db'),
    'user': os.getenv('DB_USER', 'blog_user'),
    'password': os.getenv('DB_PASSWORD', 'postgresql')
}


def get_connection():
    """Établit une connexion à la base de données PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Erreur de connexion à PostgreSQL : {e}")
        sys.exit(1)


def execute_query(conn, query, params=None, fetch=True):
    """Exécute une requête et retourne les résultats."""
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    start_time = time.time()
    
    try:
        cursor.execute(query, params)
        if fetch:
            results = cursor.fetchall()
            execution_time = time.time() - start_time
            return results, execution_time
        else:
            conn.commit()
            execution_time = time.time() - start_time
            return None, execution_time
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Erreur lors de l'exécution de la requête : {e}")
        return None, None
    finally:
        cursor.close()


def query_1_get_article_with_comments():
    """
    Requête 1 : Récupérer un article avec tous ses commentaires (avec jointures).
    Illustre l'utilisation des jointures SQL pour récupérer des données liées.
    """
    conn = get_connection()
    
    query = """
    SELECT 
        a.id_article,
        a.titre,
        a.contenu,
        a.date_publication,
        a.vue,
        u.nom AS auteur_nom,
        u.email AS auteur_email,
        json_agg(
            json_build_object(
                'id_commentaire', c.id_commentaire,
                'contenu', c.contenu,
                'date', c.date,
                'auteur', u2.nom,
                'id_parent', c.id_parent
            ) ORDER BY c.date
        ) FILTER (WHERE c.id_commentaire IS NOT NULL) AS commentaires
    FROM Article a
    INNER JOIN Utilisateur u ON a.id_utilisateur = u.id_utilisateur
    LEFT JOIN Commentaire c ON a.id_article = c.id_article
    LEFT JOIN Utilisateur u2 ON c.id_utilisateur = u2.id_utilisateur
    WHERE a.titre = %s
    GROUP BY a.id_article, a.titre, a.contenu, a.date_publication, a.vue, u.nom, u.email;
    """
    
    params = ("Pourquoi MongoDB est idéal pour les blogs modernes",)
    results, exec_time = execute_query(conn, query, params)
    
    print("\n=== Requête 1 : Article avec commentaires ===")
    if exec_time is not None:
        print(f"Temps d'exécution : {exec_time*1000:.2f} ms")
    if results:
        for row in results:
            print(f"\nArticle : {row['titre']}")
            print(f"Auteur : {row['auteur_nom']} ({row['auteur_email']})")
            print(f"Vues : {row['vue']}")
            if row['commentaires']:
                print(f"Commentaires ({len(row['commentaires'])}):")
                for comment in row['commentaires']:
                    indent = "  " if comment['id_parent'] is None else "    "
                    print(f"{indent}- {comment['auteur']}: {comment['contenu'][:50]}...")
    
    conn.close()
    return results, exec_time


def query_2_add_rating_to_article():
    """
    Requête 2 : Ajouter une note à un article (évolution du schéma).
    Illustre l'ajout dynamique d'une colonne avec ALTER TABLE.
    """
    conn = get_connection()
    
    # D'abord, vérifier si la colonne existe, sinon l'ajouter
    alter_query = """
    DO $$ 
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name='article' AND column_name='note'
        ) THEN
            ALTER TABLE Article ADD COLUMN note DECIMAL(3,2);
        END IF;
    END $$;
    """
    
    execute_query(conn, alter_query, fetch=False)
    
    # Mettre à jour l'article avec une note
    update_query = """
    UPDATE Article 
    SET note = %s 
    WHERE titre = %s
    RETURNING id_article, titre, note;
    """
    
    params = (4.5, "Pourquoi MongoDB est idéal pour les blogs modernes")
    results, exec_time = execute_query(conn, update_query, params)
    
    print("\n=== Requête 2 : Ajout d'une note à un article ===")
    if exec_time is not None:
        print(f"Temps d'exécution : {exec_time*1000:.2f} ms")
    if results:
        for row in results:
            print(f"Article '{row['titre']}' mis à jour avec la note : {row['note']}")
    
    conn.close()
    return results, exec_time


def query_3_get_articles_by_tag():
    """
    Requête 3 : Récupérer tous les articles avec un tag spécifique.
    Illustre les jointures N:M pour les relations plusieurs-à-plusieurs.
    """
    conn = get_connection()
    
    query = """
    SELECT 
        a.id_article,
        a.titre,
        a.date_publication,
        a.vue,
        u.nom AS auteur,
        array_agg(t.libelle) AS tags
    FROM Article a
    INNER JOIN Utilisateur u ON a.id_utilisateur = u.id_utilisateur
    INNER JOIN Article_Tag at ON a.id_article = at.id_article
    INNER JOIN Tag t ON at.id_tag = t.id_tag
    WHERE t.libelle = %s
    GROUP BY a.id_article, a.titre, a.date_publication, a.vue, u.nom
    ORDER BY a.date_publication DESC;
    """
    
    params = ("mongodb",)
    results, exec_time = execute_query(conn, query, params)
    
    print("\n=== Requête 3 : Articles par tag ===")
    if exec_time is not None:
        print(f"Temps d'exécution : {exec_time*1000:.2f} ms")
    if results:
        print(f"Articles trouvés avec le tag 'mongodb' : {len(results)}")
        for row in results:
            print(f"\n- {row['titre']} (par {row['auteur']})")
            print(f"  Tags : {', '.join(row['tags'])}")
            print(f"  Vues : {row['vue']}")
    
    conn.close()
    return results, exec_time


def query_4_get_comments_hierarchy():
    """
    Requête 4 : Récupérer les commentaires avec leur hiérarchie (commentaires imbriqués).
    Utilise une requête récursive CTE pour gérer les réponses aux commentaires.
    """
    conn = get_connection()
    
    query = """
    WITH RECURSIVE comment_hierarchy AS (
        -- Commentaires racines (sans parent)
        SELECT 
            c.id_commentaire,
            c.contenu,
            c.date,
            c.id_article,
            c.id_parent,
            u.nom AS auteur,
            0 AS niveau,
            ARRAY[c.id_commentaire]::VARCHAR[] AS path
        FROM Commentaire c
        INNER JOIN Utilisateur u ON c.id_utilisateur = u.id_utilisateur
        WHERE c.id_article = (
            SELECT id_article FROM Article 
            WHERE titre = 'Pourquoi MongoDB est idéal pour les blogs modernes'
        ) AND c.id_parent IS NULL
        
        UNION ALL
        
        -- Commentaires enfants (récursif)
        SELECT 
            c.id_commentaire,
            c.contenu,
            c.date,
            c.id_article,
            c.id_parent,
            u.nom AS auteur,
            ch.niveau + 1,
            ch.path || c.id_commentaire
        FROM Commentaire c
        INNER JOIN Utilisateur u ON c.id_utilisateur = u.id_utilisateur
        INNER JOIN comment_hierarchy ch ON c.id_parent = ch.id_commentaire
    )
    SELECT 
        id_commentaire,
        contenu,
        date,
        auteur,
        niveau,
        REPEAT('  ', niveau) || auteur || ': ' || LEFT(contenu, 50) AS affichage
    FROM comment_hierarchy
    ORDER BY path;
    """
    
    results, exec_time = execute_query(conn, query)
    
    print("\n=== Requête 4 : Hiérarchie des commentaires (CTE récursive) ===")
    if exec_time is not None:
        print(f"Temps d'exécution : {exec_time*1000:.2f} ms")
    if results:
        print("Structure hiérarchique des commentaires :")
        for row in results:
            print(row['affichage'] + "...")
    
    conn.close()
    return results, exec_time


def query_5_get_user_statistics():
    """
    Requête 5 : Statistiques par utilisateur (nombre d'articles, commentaires, vues totales).
    Illustre les agrégations avec GROUP BY et les jointures multiples.
    """
    conn = get_connection()
    
    query = """
    SELECT 
        u.id_utilisateur,
        u.nom,
        u.email,
        u.role,
        COUNT(DISTINCT a.id_article) AS nb_articles,
        COUNT(DISTINCT c.id_commentaire) AS nb_commentaires,
        COALESCE(SUM(a.vue), 0) AS total_vues,
        COALESCE(AVG(a.note), 0) AS note_moyenne
    FROM Utilisateur u
    LEFT JOIN Article a ON u.id_utilisateur = a.id_utilisateur
    LEFT JOIN Commentaire c ON u.id_utilisateur = c.id_utilisateur
    GROUP BY u.id_utilisateur, u.nom, u.email, u.role
    ORDER BY total_vues DESC;
    """
    
    results, exec_time = execute_query(conn, query)
    
    print("\n=== Requête 5 : Statistiques par utilisateur ===")
    if exec_time is not None:
        print(f"Temps d'exécution : {exec_time*1000:.2f} ms")
    if results:
        print(f"{'Nom':<15} {'Role':<10} {'Articles':<10} {'Commentaires':<15} {'Vues totales':<15} {'Note moy.':<10}")
        print("-" * 80)
        for row in results:
            print(f"{row['nom']:<15} {row['role']:<10} {row['nb_articles']:<10} "
                  f"{row['nb_commentaires']:<15} {row['total_vues']:<15} {row['note_moyenne']:.2f}")
    
    conn.close()
    return results, exec_time


def query_6_complex_join_performance():
    """
    Requête 6 : Requête complexe avec plusieurs jointures pour tester la performance.
    Récupère tous les articles avec leurs tags, commentaires et auteurs.
    """
    conn = get_connection()
    
    query = """
    SELECT 
        a.id_article,
        a.titre,
        a.date_publication,
        a.vue,
        a.note,
        u.nom AS auteur,
        u.email AS auteur_email,
        COALESCE(
            json_agg(DISTINCT jsonb_build_object('tag', t.libelle)) 
            FILTER (WHERE t.libelle IS NOT NULL),
            '[]'::json
        ) AS tags,
        COUNT(DISTINCT c.id_commentaire) AS nb_commentaires
    FROM Article a
    INNER JOIN Utilisateur u ON a.id_utilisateur = u.id_utilisateur
    LEFT JOIN Article_Tag at ON a.id_article = at.id_article
    LEFT JOIN Tag t ON at.id_tag = t.id_tag
    LEFT JOIN Commentaire c ON a.id_article = c.id_article
    GROUP BY a.id_article, a.titre, a.date_publication, a.vue, a.note, u.nom, u.email
    ORDER BY a.date_publication DESC;
    """
    
    results, exec_time = execute_query(conn, query)
    
    print("\n=== Requête 6 : Requête complexe avec jointures multiples ===")
    if exec_time is not None:
        print(f"Temps d'exécution : {exec_time*1000:.2f} ms")
    if results:
        print(f"Nombre total d'articles : {len(results)}")
        for row in results[:3]:  # Afficher les 3 premiers
            print(f"\n📄 {row['titre']}")
            print(f"   Auteur : {row['auteur']} | Vues : {row['vue']} | "
                  f"Commentaires : {row['nb_commentaires']} | Note : {row['note'] or 'N/A'}")
            if row['tags']:
                tags_list = [tag['tag'] for tag in row['tags'] if tag.get('tag')]
                print(f"   Tags : {', '.join(tags_list)}")
    
    conn.close()
    return results, exec_time


def benchmark_queries():
    """Exécute toutes les requêtes et affiche un résumé des performances."""
    print("\n" + "="*80)
    print("BENCHMARK DES REQUÊTES POSTGRESQL")
    print("="*80)
    
    times = {}
    
    # Exécuter toutes les requêtes
    _, times['query_1'] = query_1_get_article_with_comments()
    _, times['query_2'] = query_2_add_rating_to_article()
    _, times['query_3'] = query_3_get_articles_by_tag()
    _, times['query_4'] = query_4_get_comments_hierarchy()
    _, times['query_5'] = query_5_get_user_statistics()
    _, times['query_6'] = query_6_complex_join_performance()
    
    # Résumé
    print("\n" + "="*80)
    print("RÉSUMÉ DES PERFORMANCES")
    print("="*80)
    print(f"{'Requête':<40} {'Temps (ms)':<15}")
    print("-"*80)
    for query_name, exec_time in times.items():
        if exec_time:
            print(f"{query_name:<40} {exec_time*1000:>10.2f} ms")
    
    total_time = sum(t for t in times.values() if t)
    print("-"*80)
    print(f"{'TOTAL':<40} {total_time*1000:>10.2f} ms")
    print("="*80)


if __name__ == '__main__':
    # Exécuter toutes les requêtes avec benchmark
    benchmark_queries()

