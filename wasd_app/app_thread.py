from flask import Flask, render_template, request
from AlphaBotV3 import AlphaBot
import threading

Ab = AlphaBot()
Ab.stop()

Ab.setPWMA(33) #S
Ab.setPWMB(33) #D

# creare l'app
app = Flask(__name__)

def movimenti(cmd):
    if cmd == 'W':
        print("Vado avanti")
        Ab.forward(1)
    elif cmd == 'A':
        print("Vado a sinistra")
        Ab.left(0.28)
    elif cmd == 'S':
        print("Vado indietro")
        Ab.backward(1)
    elif cmd == 'D':
        print("Vado a destra")
        Ab.right(0.28)

@app.route("/", methods=["GET", "POST"])
def index():
    cmd = request.form.get("cmd")

    if cmd:
        print("Comando ricevuto:", cmd)
        t = threading.Thread(target=movimenti, args=(cmd,))
        t.daemon = True
        t.start()
        

    return render_template("index.html")

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)