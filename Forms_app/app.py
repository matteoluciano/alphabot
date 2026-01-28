import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

# =========================
# FLASK APP
# =========================
app = Flask(__name__)
app.secret_key = "super-secret-key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

DB_USERS = "users.db"
DB_COMMANDS = "commands.db"

VALID_COMMANDS = ["circle", "square", "triangle"]

# =========================
# USER MODEL
# =========================
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# =========================
# DATABASE FUNCTIONS - USERS
# =========================
def get_user_by_username(username):
    conn = sqlite3.connect(DB_USERS)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, password FROM users WHERE username = ?",
        (username,)
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_USERS)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, password FROM users WHERE id = ?",
        (user_id,)
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

def create_user(username, password):
    try:
        conn = sqlite3.connect(DB_USERS)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# =========================
# DATABASE FUNCTIONS - COMMANDS
# =========================
def save_command(user_id, username, command):
    conn = sqlite3.connect(DB_COMMANDS)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO commands (user_id, username, command) VALUES (?, ?, ?)",
        (user_id, username, command)
    )
    conn.commit()
    conn.close()

# =========================
# FLASK-LOGIN LOADER
# =========================
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("password")

        if not username or not password:
            flash("Username e password obbligatori!", "error")
            return redirect(url_for("register"))

        if create_user(username, password):
            flash("Registrazione completata! Effettua il login.", "success")
            return redirect(url_for("login"))
        else:
            flash("Username già esistente!", "error")
            return redirect(url_for("register"))

    return render_template("register.html")

# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("password")

        user = get_user_by_username(username)

        if user and user.password == password:
            login_user(user)
            flash(f"Benvenuto, {username}!", "success")
            return redirect(url_for("index"))

        flash("Credenziali errate!", "error")
        return redirect(url_for("login"))

    return render_template("login.html")

# =========================
# LOGOUT
# =========================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout effettuato!", "info")
    return redirect(url_for("login"))

# =========================
# MAIN PAGE (PROTETTA)
# =========================
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        cmd = request.form.get("cmd")

        if cmd in VALID_COMMANDS:
            save_command(current_user.id, current_user.username, cmd)
            flash(f"Comando '{cmd}' salvato! Il robot lo eseguirà a breve.", "success")
            print(f"✅ [{current_user.username}] Comando salvato: {cmd}")
        else:
            flash("Comando non valido!", "error")

        return redirect(url_for("index"))

    return render_template("index.html")

# =========================
# START SERVER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)