# prima prova
from flask import Flask, render_template, request

# creare l'app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    cmd = request.form.get("cmd")

    if cmd:
        print("Comando ricevuto:", cmd)
        if cmd == 'W':
            print("Vado avanti")
        elif cmd == 'A':
            print("Vado a sinistra")
        elif cmd == 'S':
            print("Vado indietro")
        elif cmd == 'D':
            print("Vado a destra")

    return render_template("index.html")

if __name__ == '__main__':
    app.run()