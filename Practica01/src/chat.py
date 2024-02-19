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
    'perro': ChatBot("perroBot"),
    'gato': ChatBot("gatoBot"),
    'veterinaria': ChatBot("VeterinariaBot"),
    'vacante': ChatBot("VacanteBot"),
    'dCurioso': ChatBot("DCuriosoBot")
}

# A partir de los diferentes archivos con las conversaciones 
#  asignamos cada chatbot a su respectivo archivo
with open('conversaciones\conver-perro.json', 'r') as file:
    conversaciones_perro = json.load(file)

with open('conversaciones\conver-gato.json', 'r') as file:
    conversaciones_gato = json.load(file)

with open('conversaciones\conver-veterinaria.json', 'r') as file:
    conversaciones_veterinaria = json.load(file)

with open('conversaciones\conver-dCurioso.json', 'r', encoding='utf-8') as file:
    conversaciones_dCurioso = json.load(file)

with open('conversaciones\conver-vacante.json', 'r') as file:
    conversaciones_vacante = json.load(file)

# Como trabajamos con distintos chat y archivos 
#  no podía ser diferente que cada uno tendía su 
#  propio entrenamiento con la importación ListTrainer
trainers_perro = ListTrainer(chatbots['perro'])
trainers_gato = ListTrainer(chatbots['gato'])
trainers_vacante = ListTrainer(chatbots['vacante'])
trainers_veterinaria = ListTrainer(chatbots['veterinaria'])
trainers_dCurioso = ListTrainer(chatbots['dCurioso'])

# Iteramos entre los datos del JSON para cargar las 
#  respuestas del chatbot
for conversation in conversaciones_perro['conversations']:
    trainers_perro.train(conversation)

for conversation in conversaciones_gato['conversations']:
    trainers_gato.train(conversation)

for conversation in conversaciones_veterinaria['conversations']:
    trainers_veterinaria.train(conversation)

for conversation in conversaciones_dCurioso['conversations']:
    trainers_dCurioso.train(conversation)

for conversation in conversaciones_vacante['conversations']:
    trainers_vacante.train(conversation)

@app.route('/') # Definimos la ruta raiz para la appweb
def home():     #  donde buscamos el archivo html
    return render_template('index.html')

# Asignar la ruta para manejar las solicitudes POST del usuario
@app.route('/get', methods=['POST'])
def get_bot_response():
    entrada_usuario = request.form['msg']
    bot_type = request.form.get('bot', 'perro')  # Valor predeterminado: 'perro'
    if bot_type not in ['perro', 'gato', 'vacante', 'veterinaria', 'dCurioso']:
        # Si el valor no está en la lista de opciones válidas, establecer 'perro' como bot predeterminado
        bot_type = 'perro'
    
    # Obtener el bot correspondiente o utilizar el predeterminado (perroBot)
    bot = chatbots.get(bot_type, chatbots['perro'])
    
    # Verificar si la entrada del usuario está vacía
    if not entrada_usuario:
        # Respuesta predeterminada para cadenas vacías
        respuesta = "Por favor, ingresa algo para que pueda ayudarte."
    else:
        # Obtener respuesta del chatbot
        respuesta = str(bot.get_response(entrada_usuario))
        
        # Si la respuesta es similar a la entrada del usuario, es probable que el bot no haya entendido la pregunta
        if respuesta.lower() == entrada_usuario.lower():  # Comparamos en minúsculas para ser menos sensibles a las diferencias de mayúsculas y minúsculas            
            respuesta = "Lo siento, no logré entender tu pregunta. ¿Podrías reformularla?"

    respuesta = respuesta.encode('latin1').decode('utf-8')

    return jsonify({'response': respuesta})


if __name__ == '__main__':
    app.run(debug=True)