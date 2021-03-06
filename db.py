import pymongo
import json

client = pymongo.MongoClient(json.loads(open("env.json", "r").read())["mongo"])
db = client.spacey
collection = db.users

#checks if passed id exists in DB
def checkUser(id):
    if collection.find_one({"user_id": id}):
        return True
    else:
        return False

#adds user to DB
def addUser(email, ref, id):
    if not checkUser(id):
        user = {
            "email": email,
            "ref": ref,
            "user_id": id,
            "hits": 0
        }
        collection.insert_one(user)

#check referrals
def checkRef(ref):
    result = collection.find_one({"ref":ref})
    if result :
        result = dict(result)
        hits = result["hits"]
        collection.update(result, { "$set": {"hits":hits+1}})
        return [True, result["user_id"]]
    else:
        return [False]

#Check referral for the referral_generator()
def checkRefRandom(ref):
    result = collection.find_one({"ref":ref})
    if result:
        return True
    else:
        return False

#remove user
def removeUser(id):
    collection.delete_one({"user_id": id})