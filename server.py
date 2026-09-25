from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__, static_folder='.', static_url_path='')

# Cloud Database Connection
client = MongoClient('mongodb+srv://krishranarajput2007_db_user:Mq6Og7D5L16gcuw7@dg-smart.ece2swx.mongodb.net/?appName=DG-Smart')
db = client['smartdg_db']
users_col = db['users']

@app.route('/')
def home():
    return app.send_static_file('login.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = users_col.find_one({'userid': data.get('userid'), 'password': data.get('password')})
    
    if user:
        return jsonify({
            'success': True, 
            'role': user.get('role'),
            'name': user.get('name', 'Admin'),
            'bill_amount': user.get('bill_amount', 0),
            'due_date': user.get('due_date', 'N/A')
        })
    return jsonify({'success': False})

# NEW ROUTE: Fetch all customers for the Admin table
@app.route('/api/customers', methods=['GET'])
def get_customers():
    # Find all customers, exclude their passwords and hidden MongoDB IDs
    customers = list(users_col.find({"role": "customer"}, {"_id": 0, "password": 0}))
    return jsonify({'success': True, 'customers': customers})

if __name__ == '__main__':
    print("Starting Secure Smart DG Server on port 8080...")
    app.run(host='0.0.0.0', port=8080)