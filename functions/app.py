from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from supabase import create_client, Client

# --- Supabase setup ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://dodijnhzghlpgmdddklr.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRvZGlqbmh6Z2hscGdtZGRka2xyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM0NTE3MTksImV4cCI6MjA2OTAyNzcxOX0.soz1ofVIZ3NeWkcE1yUCIylFiVry5nwvc9PvHn7TZQQ")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Flask setup ---
app = Flask(__name__)
CORS(app)

# --- Step 1: Username + Password ---
@app.route("/api/login-step-1", methods=["POST"])
def login_step_1():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    result = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()

    if len(result.data) == 0:
        return jsonify({"success": False, "message": "Invalid username or password"})

    user = result.data[0]
    if user["status"] == "frozen":
        return jsonify({"success": False, "message": "Account is frozen"})

    return jsonify({"success": True, "user_id": user["id"], "role": user["role"]})

# --- Step 2: Security Code + Favorite Food ---
@app.route("/api/login-step-2", methods=["POST"])
def login_step_2():
    data = request.get_json()
    user_id = data.get("user_id")
    security_code = data.get("security_code")
    favorite_food = data.get("favorite_food")

    result = supabase.table("users").select("*").eq("id", user_id).eq("security_code", security_code).eq("favorite_food", favorite_food).execute()

    if len(result.data) == 0:
        return jsonify({"success": False, "message": "Invalid security details"})

    user = result.data[0]
    return jsonify({"success": True, "role": user["role"], "redirect": "admin.html" if user["role"] == "admin" else "dashboard.html"})

# --- Admin: Create a New User ---
@app.route("/api/admin/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    security_code = data.get("security_code")
    favorite_food = data.get("favorite_food")
    account_number = data.get("account_number")
    balance = data.get("balance", 0)
    role = data.get("role", "user")
    status = data.get("status", "active")

    result = supabase.table("users").insert({
        "username": username,
        "password": password,
        "security_code": security_code,
        "favorite_food": favorite_food,
        "account_number": account_number,
        "balance": balance,
        "role": role,
        "status": status
    }).execute()

    if result.data:
        return jsonify({"success": True, "message": "User created successfully"})
    else:
        return jsonify({"success": False, "message": "Failed to create user"})

# --- Run Flask ---
if __name__ == "__main__":
    app.run(debug=True)
