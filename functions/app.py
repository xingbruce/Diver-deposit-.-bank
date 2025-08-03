from flask import Flask, request, jsonify
from supabase import create_client, Client
from passlib.hash import bcrypt
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Supabase configuration
supabase_url = os.environ.get('SUPABASE_URL', 'https://dodijnhzghlpgmdddklr.supabase.co')
supabase_key = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRvZGlqbmh6Z2hscGdtZGRka2xyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM0NTE3MTksImV4cCI6MjA2OTAyNzcxOX0.soz1ofVIZ3NeWkcE1yUCIylFiVry5nwvc9PvHn7TZQQ')
supabase = create_client(supabase_url, supabase_key)

@app.route('/api/login-step-1', methods=['POST'])
def login_step_1():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    response = supabase.table('users').select('*').eq('username', username).execute()
    user = response.data[0] if response.data else None
    logging.debug(f"Login step 1 - User: {username}, Response: {response.data}")

    if user and bcrypt.verify(password, user['password']):
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    security_code = data.get('security_code')
    favorite_food = data.get('favorite_food')

    response = supabase.table('users').select('*').eq('username', username).execute()
    user = response.data[0] if response.data else None
    logging.debug(f"Login - User: {username}, Data: {data}, User: {user}")

    if user and bcrypt.verify(password, user['password']) and user['security_code'] == security_code and user['favorite_food'].lower() == favorite_food.lower():
        return jsonify({'success': True, 'id': user['id'], 'role': user.get('role', 'user')})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email_or_phone = data.get('email_or_phone')
    password = data.get('password')
    security_code = data.get('security-code')
    favorite_food = data.get('favorite-food')

    hashed_password = bcrypt.hash(password)
    response = supabase.table('users').insert({
        'username': username,
        'email_or_phone': email_or_phone,
        'password': hashed_password,
        'security_code': security_code,
        'favorite_food': favorite_food,
        'balance': 0.0,
        'investment_funds': 0.0,
        'status': 'pending',
        'role': 'user'
    }).execute()

    if response.data:
        return jsonify({'message': 'Registration successful, pending admin approval'})
    return jsonify({'message': 'Registration failed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
