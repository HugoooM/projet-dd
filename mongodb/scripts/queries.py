import pymongo

if __name__ == '__main__':
    db = pymongo.MongoClient('localhost', 27017)['projet-dd']

    # Mise en évidence des avantages de mongodb lors de l'évolution du schéma de base
    # Ajout d'une note à un article
    posts_col = db['posts']

    myquery = {"titre": "Pourquoi MongoDB est idéal pour les blogs modernes"}
    newvalues = {"$set": {"note": 4.5}}

    posts_col.update_one(myquery, newvalues)