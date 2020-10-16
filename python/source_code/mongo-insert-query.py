from pymongo import MongoClient

#Creating a pymongo client
client = MongoClient('localhost', 27017)

#Getting the database instance
db = client['sdsegf']

#Creating a collection
coll = db['example']

#Inserting document into a collection
data = [
   {"_id": "1001", "name": "Ram", "age": "26", "city": "Hyderabad"},
   {"_id": "1002", "name": "Rahim", "age": "27", "city": "Bangalore"},
   {"_id": "1003", "name": "Robert", "age": "28", "city": "Mumbai"},
   {"_id": "1004", "name": "Romeo", "age": "25", "city": "Pune"},
   {"_id": "1005", "name": "Sarmista", "age": "23", "city": "Delhi"},
   {"_id": "1006", "name": "Rasajna", "age": "26", "city": "Chennai"}
]
res = coll.insert_many(data)
print("Data inserted ......")

#Retrieving data
print("Documents in the collection: ")

for doc1 in coll.find({"name":"Sarmista"}):
   print(doc1)