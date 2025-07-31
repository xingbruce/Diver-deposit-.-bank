from flask import Flask, request, jsonify
from supabase import create_client
import os
from passlib.hash import bcrypt

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

if __name__ == '__main__':
    app.run(debug=True)
