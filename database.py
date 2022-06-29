
from pymongo import MongoClient
import os

client = MongoClient('mongodb+srv://wikkie:vignesh7550@b-zone-discord-bot-db.gr1zx.mongodb.net/?retryWrites=true&w=majority')
db = client.rpg_users_discord_database
users_collection = db.rpg_users_discord_collection
# def get_db():
#     db = 
#     # col = db.my_collection
#     # result = col.find()
#     return db

def insert_users_data(data):
    result = users_collection.insert_one(data)
    return result.acknowledged

def get_players_data():
    result = list(users_collection.find())
    return result

def is_registered_user(user_id):
    result = users_collection.find_one({"player_discord_id":user_id})
    return result

def update_player_faction_rank(user_id,faction_rank):
    result = users_collection.find_one_and_update({"player_discord_id":user_id},{"$set":{"faction_rank":faction_rank}})
    result = list(result)
    return len(result)
def update_player_faction_name(user_id,faction_name):
    result = users_collection.find_one_and_update({"player_discord_id":user_id},{"$set":{"faction_name":faction_name}})
    result = list(result)
    return len(result)

def update_player_other_faction(user_id,other_faction_value):
    result = users_collection.find_one_and_update({"player_discord_id":user_id},{"$set":{"other_faction":other_faction_value}})
    result = list(result)
    return len(result)


def clean_database():
    users_collection.delete_many({})
    print("Cleaned the collections")
    result = list(users_collection.find())
    return result
