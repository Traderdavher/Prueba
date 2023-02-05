from FuturosBot import FuturosBot
from flask import Flask
from flask import request


app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p>Hello, World! - David</p>"

@app.route('/acerca')
def acerca():
    return "<p>David Herrera 3115550102</p>"


@app.route('/bot', methods=['POST'])
def bot():
    parametro = str(request.data, 'UTF-8').lower()
    
    bot = FuturosBot()
    bot.Entrar (parametro)
    return {
        "Funciono" : "Juliana con Exito"
    }
    

