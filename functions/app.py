# functions/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from passlib.hash import bcrypt as passlib_bcrypt
import os
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# Supabase config (use env vars in production)
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://dodijnhzghlpgmdddklr.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRvZGlqbmh6Z2hscGdtZGRka2xyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM0NTE3MTksImV4cCI6MjA2OTAyNzcxOX0.soz1ofVIZ3NeWkcE1yUCIylFiVry5nwvc9PvHn7TZQQ')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- Helpers ---------------------------------------------------------------
def get_user_by_username(username):
    if not username:
        return None
    resp = supabase.table('users').select('*').eq('username', username).limit(1).execute()
    return (resp.data[0] if resp and resp.data else None)

def get_user_by_id(user_id):
    if not user_id:
        return None
    resp = supabase.table('users').select('*').eq('id', user_id).limit(1).execute()
    return (resp.data[0] if resp and resp.data else None)

def is_admin_by_id(user_id):
    user = get_user_by_id(user_id)
    return bool(user and user.get('role') == 'admin')


# --- LOGIN STEP 1 ----------------------------------------------------------
@app.route('/api/login-step-1', methods=['POST'])
def login_step_1():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400

    user = get_user_by_username(username)
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    # Verify password using passlib bcrypt
    try:
        if not passlib_bcrypt.verify(password, user['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        # In case stored password is plain text (fallback), compare directly
        logging.warning(f"bcrypt verify error or non-hashed password for user {username}: {e}")
        if str(password) != str(user['password']):
            return jsonify({'error': 'Invalid username or password'}), 401

    if user.get('status') == 'frozen':
        return jsonify({'error': 'Account is frozen'}), 403

    # Return minimal data for step 2
    return jsonify({'success': True, 'id': user['id'], 'role': user.get('role', 'user')})


# --- LOGIN STEP 2 ----------------------------------------------------------
@app.route('/api/login-step-2', methods=['POST'])
def login_step_2():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    security_code = data.get('security_code')
    favorite_food = data.get('favorite_food')

    if not user_id or not security_code or not favorite_food:
        return jsonify({'error': 'user_id, security_code and favorite_food required'}), 400

    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if str(user.get('security_code')) != str(security_code) or str(user.get('favorite_food','')).lower() != str(favorite_food).lower():
        return jsonify({'error': 'Security answers incorrect'}), 401

    return jsonify({'success': True, 'id': user['id'], 'role': user.get('role', 'user')})


# --- PUBLIC REGISTER -------------------------------------------------------
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    security_code = data.get('security_code')
    favorite_food = data.get('favorite_food')
    email_or_phone = data.get('email_or_phone', None)
    balance = float(data.get('balance', 0) or 0)
    investment_funds = float(data.get('investment_funds', 0) or 0)
    role = data.get('role', 'user')
    account_number = data.get('account_number')

    if not username or not password or not security_code or not favorite_food:
        return jsonify({'error': 'username, password, security_code and favorite_food are required'}), 400

    if get_user_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400

    hashed = passlib_bcrypt.hash(password)

    insert = {
        'username': username,
        'password': hashed,
        'security_code': security_code,
        'favorite_food': favorite_food,
        'email_or_phone': email_or_phone,
        'balance': balance,
        'investment_funds': investment_funds,
        'status': 'active',
        'role': role
    }
    if account_number:
        insert['account_number'] = account_number

    resp = supabase.table('users').insert(insert).execute()
    if resp and resp.data:
        return jsonify({'message': 'Registration successful', 'user': resp.data[0]})
    return jsonify({'error': 'Registration failed'}), 400


# --- ADMIN: create-user (admin_id required) --------------------------------
@app.route('/api/admin/create-user', methods=['POST'])
def admin_create_user():
    data = request.get_json() or {}
    admin_id = data.get('admin_id')
    if not is_admin_by_id(admin_id):
        return jsonify({'error': 'Not authorized (admin required)'}), 403

    username = data.get('username')
    password = data.get('password')
    security_code = data.get('security_code')
    favorite_food = data.get('favorite_food')
    email_or_phone = data.get('email_or_phone', None)
    balance = float(data.get('balance', 0) or 0)
    investment_funds = float(data.get('investment_funds', 0) or 0)
    role = data.get('role', 'user')
    account_number = data.get('account_number')

    if not username or not password or not security_code or not favorite_food:
        return jsonify({'error': 'username, password, security_code and favorite_food required'}), 400

    if get_user_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400

    hashed = passlib_bcrypt.hash(password)

    insert = {
        'username': username,
        'password': hashed,
        'security_code': security_code,
        'favorite_food': favorite_food,
        'balance': balance,
        'investment_funds': investment_funds,
        'status': 'active',
        'role': role
    }
    if email_or_phone:
        insert['email_or_phone'] = email_or_phone
    if account_number:
        insert['account_number'] = account_number

    resp = supabase.table('users').insert(insert).execute()
    if resp and resp.data:
        return jsonify({'message': 'User created successfully', 'user': resp.data[0]})
    return jsonify({'error': 'User creation failed'}), 400


# --- ADMIN: list users -----------------------------------------------------
@app.route('/api/admin/list-users', methods=['GET'])
def admin_list_users():
    admin_id = request.args.get('admin_id')
    if not is_admin_by_id(admin_id):
        return jsonify({'error': 'Not authorized (admin required)'}), 403
    resp = supabase.table('users').select('*').order('created_at', desc=False).execute()
    return jsonify(resp.data or [])


# --- ADMIN: update user ----------------------------------------------------
@app.route('/api/admin/update-user/<user_id>', methods=['PUT'])
def admin_update_user(user_id):
    data = request.get_json() or {}
    admin_id = data.get('admin_id')
    if not is_admin_by_id(admin_id):
        return jsonify({'error': 'Not authorized (admin required)'}), 403

    updates = {}
    if 'balance' in data:
        updates['balance'] = float(data['balance'] or 0)
    if 'investment_funds' in data:
        updates['investment_funds'] = float(data['investment_funds'] or 0)
    if 'status' in data:
        updates['status'] = data['status']
    if 'security_code' in data:
        updates['security_code'] = data['security_code']
    if 'favorite_food' in data:
        updates['favorite_food'] = data['favorite_food']
    if 'password' in data and data['password']:
        updates['password'] = passlib_bcrypt.hash(data['password'])

    if not updates:
        return jsonify({'error': 'No valid update fields provided'}), 400

    resp = supabase.table('users').update(updates).eq('id', user_id).execute()
    if resp and resp.data:
        return jsonify({'message': 'User updated', 'user': resp.data[0]})
    return jsonify({'error': 'Update failed'}), 400


# --- Simple transactions - used by front-end simulator ---------------------
@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json() or {}
    user_id = data.get('user_id')
    tx_type = data.get('type')
    amount = float(data.get('amount') or 0)
    description = data.get('description', '')

    if not user_id or not tx_type:
        return jsonify({'error': 'user_id and type required'}), 400

    resp = supabase.table('transactions').insert({
        'user_id': user_id,
        'type': tx_type,
        'amount': amount,
        'description': description
    }).execute()

    # Note: updating balances via SQL expression isn't guaranteed with supabase.raw here.
    # For a simple demo we fetch current balance and set the new balance server-side.
    try:
        user = get_user_by_id(user_id)
        if user:
            new_balance = float(user.get('balance', 0))
            if tx_type.lower() == 'deposit':
                new_balance += amount
            elif tx_type.lower() in ('withdraw', 'transfer'):
                new_balance -= amount
            supabase.table('users').update({'balance': new_balance}).eq('id', user_id).execute()
    except Exception as e:
        logging.error("Balance update failed: %s", e)

    return jsonify({'message': 'Transaction recorded', 'transaction': resp.data[0] if resp and resp.data else None})


# --- Run -------------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
