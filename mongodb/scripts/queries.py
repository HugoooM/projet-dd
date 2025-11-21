import pymongo
from datetime import datetime

if __name__ == '__main__':
    db = pymongo.MongoClient('localhost', 27017)['projet-dd']

    # Mise en évidence des avantages de mongodb lors de l'évolution du schéma de base
    # Ajout d'une note à un article
    posts_col = db['posts']

    myquery = {"titre": "Pourquoi MongoDB est idéal pour les blogs modernes"}
    newvalues = {"$set": {"note": 4.5}}

    posts_col.update_one(myquery, newvalues)


    # Ajout d'un commentaire
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
