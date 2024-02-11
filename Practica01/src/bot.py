###
#### Chat Dog
### 

from chatterbot import ChatBot
# Entrenamiento con conversaciones predefinidas
from chatterbot.trainers import ListTrainer  
import json

chatbot = ChatBot("ChatDog")

# Cargar datos de entrenamiento desde el archivo JSON
#  los cuales cuales son almacenados en la variable "conver"
with open('conver.json', 'r') as file:
    conver = json.load(file)

# Creamos el objeto entrenador de nuesto chatbot definido 
trainer = ListTrainer(chatbot)

# Iteramos entre los datos del JSON para entrenar las 
#  respuestas futuras del chatbot
for conversation in conver['conversations']:
    trainer.train(conversation)

# Entramos a un bucle donde se pide al usuario la entrada
#  la variable hace la verificación para saber si debe salir
#  de lo contrario se llama al metodo para obtener respuestas
exit_conditions = (":q", "quit", "exit")
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print(f"🐶 {chatbot.get_response(query)}")

## NOTA : eliminar la base de datos generada para reiniciar el aprendizaje