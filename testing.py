from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")

dbImage = client['image']['image']

# dbNotes.insert_one({"username": "hello"})
# dbNotes.update_one({"username": "hello"}, {'$push': {'notes': "ho"}})
userdata = list(dbImage.find({}))
for i in userdata:
    print(i.get("image"))


