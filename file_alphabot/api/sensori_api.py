from AlphaBotV3 import AlphaBot
from flask import Flask, jsonify
from flasgger import Swagger

# Inizializza robot
Ab = AlphaBot()
Ab.stop()  # sicurezza: fermo all'avvio

# Flask
app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/sensori', methods=['GET'])
def leggi_sensori():
    """
    Lettura sensori AlphaBot
    ---
    responses:
      200:
        description: Stato sensori
    """
    left = Ab.left_sensor()
    right = Ab.right_sensor()

    return jsonify({
        "sensore_sinistro": left,
        "sensore_destro": right
    })

if __name__ == '__main__':
    print("API attiva su: http://127.0.0.1:5000/apidocs/")
    app.run(host='0.0.0.0', port=5000, debug=True)
