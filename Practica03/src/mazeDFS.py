"""
PRACTICA 03: Explorador de laberinto con algoritmo DFS


El labrinto tiene las siguientes especificaciones
* 0 es un espacio libre
* 1 es un obstáculo (unico)
* E es la entrada del laberinto
* S es la salida del laberinto
"""

import gym
from gym import spaces

# Representar el entorno del laberinto
class Maze(gym.Env):

    def __init__(self, maze):
        super(Maze, self).__init__()
        self.maze = maze  # Almacena el laberinto
        self.height = len(maze)  # Almacena la altura del laberinto
        self.width = len(maze[0])  # Almacena la anchura del laberinto
        self.action_space = spaces.Discrete(4)  # Espacio de acción del agente: arriba, abajo, izquierda, derecha
        self.observation_space = spaces.Discrete(self.height * self.width)  # Espacio de observación (posibles estados que el agente puede observar del entorno)
        self.agent_pos = None  # Posición inicial 
        self.done = False  # Indica si el recorrido ha terminado (interacciones entre el agente y el entorno )
    
    # Reinicia el entorno a su estado inicial y devuelve la posición inicial del agente.
    def reset(self):
        self.agent_pos = self.find_start() # Se busca la posición de inicio en el laberinto
        self.done = False  # Reinicia el estado de finalización del recorrido
        return self.agent_pos

    # Toma una acción y se mueve un paso en el entorno.
    def step(self, action):
        if self.done:
            # Si el recorrido ya ha terminado, regresamos a la posición actual
            return self.agent_pos, 0, True, {}

        x, y = self.agent_pos

        # Movimientos posibles: arriba, abajo, izquierda, derecha
        if action == 0 and x > 0 and self.maze[x - 1][y] != 1:
            print("Movimiento: arriba")
            x -= 1
        elif action == 1 and x < self.height - 1 and self.maze[x + 1][y] != 1:
            print("Movimiento: abajo")
            x += 1
        elif action == 2 and y > 0 and self.maze[x][y - 1] != 1:
            print("Movimiento: izquierda")
            y -= 1
        elif action == 3 and y < self.width - 1 and self.maze[x][y + 1] != 1:
            print("Movimiento: derecha")
            y += 1

        self.agent_pos = (x, y)

        # Verifica si la posición en la que se encuentra es la salida
        if self.maze[x][y] == "S":
            self.done = True

        return self.agent_pos, 0, self.done, {}
    
    # Encuentra la posición inicial del agente (entrada del laberinto).
    def find_start(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == "E":
                    return (i, j)
        return None # Solucionando caso donde no encuentre la entrada

# Encuentra la salida usando backtracking
def solve(env):
    actions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # arriba, abajo, izquierda, derecha

    def backtrack(x, y, path):
        if x < 0 or x >= env.height or y < 0 or y >= env.width or env.maze[x][y] == 1 or (x, y) in path:
            return False

        path.append((x, y))

        if env.maze[x][y] == "S":
            print("Encontré la salida :D")
            return True

        for action in range(env.action_space.n):
            if backtrack(x + actions[action][0], y + actions[action][1], path):
                return True

        path.pop()
        return False

    start_x, start_y = env.find_start()
    path = []
    if backtrack(start_x, start_y, path):
        print("La ruta es:")
        for i, pos in enumerate(path):
            x, y = pos
            direction = ""
            if i > 0:
                # Comparar la posición actual con la anterior para determinar la dirección
                prev_pos = path[i - 1]
                if x < prev_pos[0]:
                    direction = "arriba"
                elif x > prev_pos[0]:
                    direction = "abajo"
                elif y < prev_pos[1]:
                    direction = "izquierda"
                elif y > prev_pos[1]:
                    direction = "derecha"
            print(f"Posición: {pos}, Dirección: {direction}")        
    else:
        print("iiiiii no encontré la salida")


# Laberinto 01 CON SOLUCIÓN
laberinto01 = [
    [  1, 0, 0, 0,   0, 0,   0, 0],
    [  0, 0, 1, 0,   1, 1,   0, 0],
    [  0, 0, 1, 1, "S", 1,   0, 1],
    [  0, 0, 0, 1,   0, 1,   0, 0],
    [  1, 0, 1, 1,   0, 0,   0, 0],
    [  0, 0, 0, 1,   1, 0,   0, 1],
    [  0, 1, 1, 1,   1, 1,   1, 0],
    [  0, 0, 0, 0,   0, 0, "E", 0]
]

# Laberinto 02 CON SOLUCIÓN
laberinto02 = [
    ["E", 0, 0,   0, 0, 0, 0, 0],
    [  0, 0, 1,   0, 1, 0, 1, 0],
    [  0, 0, 1,   0, 1, 0, 1, 1],
    [  0, 0, 0,   0, 1, 1, 1, 0],
    [  1, 0, 1,   1, 1, 1, 1, 0],
    [  0, 0, 0,   0, 0, 0, 0, 1],
    [  0, 1, 1,   1, 0, 0, 0, 0],
    [  0, 0, 0, "S", 0, 0, 1, 1]
]

# Laberinto 03 SIN SOLUCIÓN
# No hay camino
laberinto03 = [
    ["E", 1],
    [1, "S"]
]

# Laberinto 04 SIN SOLUCIÓN
# No hay salida
laberinto04 = [
    ["E", 0, 0, 0, 0, 0, 0, 0],
    [  0, 0, 1, 0, 1, 0, 1, 0],
    [  0, 0, 1, 0, 1, 0, 1, 1],
    [  0, 0, 0, 0, 1, 1, 1, 0],
    [  1, 0, 1, 1, 1, 1, 1, 0],
    [  0, 0, 0, 0, 0, 0, 0, 1],
    [  0, 1, 1, 1, 0, 0, 0, 0],
    [  0, 0, 0, 1, 0, 0, 1, 1]
]

# Laberinto 05 SIN SOLUCIÓN
# No hay entrada
laberinto05 = [
    [ 1, 0, 1, 0,   0, 0, 0, 0],
    [ 0, 0, 1, 0,   1, 0, 1, 0],
    [ 0, 0, 1, 0, "S", 0, 1, 1],
    [ 0, 0, 0, 0,   1, 1, 0, 0],
    [ 1, 0, 1, 1,   1, 1, 1, 0],
    [ 0, 0, 0, 0,   0, 0, 1, 0],
    [ 0, 1, 1, 1,   1, 1, 1, 0],
    [ 0, 0, 0, 0,   0, 0, 0, 0]
]

# switch para elegir entre laberitos predefinidos
def elegirLaberinto(nlaberinto):
    if nlaberinto == 1:
        return Maze(laberinto01)
    elif nlaberinto == 2:
        return Maze(laberinto02)
    elif nlaberinto == 3:
        return Maze(laberinto03)
    elif nlaberinto == 4:
        return Maze(laberinto04)
    elif nlaberinto == 5:
        return Maze(laberinto05)    
    else:
        raise ValueError("Laberinto no válido")

# Main del programa
def main():
    while True:
        try:
            nlaberinto = int(input("Seleccione un laberinto escribiendo el número [1, 2, 3, 4, 5]:  "))
            env = elegirLaberinto(nlaberinto)

             # Verifica si se encontró la entrada para el agente
            agent_pos = env.find_start()

            if agent_pos is None:
                print("No se encontró la entrada del agente en el laberinto.")
            else:
                solve(env) # Ejecutamos la solución al laberinto
            break

        except ValueError:
            print("Por favor, ingrese una opción válida:")

if __name__ == "__main__":
    main()