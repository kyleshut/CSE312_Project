from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

dbImage = client['notes']['note']

# dbNotes.insert_one({"username": "hello"})
# dbNotes.update_one({"username": "hello"}, {'$push': {'notes': "ho"}})
userdata = list(dbImage.find({"username": "test1"}))[0]
notes = userdata.get('notes')

set = {"username": "test1", "notes": []}
dbImage.update_one({"username": "test1", "notes": ['', 'jdjd']}, {'$set': set})
#
# dbImage.update({'title':'MongoDB Overview'},{$set:{'title':'New MongoDB Tutorial'}})
