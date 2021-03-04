import pymongo
import json

client = pymongo.MongoClient(json.loads(open("env.json", "r").read())["mongo"])
db = client.spacey
collection = db.users

#checks if passed id exists in DB
def checkUser(id):
    if(collection.find_one({"user_id": id})):
        return True
    else:
        return False

#adds user to DB
def addUser(email, ref, id):
    if(not checkUser(id)):
        user = {
            "email": email,
            "ref": ref,
            "user_id": id,
            "hits": 0
        }
        collection.insert_one(user)

#check refferals
def checkRef(ref):
    result = dict(collection.find_one({"ref":ref}))
    hits = result["hits"]
    if(result):
        collection.update(result, { "$set": {"hits":hits+1}})
        return True
    else:
        return False
