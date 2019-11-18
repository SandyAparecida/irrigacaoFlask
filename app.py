import RPi.GPIO as gpio
from flask import Flask, render_template
# Corrigir problema de requisicao de um localhost para um endereco da raspberwwy wlan
from flask_cors import CORS

app = Flask(__name__)

# Corrigir problema de requisicao de um localhost para um endereco da raspberwwy wlan
CORS(app)

# Meu ################################

import RPi.GPIO as gpio
import time

# Forma que queremos identificar cada porta. Numero fisico ou bcm. Pode ser BCM ou BOARD
gpio.setmode(gpio.BOARD)

pin_umidade = 37
gpio.setup(pin_umidade, gpio.IN)

pin_irrigacao_cenoura = 38
gpio.setup(pin_irrigacao_cenoura, gpio.OUT)
gpio.output(pin_irrigacao_cenoura, 0)

pin_irrigacao_alface = 36
gpio.setup(pin_irrigacao_alface, gpio.OUT)
gpio.output(pin_irrigacao_alface, 0)


def rc_time(pin):
    cont = 0
    # Definindo pino de saida
    gpio.setup(pin, gpio.OUT)
    # Definindo estado como desligado
    gpio.output(pin, gpio.LOW)
    time.sleep(0.1)
    # Mudar o pino para entrada
    gpio.setup(pin, gpio.IN)

    while (gpio.input(pin) == gpio.LOW):
        cont += 1
        valor_convertido = int(cont / 10000)
        if valor_convertido >= 100:
            return str(valor_convertido)
    return str(valor_convertido)


def sensor_umidade(pin_umidade):
    if gpio.input(pin_umidade) == gpio.HIGH:
        return "Seco"
    else:
        return "Úmido"


def lampada_quarto_status(pin_lampada_quarto):
    return str(gpio.input(pin_lampada_quarto))


@app.route('/')
def index():
    templateData = {
        'title': 'Sensor de luminosidade LDR',
    }
    return render_template('index.html', **templateData)


# Sensor umidade
@app.route('/get-umidade')
def get_umidade():
    return sensor_umidade(pin_umidade)


# Rele
@app.route('/set-irrigacao-cenoura/<estado>', methods=['GET'])
def set_irrigacao_cenoura(estado):
    estado = int(estado)
    gpio.output(int(pin_irrigacao_cenoura), int(estado))
    print("Cenoura")
    if estado == 0:
        return "Ligado"
    if estado == 1:
        return "Desligado"
    else:
        return "Estado Inexistente"

    return "Feito"


# Rele
@app.route('/set-irrigacao-alface/<estado>', methods=['GET'])
def set_irrigacao_alface(estado):
    estado = int(estado)
    gpio.output(int(pin_irrigacao_alface), int(estado))
    print("Alface")
    if estado == 0:
        return "Ligado"
    if estado == 1:
        return "Desligado"
    else:
        return "Estado Inexistente"

    return "Feito"


@app.route('/get-lampada-quarto-status')
def get_lampada_quarto_status():
    return lampada_quarto_status(pin_lampada_quarto)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
