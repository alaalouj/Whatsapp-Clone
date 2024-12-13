from flask import Flask, render_template, request, session, redirect, url_for
import requests
import os

BACKEND_URL = "http://backend:8000"  # via docker network

app = Flask(__name__)
app.secret_key = "frontendsecretkey"  # en prod, utiliser variable d'env

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
        session["token"] = data["access_token"]
        # Récupérer l'ID utilisateur à partir du token (normalement stocké dans le JWT, on simplifie)
        # Ici, on pourrait appeler /users/me si on avait ce endpoint. Pour simplifier, ajoutons-le plus tard.
        # Hypothèse: ID stocké dans token décodé côté frontend (non recommandé en prod).
        # Simplifions en ajoutant un cookie user_id une fois l'endpoint prévu:
        # Pour l'instant on ne sait pas user_id. On pourrait créer un endpoint /users/me, mais on a pas implémenté.
        # On va le faire simple: On stocke username, on supposera user_id connu plus tard ou on modifie backend.
        session["username"] = username
        return redirect(url_for("conversations"))
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
    if not token or not username:
        return redirect(url_for("index"))
    # Dans un vrai cas, on aurait besoin d'un endpoint /users/me pour récupérer l'user_id
    # Rajoutons-le rapidement dans le backend (facultatif)
    user_id = get_user_id(token)
    if user_id is None:
        return "User not found", 401

    if request.method == "POST":
        recipient_id = request.form.get("recipient_id")
        content = request.form.get("content")
        headers = {"token": token}
        resp = requests.post(f"{BACKEND_URL}/messages", json={"recipient_id": int(recipient_id), "content": content}, headers=headers)
        if resp.status_code != 200:
            return "Message send failed", 400

    headers = {"token": token}
    resp = requests.get(f"{BACKEND_URL}/conversations/{user_id}", headers=headers)
    messages = resp.json() if resp.status_code == 200 else []
    return render_template("conversations.html", messages=messages)

def get_user_id(token):
    # Décoder le token JWT côté frontend (non recommandé, mieux d'avoir un endpoint dédié dans backend)
    # Par simplification, ajoutons un endpoint dans backend:
    # On modifie backend/app/routes/auth.py (ajouter un /users/me) :

    resp = requests.get(f"{BACKEND_URL}/users/me", headers={"token": token})
    if resp.status_code == 200:
        return resp.json()["id"]
    return None

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
