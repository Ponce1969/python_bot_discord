import pymongo, os
from dotenv import load_dotenv


load_dotenv()
db_uri = os.getenv("DB_URI")

def db_connect():
    connection = pymongo.MongoClient(db_uri)
    return connection

def register(conn, ctx):
    database = conn["discord_server"]
    collection = database["user"]
    doc= {"discordID" : str(ctx.author.id), "userName": str(ctx.author)}
    collection.insert_one(doc)

def verify_id(conn, discord_ID):
    database = conn["discord_server"]
    collection = database["users"]
    doc = collection.find_one({"discordID": discord_ID})
    if doc:
        return True
    else:
        return False