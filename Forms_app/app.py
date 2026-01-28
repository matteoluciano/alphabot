import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin,login_user, login_required,logout_user, current_user
from AlphaBotV3 import AlphaBot

# alphabot
Ab = AlphaBot()
Ab.stop()
Ab.setPWMA(33)
Ab.setPWMB(33)

# flask
app = Flask(__name__)
app.secret_key = "super-secret-key"  # OBBLIGATORIA per Flask-Login

login_manager = LoginManager()
login_manager.init_app(app) # collega l'app a flask-login
login_manager.login_view = "login"

DB_PATH = "users.db"

# classe user
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# query
def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

# login loader
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@app.route("/")
def index():
    return redirect(url_for("login"))

# login
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("password")

        user = get_user_by_username(username)

        if user and user.password == password:
            login_user(user, remember=False)
            return redirect(url_for("commands"))

        return "Login fallito", 401

    return render_template("login.html")

# logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# controlli (accessisibile solo con login)
@app.route("/commands", methods=["GET", "POST"])
@login_required
def commands():
    if request.method == "POST":
        cmd = request.form.get("cmd")

        if cmd:
            print(f"[{current_user.username}] Comando:", cmd)

            if cmd == 'W':
                Ab.forward(1)
            elif cmd == 'A':
                Ab.left(0.28)
            elif cmd == 'S':
                Ab.backward(1)
            elif cmd == 'D':
                Ab.right(0.28)
            elif cmd == 'triangolo':
                Ab.triangolo()
            elif cmd == 'quadrato':
                Ab.quadrato()
            elif cmd == 'cerchio':
                Ab.cerchio()

    return render_template("commands.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)