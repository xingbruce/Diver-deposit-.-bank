from flask import Flask, request, jsonify
from supabase import create_client
import os
from passlib.hash import bcrypt
import random

app = Flask(__name__)
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    response = supabase.table('users').select('*').eq('username', data['username']).execute()
    if not response.data or not bcrypt.verify(data['password'], response.data[0]['password']) or response.data[0]['security_code'] != data['security_code'] or response.data[0]['favorite_food'] != data['favorite_food']:
        return jsonify({'error': 'Invalid credentials'}), 401
    user = response.data[0]
    return jsonify({'role': user['role'], 'id': user['id']})

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    data = request.get_json()
    response = supabase.table('transactions').insert({
        'user_id': data['user_id'],
        'type': data['type'],
        'amount': data['amount'],
        'description': data['description']
    }).execute()
    return jsonify({'message': 'Transaction added'})

@app.route('/api/admin/users', methods=['POST'])
def create_user():
    data = request.get_json()
    response = supabase.table('users').insert({
        'admin_id': data['admin_id'],
        'username': data['username'],
        'password': bcrypt.hash(data['password']),
        'security_code': data['security_code'],
        'favorite_food': data['favorite_food'],
        'account_number': f"ACCT{''.join([str(x) for x in range(10, 90)]).zfill(10)}",
        'balance': data['balance'],
        'investment_funds': data.get('investment_funds', 0)
    }).execute()
    return jsonify({'message': 'User created'})

@app.route('/api/admin/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    response = supabase.table('users').update({
        'balance': data.get('balance'),
        'status': data.get('status'),
        'investment_funds': data.get('investment_funds'),
        'password': bcrypt.hash(data.get('password')) if data.get('password') else None,
        'security_code': data.get('security_code'),
        'favorite_food': data.get('favorite_food')
    }).eq('id', user_id).execute()
    return jsonify({'message': 'User updated'})

@app.route('/api/loan_companies', methods=['GET'])
def get_loan_companies():
    response = supabase.table('loan_companies').select('*').execute()
    return jsonify(response.data)

@app.route('/api/bitcoin_exchanges', methods=['GET'])
def get_bitcoin_exchanges():
    response = supabase.table('bitcoin_exchanges').select('*').execute()
    return jsonify(response.data)

@app.route('/api/stock_exchanges', methods=['GET'])
def get_stock_exchanges():
    response = supabase.table('stock_exchanges').select('*').execute()
    return jsonify(response.data)

# New Registration Endpoint
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email_or_phone = data.get('email_or_phone')
    password = data.get('password')
    security_code = data.get('security_code')
    favorite_food = data.get('favorite_food')
    account_number = f"ACCT{''.join([str(random.randint(0, 9)) for _ in range(10)])}"

    existing = supabase.table('users').select('id').eq('username', username).execute()
    if existing.data:
        return jsonify({'error': 'Username already taken'}), 400

    new_user = {
        'username': username,
        'password': bcrypt.hash(password),
        'security_code': security_code,
        'favorite_food': favorite_food,
        'account_number': account_number,
        'balance': 0.00,
        'investment_funds': 0.00,
        'role': 'user',
        'status': 'pending',
        'email_or_phone': email_or_phone
    }
    response = supabase.table('users').insert(new_user).execute()
    return jsonify({'message': 'Registration pending admin approval', 'id': response.data[0]['id']}), 201

# New Passport Upload Endpoint
@app.route('/api/upload_passport', methods=['POST'])
def upload_passport():
    if 'passport' not in request.files:
        return jsonify({'error': 'No passport image uploaded'}), 400
    file = request.files['passport']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    # Placeholder: Store file path (integrate Supabase Storage for real use)
    passport_url = f"passports/{file.filename}"
    user_id = request.form.get('user_id')
    supabase.table('users').update({'passport_image': passport_url}).eq('id', user_id).execute()
    return jsonify({'message': 'Passport uploaded', 'url': passport_url}), 200

# New Admin Approval Endpoint
@app.route('/api/approve_user/<int:user_id>', methods=['POST'])
def approve_user(user_id):
    supabase.table('users').update({'status': 'active'}).eq('id', user_id).execute()
    return jsonify({'message': 'User approved'}), 200

# New Admin Freeze Endpoint
@app.route('/api/freeze_user/<int:user_id>', methods=['POST'])
def freeze_user(user_id):
    supabase.table('users').update({'status': 'frozen'}).eq('id', user_id).execute()
    return jsonify({'message': 'User frozen'}), 200

# New Admin Add Profile Endpoint
@app.route('/api/add_profile', methods=['POST'])
def add_profile():
    data = request.get_json()
    new_profile = {
        'username': data.get('username'),
        'password': bcrypt.hash(data.get('password')),
        'security_code': data.get('security_code'),
        'favorite_food': data.get('favorite_food'),
        'account_number': f"ACCT{''.join([str(random.randint(0, 9)) for _ in range(10)])}",
        'balance': 0.00,
        'investment_funds': 0.00,
        'role': 'user',
        'status': 'active'
    }
    response = supabase.table('users').insert(new_profile).execute()
    return jsonify({'message': 'Profile added', 'id': response.data[0]['id']}), 201

# New Password Update Endpoint
@app.route('/api/update_password', methods=['POST'])
def update_password():
    data = request.get_json()
    user_id = data.get('user_id')
    new_password = data.get('new_password')
    supabase.table('users').update({'password': bcrypt.hash(new_password)}).eq('id', user_id).execute()
    return jsonify({'message': 'Password updated'}), 200

if __name__ == '__main__':
    app.run(debug=True)
