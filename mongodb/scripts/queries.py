import pymongo
from datetime import datetime

if __name__ == '__main__':
    db = pymongo.MongoClient('localhost', 27017)['projet-dd']

    # Mise en évidence des avantages de mongodb lors de l'évolution du schéma de base
    # 1. Ajout d'une note à un article
    posts_col = db['posts']

    myquery = {"titre": "Pourquoi MongoDB est idéal pour les blogs modernes"}
    newvalues = {"$set": {"note": 4.5}}

    posts_col.update_one(myquery, newvalues)


    # 2. Ajout d'un commentaire
    myquery = {"titre": "Mariette : une révolution culinaire ?"}

    new_comment = {
        "_id": "cmt_003",
        "auteur": {
            "id": "user1@example.com",
            "nom": "User1"
        },
        "contenu": "Incroyable analyse ! J'ai goûté son sandwich l'année dernière, et c'est vraiment une expérience unique.",
        "date": datetime.now().isoformat(),
        "reponses": []
    }
    posts_col.update_one(myquery, {"$push": {"commentaires": new_comment}})

    # 3. Recherche d'une regex dans un commentaire
    regex = "Mongo"

    pipeline = [
        # Filtre les articles qui ont un commentaire contenant la regex
        {
            "$match": {
                "commentaires.contenu": {"$regex": regex, "$options": "i"}
            }
        },
        # Sélection des champs
        {
            "$project": {
                "titre": 1,
                "auteur": 1,
                "note": 1,
                "commentaires": {
                    "$filter": {
                        "input": "$commentaires",
                        "as": "commentaire",
                        "cond": {
                            "$regexMatch": {"input": "$$commentaire.contenu", "regex": regex, "options": "i"}}
                    }
                }
            }
        }
    ]

    resultats = list(posts_col.aggregate(pipeline))

    print("Résultat requête 3")
    for article in resultats:
        print(f"Titre : {article['titre']}")
        print(f"Auteur : {article['auteur']['nom']}")
        print(f"Commentaires mentionnant '{regex}' :")
        for commentaire in article['commentaires']:
            print(f"  - {commentaire['auteur']['nom']} : {commentaire['contenu']}")
        print("\n")

    # 4. Ajout de meta data personnalisée à un post
    posts_col.update_one(
        {"titre": "Mariette : une révolution culinaire ?"},
        {
            "$set": {
                "metadonnees": {
                    "type": "culinaire",
                    "ingredients": ["tacos", "sauce secrète", "fromage"],
                    "temps_preparation_min": 15,
                    "prix": "abordable",
                    "note_nutritionnelle": {
                        "calories": 850,
                        "protéines_g": 200
                    }
                }
            }
        }
    )

    # 5. Recherche d'un article par rapport aux metadata
    pipeline = [
        {
            "$match": {
                "metadonnees.type": "culinaire",
                "metadonnees.ingredients": "tacos"
            }
        },
        {
            "$project": {
                "titre": 1,
                "auteur": 1,
                "metadonnees": 1,
                "_id": 0
            }
        }
    ]

    resultats = list(posts_col.aggregate(pipeline))

    print("Résultat requête 5")
    for article in resultats:
        print(f"Titre : {article['titre']}")
        print(f"Auteur : {article['auteur']['nom']}")
        print("Métadonnées :")
        for cle, valeur in article['metadonnees'].items():
            print(f"  - {cle} : {valeur}")
        print("\n")

