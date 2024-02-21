# -*- coding: utf-8 -*-
"""
PRACTICA 02: Agentes Inteligentes

El labrinto tiene las siguientes especificaciones
* 0 es un espacio libre
* 1 es un obstáculo
* E es la entrada del laberinto
* S es la salida del laberinto
"""

import gym
from gym import spaces
import numpy as np

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
        self.done = False  # Indica si el episodio ha terminado (interacciones entre el agente y el entorno )
    
    # Reinicia el entorno a su estado inicial y devuelve la posición inicial del agente.
    def reset(self):
        self.agent_pos = self.find_start() # Se busca la posición de inicio en el laberinto
        self.done = False  # Reinicia el estado de finalización del episodio
        return self.agent_pos

    # Toma una acción y se mueve un paso en el entorno.
    def step(self, action):
        if self.done:
            # Si el episodio ya ha terminado, regresamos a la posición actual
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
        raise ValueError("No se pudo encontrar el punto de inicio 'E' en el laberinto")

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

if __name__ == "__main__":
    maze = [
    ["E", 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, "S", 0],
    [1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

    env = Maze(maze)
    solve(env)


