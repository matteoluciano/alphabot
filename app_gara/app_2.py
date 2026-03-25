from flask import Flask, render_template, request, jsonify, redirect, url_for
from AlphaBotV3 import AlphaBot

Ab = AlphaBot()
Ab.stop()

Ab.setPWMA(33)
Ab.setPWMB(33)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/cmd", methods=["POST"])
def cmd():
    data = request.get_json()
    command = data.get("cmd") if data else None

    if command:
        print("Comando ricevuto:", command)
        if command == 'START_W':
            print("Vado avanti")
            Ab.forward()
        elif command == 'START_S':
            print("Vado indietro")
            Ab.backward()
        elif command == 'START_A':
            print("Vado a sinistra")
            Ab.left()
        elif command == 'START_D':
            print("Vado a destra")
            Ab.right()
        elif command == 'STOP':
            print("Stop")
            Ab.stop()

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
