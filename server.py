from flask import Flask, request, jsonify, session
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SECRET_KEY'] = 'dg-smart-local-session'

# Cloud Database Connection
client = MongoClient('mongodb+srv://krishranarajput2007_db_user:Mq6Og7D5L16gcuw7@dg-smart.ece2swx.mongodb.net/?appName=DG-Smart', serverSelectionTimeoutMS=5000, connectTimeoutMS=5000, socketTimeoutMS=5000)
db = client['smartdg_db']
users_col = db['users']

@app.route('/')
def home():
    return app.send_static_file('login.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    try:
        user = users_col.find_one({'userid': data.get('userid'), 'password': data.get('password')})
    except PyMongoError:
        return jsonify({'success': False, 'error': 'DATABASE_UNAVAILABLE'}), 503
    
    if user:
        session['userid'] = user.get('userid')
        return jsonify({
            'success': True, 
            'userid': user.get('userid'),
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

@app.route('/api/customer/<userid>', methods=['GET'])
def get_customer(userid):
    if userid == '__current__':
        userid = session.get('userid')
    if not userid:
        return jsonify({'success': False, 'error': 'AUTHENTICATION_REQUIRED'}), 401
    try:
        customer = users_col.find_one({'userid': userid, 'role': 'customer'}, {'_id': 0, 'password': 0})
    except PyMongoError:
        return jsonify({'success': False, 'error': 'DATABASE_UNAVAILABLE'}), 503
    if not customer:
        return jsonify({'success': False, 'error': 'CUSTOMER_NOT_FOUND'}), 404
    return jsonify({'success': True, 'customer': customer})

if __name__ == '__main__':
    print("Starting Secure Smart DG Server on port 8080...")
    app.run(host='0.0.0.0', port=8080)