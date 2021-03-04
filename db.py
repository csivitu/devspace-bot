import pymongo
import json

print(json.loads(open("env.json", "r").read())["mongo"])
client = pymongo.MongoClient(json.loads(open("env.json", "r").read())["mongo"])
db = client.spacey
collection = db.users

#checks if passed email exists in DB
def checkUser(email):
    if(collection.find_one({"email": email})):
        return True
    else:
        return False

#adds user to DB
def addUser(email, ref):
    user = {
        "email": email,
        "ref": ref,
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
