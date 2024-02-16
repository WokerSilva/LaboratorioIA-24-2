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

# Este es el nombre nuestro chatbot
chatbot = ChatBot("ChatDog")

# Cargar datos de entrenamiento desde el archivo JSON
#  los cuales cuales son almacenados en la variable "conversaciones"
with open('conversaciones.json', 'r') as file:
    conversaciones = json.load(file)

# Creamos el objeto entrenador de nuesto chatbot definido 
trainer = ListTrainer(chatbot)

# Iteramos entre los datos del JSON para entrenar las 
#  respuestas futuras del chatbot
for conversation in conversaciones['conversaciones']:
    trainer.train(conversation)


@app.route("/") # Definimos la ruta raiz para la appweb
def home():     #  donde buscamos el archivo html
    return render_template("index.html")


# Dentro de la web solo se aceptan solicitudes POST
# Para eso es el metodo get_bot_response(), dodne:
#  - Se obtiene lo que escribe el usuario
#  - si se escribio algo, el chat se encarga 
#     de leerlo y dar la respuesta
#  - si no da un mensaje de error
#  - Finalmente se devuelve lo generado 
@app.route("/get", methods=["POST"])
def get_bot_response():
    entrada_usuario = request.form.get('msg', '')  # Obtener el texto del mensaje del formulario
    if entrada_usuario:
        response = str(chatbot.get_response(entrada_usuario))
    else:
        response = "Ingrese texto valido"

    response = response.encode('latin1').decode('utf-8')

    return jsonify({'response': response})


if __name__ == "__main__":
    app.run(debug=True)

## NOTA : eliminar la base de datos generada para reiniciar el aprendizaje