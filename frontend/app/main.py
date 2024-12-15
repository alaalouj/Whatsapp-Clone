# frontend/app/main.py

from flask import Flask, render_template, request, session, redirect, url_for
import requests
import os

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")  # via docker network

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "frontendsecretkey")  # en prod, utiliser une variable d'environnement

@app.route("/")
def index():
    if "token" in session:
        return redirect(url_for("conversations"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    resp = requests.post(f"{BACKEND_URL}/users/login", json={"username": username, "password": password})
    if resp.status_code == 200:
        data = resp.json()
        token = data["access_token"]
        session["token"] = token
        session["username"] = username
        user_id = get_user_id(token)
        if user_id is not None:
            session["user_id"] = user_id
            return redirect(url_for("conversations"))
        else:
            return "Failed to retrieve user ID", 401
    else:
        return "Login failed", 401

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        resp = requests.post(f"{BACKEND_URL}/users/register", json={"username": username, "password": password})
        if resp.status_code == 200:
            return redirect(url_for("index"))
        else:
            return "Registration failed", 400
    return render_template("register.html")

@app.route("/conversations", methods=["GET", "POST"])
def conversations():
    token = session.get("token")
    username = session.get("username")
    user_id = session.get("user_id")
    if not token or not username or not user_id:
        return redirect(url_for("index"))

    if request.method == "POST":
        recipient_id = request.form.get("recipient_id")
        content = request.form.get("content")
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(f"{BACKEND_URL}/messages/", json={"recipient_id": int(recipient_id), "content": content}, headers=headers)
        if resp.status_code != 200:
            return "Message send failed", 400

    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{BACKEND_URL}/conversations/{user_id}", headers=headers)
    messages = resp.json() if resp.status_code == 200 else []
    return render_template("conversations.html", messages=messages, token=token, user_id=user_id)

def get_user_id(token):
    # Utiliser l'endpoint /users/me pour récupérer les informations de l'utilisateur
    resp = requests.get(f"{BACKEND_URL}/users/me", headers={"Authorization": f"Bearer {token}"})
    if resp.status_code == 200:
        return resp.json().get("id")
    return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
