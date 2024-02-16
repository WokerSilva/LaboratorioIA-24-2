from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

# Crear múltiples instancias de ChatBot
chatbots = {}

# Asociar cada instancia de ChatBot con un archivo JSON diferente
chatbots['dog'] = ChatBot("DogBot")
chatbots['cat'] = ChatBot("CatBot")

# Cargar datos de entrenamiento desde archivos JSON diferentes para cada ChatBot
with open('conver-dog.json', 'r') as file:
    conversaciones_dog = json.load(file)

with open('conver-cat.json', 'r') as file:
    conversaciones_cat = json.load(file)

# Crear entrenadores para cada instancia de ChatBot
trainers_dog = ListTrainer(chatbots['dog'])
trainers_cat = ListTrainer(chatbots['cat'])

# Entrenar cada ChatBot con los datos correspondientes
for conversation in conversaciones_dog['conversations']:
    trainers_dog.train(conversation)

for conversation in conversaciones_cat['conversations']:
    trainers_cat.train(conversation)

# Definir las condiciones de salida
exit_conditions = (":q", "quit", "exit")

while True:
    query = input("> ")

    # Switch para determinar qué ChatBot utilizar basándose en la entrada del usuario
    if query.startswith("dog"):
        bot = chatbots['dog']
    elif query.startswith("cat"):
        bot = chatbots['cat']
    else:
        # Si no se especifica ningún bot, se utiliza uno predeterminado (en este caso, DogBot)
        bot = chatbots['dog']

    # Salir del bucle si se ingresa una condición de salida
    if query in exit_conditions:
        break
    else:
        # Obtener una respuesta del ChatBot correspondiente
        print(f"🐶 {bot.get_response(query)}")
