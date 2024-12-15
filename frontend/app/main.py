# frontend/app/main.py

from flask import Flask, render_template, request, session, redirect, url_for, flash
import requests
import os
import logging

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")  # Assurez-vous que ce nom correspond au service backend dans Docker

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")  # Utilisez une clé secrète sécurisée en production

# Configuration du logger de Flask
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)  # Capture tous les niveaux de logs
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)  # Définit le niveau de log global

def is_authenticated():
    """Vérifie si l'utilisateur est authentifié."""
    return "token" in session and "user_id" in session

def get_user_id(token):
    """
    Récupère l'ID de l'utilisateur à partir du token en appelant l'endpoint /users/me.
    Retourne l'ID de l'utilisateur si le token est valide, sinon None.
    """
    app.logger.debug(f"Token sent to /users/me: {token}")
    try:
        resp = requests.get(
            f"{BACKEND_URL}/users/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        app.logger.debug(f"/users/me response: {resp.status_code} - {resp.text}")
        if resp.status_code == 200:
            return resp.json().get("id")
        else:
            app.logger.error(f"Failed to retrieve user ID: {resp.status_code} - {resp.text}")
            return None
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Exception during /users/me request: {e}")
        return None

@app.route("/")
def index():
    """
    Page d'accueil qui redirige vers /conversations si l'utilisateur est authentifié,
    sinon affiche la page de login.
    """
    if is_authenticated():
        app.logger.info(f"User {session.get('username')} is authenticated. Redirecting to conversations.")
        return redirect(url_for("conversations"))
    app.logger.info("User is not authenticated. Rendering login page.")
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    """
    Gère la connexion de l'utilisateur.
    """
    username = request.form.get("username")
    password = request.form.get("password")
    app.logger.info(f"Attempting to log in user: {username}")

    try:
        resp = requests.post(
            f"{BACKEND_URL}/users/login",
            json={"username": username, "password": password}
        )
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Login request failed: {e}")
        flash("Login failed: Unable to reach backend service.", "error")
        return redirect(url_for("index"))

    if resp.status_code == 200:
        data = resp.json()
        token = data.get("access_token")
        if not token:
            app.logger.error("Login failed: No token received.")
            flash("Login failed: No token received.", "error")
            return redirect(url_for("index"))

        app.logger.debug(f"Received token: {token}")
        session["token"] = token
        session["username"] = username

        user_id = get_user_id(token)
        app.logger.debug(f"Retrieved user_id: {user_id}")

        if user_id:
            session["user_id"] = user_id
            app.logger.info(f"User {username} logged in successfully with user_id: {user_id}")
            return redirect(url_for("conversations"))
        else:
            flash("Failed to retrieve user ID. Please try logging in again.", "error")
            session.pop("token", None)  # Nettoyer la session en cas d'erreur
            return redirect(url_for("index"))
    else:
        error_detail = resp.json().get("detail", "Invalid credentials.")
        app.logger.error(f"Login failed: {error_detail}")
        flash(f"Login failed: {error_detail}", "error")
        return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Gère l'inscription des nouveaux utilisateurs.
    """
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        app.logger.info(f"Attempting to register user: {username}, email: {email}")

        try:
            resp = requests.post(
                f"{BACKEND_URL}/users/register",
                json={"username": username, "email": email, "password": password}
            )
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Registration request failed: {e}")
            flash("Registration failed: Unable to reach backend service.", "error")
            return redirect(url_for("register"))

        if resp.status_code == 200:
            app.logger.info(f"User {username} registered successfully.")
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("index"))
        else:
            error_detail = resp.json().get("detail", "Registration failed.")
            app.logger.error(f"Registration failed: {error_detail}")
            flash(f"Registration failed: {error_detail}", "error")
            return redirect(url_for("register"))

    app.logger.info("Rendering registration page.")
    return render_template("register.html")

@app.route("/conversations", methods=["GET", "POST"])
def conversations():
    """
    Gère l'affichage des conversations et l'envoi des messages.
    """
    if not is_authenticated():
        app.logger.warning("User is not authenticated. Redirecting to login.")
        return redirect(url_for("index"))

    token = session.get("token")
    user_id = session.get("user_id")
    username = session.get("username")
    app.logger.info(f"Accessing conversations for user_id: {user_id}, username: {username}")

    # Vérifier si le token est toujours valide
    valid_user_id = get_user_id(token)
    if not valid_user_id:
        app.logger.warning("Token invalid or expired. Clearing session and redirecting to login.")
        flash("Session expired. Please log in again.", "error")
        session.clear()
        return redirect(url_for("index"))

    if request.method == "POST":
        recipient_id = request.form.get("recipient_id")
        content = request.form.get("content")
        app.logger.info(f"Sending message from user_id: {user_id} to recipient_id: {recipient_id}")
        headers = {"Authorization": f"Bearer {token}"}

        try:
            resp = requests.post(
                f"{BACKEND_URL}/messages/",
                json={"recipient_id": int(recipient_id), "content": content},
                headers=headers
            )
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Message send request failed: {e}")
            flash("Message send failed: Unable to reach backend service.", "error")
            return redirect(url_for("conversations"))

        if resp.status_code != 200:
            error_detail = resp.json().get("detail", "Failed to send message.")
            app.logger.error(f"Message send failed: {error_detail}")
            flash(f"Message send failed: {error_detail}", "error")
        else:
            app.logger.info("Message sent successfully.")
            flash("Message sent successfully!", "success")

    # Récupérer la liste des utilisateurs
    headers = {"Authorization": f"Bearer {token}"}
    try:
        users_resp = requests.get(f"{BACKEND_URL}/users", headers=headers)
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Users list request failed: {e}")
        flash("Failed to retrieve users list: Unable to reach backend service.", "error")
        users = []
    else:
        if users_resp.status_code == 200:
            users = users_resp.json()
            app.logger.debug(f"Retrieved users list: {users}")
        else:
            error_detail = users_resp.json().get("detail", "Failed to retrieve users.")
            app.logger.error(f"Failed to retrieve users list: {error_detail}")
            users = []
            flash(f"Failed to retrieve users list: {error_detail}", "error")

    # Gérer la sélection d'une conversation spécifique
    selected_user_id = request.args.get("user_id")
    messages = []
    if selected_user_id:
        selected_user_id = int(selected_user_id)
        app.logger.info(f"Selected conversation with user_id: {selected_user_id}")

        try:
            resp = requests.get(
                f"{BACKEND_URL}/messages/conversations/{user_id}",
                headers=headers
            )
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Conversations request failed: {e}")
            flash("Failed to retrieve conversations: Unable to reach backend service.", "error")
        else:
            if resp.status_code == 200:
                all_messages = resp.json()
                # Filtrer les messages pour la conversation spécifique
                messages = [
                    msg for msg in all_messages
                    if msg["sender_id"] == selected_user_id or msg["recipient_id"] == selected_user_id
                ]
                app.logger.debug(f"Filtered messages: {messages}")
            else:
                error_detail = resp.json().get("detail", "Failed to retrieve conversations.")
                app.logger.error(f"Failed to retrieve conversations: {error_detail}")
                flash(f"Failed to retrieve conversations: {error_detail}", "error")

    else:
        app.logger.info("No conversation selected.")

    return render_template(
        "conversations.html",
        messages=messages,
        users=users,
        token=token,
        user_id=user_id,
        selected_user_id=selected_user_id
    )

@app.route("/logout")
def logout():
    """
    Gère la déconnexion de l'utilisateur en nettoyant la session.
    """
    username = session.get("username")
    app.logger.info(f"User {username} is logging out.")
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
