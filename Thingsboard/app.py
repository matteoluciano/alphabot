"""
app.py  –  AlphaBot ← ThingsBoard
==========================================
Funzionalità:
  • RPC bidirezionale da ThingsBoard  → comandi motore
  • Telemetria sensori IR             → ThingsBoard ogni 5 s
  • Streaming MJPEG dalla Pi Camera   → /video_feed  (visibile in ThingsBoard
                                        tramite un widget HTML personalizzato)
  • REST API locale                   → /api/sensori, /cmd (compatibilità)
  • Swagger UI                        → /apidocs

Dipendenze extra:
  pip install flask flasgger paho-mqtt picamera2 opencv-python-headless
"""

from __future__ import annotations

import json
import threading
import time

import cv2
import paho.mqtt.client as mqtt
from flasgger import Swagger
from flask import Flask, Response, jsonify, render_template, request
from picamera2 import Picamera2

from AlphaBotV3 import AlphaBot

# ── AlphaBot ─────────────────────────────────────────────────────────────────
Ab = AlphaBot()
Ab.stop()
Ab.setPWMA(33)
Ab.setPWMB(33)

# ── Flask ─────────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SWAGGER"] = {"title": "AlphaBot API", "uiversion": 3}
swagger = Swagger(app)

# ── Camera (Picamera2 + OpenCV) ───────────────────────────────────────────────
picam2 = Picamera2()
picam2.configure(
    picam2.create_video_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
)
picam2.start()

_frame_lock = threading.Lock()
_latest_frame: bytes | None = None


def camera_capture_loop():
    """Thread dedicato: cattura frame e li comprime in JPEG."""
    global _latest_frame
    while True:
        frame = picam2.capture_array()
        # BGR per OpenCV (Picamera2 restituisce RGB)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ok, buf = cv2.imencode(
            ".jpg", frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 70]
        )
        if ok:
            with _frame_lock:
                _latest_frame = buf.tobytes()
        time.sleep(0.033)  # ~30 fps


threading.Thread(target=camera_capture_loop, daemon=True).start()


def generate_mjpeg():
    """Generatore per lo stream MJPEG."""
    boundary = b"--frame"
    while True:
        with _frame_lock:
            frame = _latest_frame
        if frame:
            yield (
                boundary
                + b"\r\nContent-Type: image/jpeg\r\n\r\n"
                + frame
                + b"\r\n"
            )
        time.sleep(0.033)


# ── ThingsBoard MQTT ──────────────────────────────────────────────────────────
THINGSBOARD_HOST = "127.0.0.1"
ACCESS_TOKEN     = "vUm2R5zjmxUiX40Ez775"
TELEMETRY_TOPIC  = "v1/devices/me/telemetry"
RPC_REQUEST_TOPIC    = "v1/devices/me/rpc/request/+"
RPC_RESPONSE_TOPIC   = "v1/devices/me/rpc/response/{}"
PUBLISH_INTERVAL = 5   # secondi

mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(ACCESS_TOKEN)

# ── Gestione comandi motore ───────────────────────────────────────────────────
_SPEED_DEFAULT = 50
_SPEED_TURN    = 35


def execute_command(cmd: str, speed: int = _SPEED_DEFAULT) -> str:
    """Esegue un comando di movimento e restituisce una stringa di stato."""
    cmd = cmd.upper()
    Ab.stop()

    if cmd == "FORWARD":
        Ab.setPWMA(speed)
        Ab.setPWMB(speed)
        Ab.forward()
    elif cmd == "BACKWARD":
        Ab.setPWMA(speed)
        Ab.setPWMB(speed)
        Ab.backward()
    elif cmd == "LEFT":
        Ab.setPWMA(_SPEED_TURN)
        Ab.setPWMB(_SPEED_TURN)
        Ab.left()
    elif cmd == "RIGHT":
        Ab.setPWMA(_SPEED_TURN)
        Ab.setPWMB(_SPEED_TURN)
        Ab.right()
    elif cmd == "STOP":
        Ab.stop()
    elif cmd == "CERCHIO":
        threading.Thread(target=Ab.cerchio, daemon=True).start()
    elif cmd == "QUADRATO":
        threading.Thread(target=Ab.quadrato, daemon=True).start()
    elif cmd == "TRIANGOLO":
        threading.Thread(target=Ab.triangolo, daemon=True).start()
    else:
        return f"unknown_command:{cmd}"

    return f"ok:{cmd}"


# ── Callback MQTT ─────────────────────────────────────────────────────────────

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connesso a ThingsBoard")
        # Sottoscrizione ai topic RPC server-side
        client.subscribe(RPC_REQUEST_TOPIC)
        print(f"[MQTT] Subscribed to {RPC_REQUEST_TOPIC}")
    else:
        print(f"[MQTT] Errore connessione: rc={rc}")


def on_message(client, userdata, msg):
    """
    Gestisce i comandi RPC inviati da ThingsBoard.

    Formato atteso del payload:
      { "method": "setCommand", "params": { "cmd": "FORWARD", "speed": 50 } }
      oppure
      { "method": "getStatus", "params": {} }
    """
    try:
        # Estrai l'ID richiesta dal topic  v1/devices/me/rpc/request/{id}
        request_id = msg.topic.split("/")[-1]
        payload    = json.loads(msg.payload.decode())
        method     = payload.get("method", "")
        params     = payload.get("params", {})

        print(f"[RPC] {method} params={params}")

        if method == "setCommand":
            cmd   = params.get("cmd", "STOP")
            speed = int(params.get("speed", _SPEED_DEFAULT))
            result = execute_command(cmd, speed)
            response = {"result": result}

        elif method == "getStatus":
            response = {
                "result": {
                    "sensore_sinistro": Ab.left_sensor(),
                    "sensore_destro":   Ab.right_sensor(),
                }
            }

        else:
            response = {"error": f"unknown method: {method}"}

        # Pubblica risposta RPC
        resp_topic = RPC_RESPONSE_TOPIC.format(request_id)
        client.publish(resp_topic, json.dumps(response), qos=1)

    except Exception as exc:
        print(f"[RPC] Eccezione: {exc}")


def on_publish(client, userdata, mid):
    print(f"[MQTT] Pubblicato mid={mid}")


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_publish = on_publish

mqtt_client.connect(THINGSBOARD_HOST, 1883, 60)
mqtt_client.loop_start()


# ── Thread telemetria sensori ─────────────────────────────────────────────────

def sensor_publisher():
    while True:
        try:
            payload = {
                "sensore_sinistro": Ab.left_sensor(),
                "sensore_destro":   Ab.right_sensor(),
            }
            result = mqtt_client.publish(
                TELEMETRY_TOPIC, json.dumps(payload), qos=1
            )
            print(f"[MQTT] Telemetria: {payload}  rc={result.rc}")
        except Exception as exc:
            print(f"[MQTT] Errore telemetria: {exc}")
        time.sleep(PUBLISH_INTERVAL)


threading.Thread(target=sensor_publisher, daemon=True).start()


# ── Route Flask ───────────────────────────────────────────────────────────────

@app.route("/video_feed")
def video_feed():
    """
    Stream MJPEG della Pi Camera.
    Usato nel widget HTML di ThingsBoard tramite un tag <img>.
    ---
    responses:
      200:
        description: Stream MJPEG continuo
        content:
          multipart/x-mixed-replace:
            schema:
              type: string
              format: binary
    """
    return Response(
        generate_mjpeg(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@app.route("/api/sensori", methods=["GET"])
def leggi_sensori():
    """
    Lettura sensori IR AlphaBot
    ---
    responses:
      200:
        description: Stato sensori sinistro e destro
        schema:
          type: object
          properties:
            sensore_sinistro:
              type: boolean
            sensore_destro:
              type: boolean
    """
    return jsonify(
        {
            "sensore_sinistro": Ab.left_sensor(),
            "sensore_destro":   Ab.right_sensor(),
        }
    )


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/cmd", methods=["POST"])
def cmd():
    """
    Invia un comando di movimento (compatibilità con il frontend locale)
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            cmd:
              type: string
              example: START_W
    responses:
      200:
        description: Stato esecuzione
    """
    data    = request.get_json()
    command = (data or {}).get("cmd", "")

    if not command:
        return jsonify({"status": "no command"})

    print(f"[HTTP] Comando: {command}")

    if command == "STOP":
        execute_command("STOP")
    elif command.startswith("START_"):
        key_map = {"W": "FORWARD", "S": "BACKWARD", "A": "LEFT", "D": "RIGHT"}
        key = command.split("_", 1)[-1]
        execute_command(key_map.get(key, "STOP"))

    return jsonify({"status": "ok"})


# ── Avvio ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
    finally:
        Ab.stop()
        picam2.stop()
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("[APP] Shutdown completato")