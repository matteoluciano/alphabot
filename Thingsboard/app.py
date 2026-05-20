from flask import Flask, render_template, request, jsonify
from AlphaBotV3 import AlphaBot
from flasgger import Swagger
import threading
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json
import time

# ── AlphaBot ────────────────────────────────────────────────────────────────
Ab = AlphaBot()
Ab.stop()
Ab.setPWMA(33)
Ab.setPWMB(33)

# ── Flask ────────────────────────────────────────────────────────────────────
app = Flask(__name__)
move_thread = None

app.config["SWAGGER"] = {
    "title": "API sensori",
    "uiversion": 3,
}
swagger = Swagger(app)

# ── ThingsBoard MQTT ─────────────────────────────────────────────────────────
THINGSBOARD_HOST = "127.0.0.1"
ACCESS_TOKEN     = "vUm2R5zjmxUiX40Ez775"
TELEMETRY_TOPIC  = "v1/devices/me/telemetry"
PUBLISH_INTERVAL = 5          # secondi tra un invio e l'altro

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(ACCESS_TOKEN)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connesso a ThingsBoard")
    else:
        print(f"[MQTT] Errore connessione: {rc}")

def on_publish(client, userdata, mid):
    print(f"[MQTT] Messaggio inviato (id: {mid})")

mqtt_client.on_connect = on_connect
mqtt_client.on_publish  = on_publish

mqtt_client.connect(THINGSBOARD_HOST, 1883, 60)
mqtt_client.loop_start()

def sensor_publisher():
    """Thread che legge i sensori e li pubblica su ThingsBoard ogni PUBLISH_INTERVAL secondi."""
    while True:
        try:
            left  = Ab.left_sensor()
            right = Ab.right_sensor()

            payload = {
                "sensore_sinistro": left,
                "sensore_destro":   right,
            }

            result = mqtt_client.publish(TELEMETRY_TOPIC, json.dumps(payload), qos=1)

            if result.rc == 0:
                print(f"[MQTT] Inviato: {payload}")
            else:
                print(f"[MQTT] Errore invio: {result.rc}")

        except Exception as e:
            print(f"[MQTT] Eccezione nel publisher: {e}")

        time.sleep(PUBLISH_INTERVAL)

# Avvia il thread di pubblicazione come daemon (si chiude con il processo principale)
threading.Thread(target=sensor_publisher, daemon=True).start()

# ── Route Flask ──────────────────────────────────────────────────────────────
@app.route("/api/sensori", methods=["GET"])
def leggi_sensori():
    """
    Lettura sensori AlphaBot
    ---
    responses:
      200:
        description: Stato sensori
    """
    left  = Ab.left_sensor()
    right = Ab.right_sensor()

    return jsonify({
        "sensore_sinistro": left,
        "sensore_destro":   right,
    })

def run_command(cmd):
    if cmd == "START_W":
        Ab.setPWMA(50)
        Ab.setPWMB(50)
        Ab.forward(9999)
    elif cmd == "START_S":
        Ab.setPWMA(50)
        Ab.setPWMB(50)
        Ab.backward(9999)
    elif cmd == "START_A":
        Ab.setPWMA(31)
        Ab.setPWMB(31)
        Ab.left(9999)
    elif cmd == "START_D":
        Ab.setPWMA(31)
        Ab.setPWMB(31)
        Ab.right(9999)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/cmd", methods=["POST"])
def cmd():
    global move_thread

    data    = request.get_json()
    command = data.get("cmd") if data else None

    if not command:
        return jsonify({"status": "no command"})

    print("Comando ricevuto:", command)

    if command == "STOP":
        Ab.stop()
        print("Stop")
    elif command.startswith("START_"):
        Ab.stop()
        move_thread = threading.Thread(target=run_command, args=(command,), daemon=True)
        move_thread.start()

    return jsonify({"status": "ok"})

# ── Avvio ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("[MQTT] Disconnesso")