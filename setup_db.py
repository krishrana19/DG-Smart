from pymongo import MongoClient

print("Connecting to MongoDB Atlas...")
client = MongoClient('mongodb+srv://krishranarajput2007_db_user:Mq6Og7D5L16gcuw7@dg-smart.ece2swx.mongodb.net/?appName=DG-Smart')
db = client['smartdg_db']
users_col = db['users']

# Clear out the old data
users_col.delete_many({})

# Setup ONE Admin and ONE Demo Customer with your new passwords
users = [
    {
        "userid": "admin", 
        "password": "dg19", 
        "role": "admin", 
        "name": "System Admin"
    },
    {
        "userid": "CUST001", 
        "password": "cust123", 
        "role": "customer", 
        "name": "Harshdeep", 
        "bill_amount": 1250, 
        "due_date": "2026-10-15"
    }
]

users_col.insert_many(users)
print("Success! Database reset with new admin and customer passwords.")