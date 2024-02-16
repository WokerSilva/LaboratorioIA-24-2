###
#### Chat Dog
### 

# Para desarrollo web
#  - Renderizar templates HTML : render_template
#  - Solicitudes HTTP          : request
#  - Trabajar JSON             : jsonify
from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
# Entrenamiento con conversaciones predefinidas
from chatterbot.trainers import ListTrainer
import json


# Inicializamos la  instancia para flask
#  pasandole como argumento "name" (predeterminada)
app = Flask(__name__)

# Crear varios ChatBot con distintos
#  nombres para su entrenamiento especifico 
chatbots = {
    'dog': ChatBot("DogBot", storage_adapter="chatterbot.storage.SQLStorageAdapter",
                   database_uri="sqlite:///dogbot_database.sqlite3"),
    'cat': ChatBot("CatBot", storage_adapter="chatterbot.storage.SQLStorageAdapter",
                   database_uri="sqlite:///catbot_database.sqlite3")
}

# A partir de los diferentes archivos con las conversaciones 
#  asignamos cada chatbot a su respectivo archivo
with open('conver-dog.json', 'r') as file:
    conversaciones_dog = json.load(file)

with open('conver-cat.json', 'r') as file:
    conversaciones_cat = json.load(file)

# Como trabajamos con distintos chat y archivos 
#  no podía ser diferente que cada uno tendía su 
#  propio entrenamiento con la importación ListTrainer
trainers_dog = ListTrainer(chatbots['dog'])
trainers_cat = ListTrainer(chatbots['cat'])

# Iteramos entre los datos del JSON para cargar las 
#  respuestas del chatbot
for conversation in conversaciones_dog['conversations']:
    trainers_dog.train(conversation)

for conversation in conversaciones_cat['conversations']:
    trainers_cat.train(conversation)


@app.route('/') # Definimos la ruta raiz para la appweb
def home():     #  donde buscamos el archivo html
    return render_template('index.html')

# Asignar la ruta para manejar las solicitudes POST del usuario
@app.route('/get', methods=['POST'])
def get_bot_response():
    entrada_usuario = request.form['msg']
    bots = request.form.get('bot', 'dog')      # Opciones del bot
    bot = chatbots.get(bots, chatbots['dog'])  # Bot predefinido
    respuesta = str(bot.get_response(entrada_usuario))
    return jsonify({'response': respuesta})

if __name__ == '__main__':
    app.run(debug=True)