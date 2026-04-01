from flask import Flask, render_template, request, jsonify
from AlphaBotV3 import AlphaBot
import threading

Ab = AlphaBot()
Ab.stop()
Ab.setPWMA(33)
Ab.setPWMB(33)

app = Flask(__name__)

move_thread = None

def run_command(cmd):
    if cmd == 'START_W':
        Ab.forward(9999)
    elif cmd == 'START_S':
        Ab.backward(9999)
    elif cmd == 'START_A':
        Ab.left(9999)
    elif cmd == 'START_D':
        Ab.right(9999)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/cmd", methods=["POST"])
def cmd():
    global move_thread

    data = request.get_json()
    command = data.get("cmd") if data else None

    if not command:
        return jsonify({"status": "no command"})

    print("Comando ricevuto:", command)

    if command == 'STOP':
        Ab.stop()
        print("Stop")
    elif command.startswith('START_'):
        # Ferma il movimento precedente
        Ab.stop()
        # Avvia il nuovo movimento in un thread separato
        move_thread = threading.Thread(target=run_command, args=(command,), daemon=True)
        move_thread.start()

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)