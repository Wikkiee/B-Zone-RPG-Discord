
import os
from pymongo import MongoClient
import re
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())



client = MongoClient(os.environ.get("DB_TOKEN"))
db = client.rpg_users_discord_database

users_collection = db.rpg_users_discord_collection


forum_collection = db.forum_tracker_link_collection

def create_last_announcement_link():
    collist = db.list_collection_names()
    if "forum_tracker_link_collection" in collist:
        print("The collection exists.")
        return "The collection exists."
    else:
        forum_collection.insert_one({
            "type":"forum",
            "link":""
        })
        return "Collection Created successfully"

def  update_last_announcement_link(link):
    result = forum_collection.find_one_and_update({'type':"forum"},{ '$set': { "link" :link } })
    return result


def get_last_announcement_link():
    result = forum_collection.find_one({"type":"forum"})   
    return result["link"]    

def insert_users_data(data):
    result = users_collection.insert_one(data)
    return result.acknowledged

def get_players_data():
    result = list(users_collection.find())
    return result

def is_registered_user(user_id):
    result = users_collection.find_one({"player_discord_id":user_id})
    return result

def is_registered_rpg_user(player_name):
    result = users_collection.find_one({'player_name': re.compile('^' + re.escape(player_name) + '$', re.IGNORECASE)})
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
