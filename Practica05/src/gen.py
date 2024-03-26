import random

# Constantes
TABLERO = 15
POBLACION_INICIAL = 10
GENERACIONES = 120
C = 1  # Velocidad de la luz (celda por generación)


# Función para inicializar la población
def inicializar_poblacion(tamano):
    poblacion = []
    for _ in range(tamano):
        cromosoma = [random.randint(0, 1) for _ in range(TABLERO**2)]
        poblacion.append(cromosoma)
    return poblacion

# Función para calcular el desplazamiento de las naves espaciales
def calcular_desplazamiento(cromosoma):
    # Implementación específica necesaria aquí
    return 0, 0, 1  # Ejemplo de valores de retorno

# Función fitness basada en la velocidad de las naves espaciales
def funcion_fitness(cromosoma):
    x, y, n = calcular_desplazamiento(cromosoma)
    v = max(abs(x), abs(y)) / n * C
    return v

# Función para aplicar las reglas del Juego de la Vida y evaluar el tablero
def evaluar_tablero(cromosoma, poblacion_actual, generacion_actual, umbral_poblacion=1, max_generaciones=115):
    tablero = [cromosoma[i:i+TABLERO] for i in range(0, len(cromosoma), TABLERO)]
    nuevo_tablero = [[0]*TABLERO for _ in range(TABLERO)]
    
    for i in range(TABLERO):
        for j in range(TABLERO):
            vecinos_vivos = contar_vecinos_vivos(tablero, i, j)
            if tablero[i][j] == 1:  # Si la célula está viva
                if vecinos_vivos < 2:
                    nuevo_tablero[i][j] = 0  # Muerte uno: muerte por soledad
                elif vecinos_vivos > 3:
                    if poblacion_actual >= umbral_poblacion and vecinos_vivos == 4:
                        nuevo_tablero[i][j] = 1  # Condición Especial de Supervivencia
                    else:
                        nuevo_tablero[i][j] = 0  # Muerte dos: muerte por sobrepoblación
                else:
                    nuevo_tablero[i][j] = 1  # Supervivencia Normal
            else:  # Si la célula está muerta
                if vecinos_vivos == 3:
                    nuevo_tablero[i][j] = 1  # Nacimientos
    
    # Convertir el nuevo tablero a un cromosoma para la siguiente generación
    nuevo_cromosoma = [celula for fila in nuevo_tablero for celula in fila]
    
    # Muerte tres: terminar el juego si no se alcanza el objetivo en 'n' generaciones
    if generacion_actual >= max_generaciones:
        return None  # Esto indicaría el fin del juego
    
    return nuevo_cromosoma

# Función para contar los vecinos vivos de una célula
def contar_vecinos_vivos(tablero, fila, columna):
    vecinos_vivos = 0
    for i in range(max(0, fila-1), min(fila+2, TABLERO)):
        for j in range(max(0, columna-1), min(columna+2, TABLERO)):
            if (i, j) != (fila, columna) and tablero[i][j] == 1:
                vecinos_vivos += 1
    return vecinos_vivos

# Función de selección por torneo
def seleccion_por_torneo(poblacion, aptitudes):
    seleccionados = []
    for _ in range(len(poblacion)):
        competidores = random.sample(list(enumerate(aptitudes)), 2)
        ganador = max(competidores, key=lambda item: item[1])
        seleccionados.append(poblacion[ganador[0]])
    return seleccionados

# Función de reproducción asexual
def reproduccion(seleccionados):
    hijos = []
    for padre in seleccionados:
        hijo = padre[:]  # Crear una copia del padre
        hijos.append(hijo)
    return hijos

# Función de mutación
def mutacion(hijos):
    mutados = []
    for hijo in hijos:
        if random.random() < 0.1:  # Probabilidad de mutación del 10%
            indice = random.randint(0, len(hijo) - 1)
            hijo[indice] = 1 if hijo[indice] == 0 else 0
        mutados.append(hijo)
    return mutados

# Función de reemplazo
def reemplazo(poblacion, mutados, aptitudes):
    # Reemplaza los peores ajustados con los nuevos mutados
    ordenados = sorted(zip(poblacion, aptitudes), key=lambda item: item[1], reverse=True)
    sobrevivientes = ordenados[:len(poblacion) - len(mutados)]
    nueva_poblacion = [individuo for individuo, _ in sobrevivientes] + mutados
    return nueva_poblacion


# Función para imprimir el tablero
def imprimir_tablero(cromosoma):
    tablero = [cromosoma[i:i+TABLERO] for i in range(0, len(cromosoma), TABLERO)]
    for fila in tablero:
        print(' '.join(['X' if celula == 1 else '-' for celula in fila]))
    print('\n')

# Método principal que ejecuta el algoritmo genético
def main():
    poblacion = inicializar_poblacion(POBLACION_INICIAL)
    poblacion_actual = len(poblacion)  # Asumiendo que poblacion_actual es la longitud de la población
    for generacion_actual in range(GENERACIONES):
        # Aplicar las reglas del juego y evaluar el tablero
        nueva_poblacion = []
        for cromosoma in poblacion:
            nuevo_cromosoma = evaluar_tablero(cromosoma, poblacion_actual, generacion_actual)
            if nuevo_cromosoma is not None:
                nueva_poblacion.append(nuevo_cromosoma)
        
        poblacion = nueva_poblacion
        if not poblacion:  # Si la población está vacía, terminar el juego
            print("El juego ha terminado debido a que no se alcanzaron los objetivos.")
            break

        # Imprimir el tablero cada 10 generaciones
        if generacion_actual % 10 == 0:
            imprimir_tablero(poblacion[0])

        # Calcular la aptitud de cada cromosoma basada en las naves espaciales
        aptitudes = [funcion_fitness(cromosoma) for cromosoma in poblacion]
        
        # Selección por torneo
        seleccionados = seleccion_por_torneo(poblacion, aptitudes)
        
        # Reproducción asexual
        hijos = reproduccion(seleccionados)
        
        # Mutación
        mutados = mutacion(hijos)
        
        # Reemplazo
        poblacion = reemplazo(poblacion, mutados, aptitudes)

      # Imprimir la generación final
    print(f"El programa terminó en la generación {generacion_actual + 1}")


if __name__ == "__main__":
    main()
