import json
import pymongo


def create_database():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/", connect=False)

    if 'projet-dd' in myclient.list_database_names():
        # Suppression de la base si elle existe déjà
        myclient.drop_database('projet-dd')

    # Création de la base et des collections
    db = myclient['projet-dd']
    users_col = db['users']
    posts_col = db['posts']

    # Chargement des users depuis le fichier json
    with open("datasets/users.json") as users_file:
        users_list = json.load(users_file)

    users_col.insert_many(users_list)

    # Chargement des blogs depuis le fichier json
    with open("datasets/posts.json") as posts_file:
        posts_list = json.load(posts_file)

    posts_col.insert_many(posts_list)



if __name__ == '__main__':
    create_database()







