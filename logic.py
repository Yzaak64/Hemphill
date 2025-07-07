# ===================================================================================
# logic.py
# Contiene las funciones de cálculo para procesar las respuestas.
# ===================================================================================

import pandas as pd
from config import nombres_dimensiones, dimensiones_items, clave_puntuacion, tabla_estaninas

def calculate_scores_from_answers(all_answers):
    """Convierte una lista de 150 respuestas (1-5) a un DataFrame de resultados."""
    map_num_to_char = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}
    respuestas_char = [map_num_to_char[r] for r in all_answers]
    puntuaciones_brutas = {dim: 0 for dim in nombres_dimensiones.keys()}
    puntuaciones_directas = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1}
    puntuaciones_inversas = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
    for i, respuesta_char in enumerate(respuestas_char):
        item_num, dim, tipo = i + 1, dimensiones_items.get(i + 1), clave_puntuacion.get(i + 1)
        if tipo is None or dim is None: continue # Ignora items sin configuración
        puntuacion = puntuaciones_directas[respuesta_char] if tipo == 'directo' else puntuaciones_inversas[respuesta_char]
        puntuaciones_brutas[dim] += puntuacion
    return calculate_stanine(puntuaciones_brutas)

def calculate_stanine(puntuaciones_brutas):
    """Convierte un diccionario de puntuaciones crudas a un DataFrame de estaninas."""
    puntuaciones_estaninas = {}
    for dimension, puntaje_bruto in puntuaciones_brutas.items():
        tabla = tabla_estaninas.get(dimension, {})
        estanina_encontrada = 'N/A'
        for estanina, (min_val, max_val) in tabla.items():
            if min_val <= puntaje_bruto <= max_val:
                estanina_encontrada = estanina
                break
        puntuaciones_estaninas[dimension] = estanina_encontrada
    return pd.DataFrame({
        'Dimensión': [nombres_dimensiones[d] for d in puntuaciones_brutas.keys()], 
        'Puntuación Cruda': list(puntuaciones_brutas.values()), 
        'Puntuación Estanina': list(puntuaciones_estaninas.values())
    })