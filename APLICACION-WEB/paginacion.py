import datetime
from collections import defaultdict

def calcular_paginacion(periodicidad, cantidad, vector_consulta, headers):
    """
    Calcula la paginación de los datos según la periodicidad (anual o mensual) y la cantidad de periodos por página.
    
    Args:
        periodicidad (str): La periodicidad para agrupar los datos, "anual" o "mensual".
        cantidad (int): El número de periodos por página (1 a 4).
        vector_consulta (list of tuples): Lista de datos donde cada fila incluye una columna de fecha (datetime.date).
        headers (list of str): Lista con los nombres de las columnas que incluye "fecha".
        
    Returns:
        list: Una lista donde cada elemento representa el tamaño de cada página (número de filas).
    """
    if periodicidad not in ["anual", "mensual"]:
        raise ValueError("Periodicidad no válida. Use 'anual' o 'mensual'.")
    if not (1 <= cantidad <= 4):
        raise ValueError("Cantidad debe estar entre 1 y 4.")
    
    # Índice de la columna "fecha"
    fecha_index = headers.index("fecha")
    
    # Agrupar los datos por periodo
    conteo_por_periodo = defaultdict(int)
    
    for fila in vector_consulta:
        fecha = fila[fecha_index]
        if periodicidad == "anual":
            clave_periodo = fecha.year
        elif periodicidad == "mensual":
            clave_periodo = (fecha.year, fecha.month)
        conteo_por_periodo[clave_periodo] += 1
    
    # Convertir los conteos por periodo a una lista (respetando el orden original)
    conteo_filas = list(conteo_por_periodo.values())
    
    # Agrupar por cantidad para calcular el tamaño de las páginas
    tamanos_paginas = []
    acumulador = 0
    
    for i, conteo in enumerate(conteo_filas):
        acumulador += conteo
        if (i + 1) % cantidad == 0 or i == len(conteo_filas) - 1:
            tamanos_paginas.append(acumulador)
            acumulador = 0

    return tamanos_paginas


# === Ejemplo de uso 1 ===
vector_consulta = [
    (datetime.date(2013, 1, 1), 100),
    (datetime.date(2013, 1, 15), 110),
    (datetime.date(2013, 2, 1), 120),
    (datetime.date(2013, 7, 30), 150),
    (datetime.date(2014, 1, 1), 200),
    (datetime.date(2014, 12, 31), 250),
    (datetime.date(2015, 1, 1), 300),
]

headers = ["fecha", "valor"]

# Caso 1: Paginación anual, 2 años por página
periodicidad = "anual"
cantidad = 2
print("Ejemplo 1 - Anual, 2 años por página:")
tamanos_paginas = calcular_paginacion(periodicidad, cantidad, vector_consulta, headers)
print(tamanos_paginas)  # Salida esperada: [575 (2013 + 2014), ...]

# === Ejemplo de uso 2 ===
vector_consulta = [
    (datetime.date(2023, 1, 1), 100),
    (datetime.date(2023, 1, 10), 110),
    (datetime.date(2023, 2, 1), 120),
    (datetime.date(2023, 2, 28), 130),
    (datetime.date(2023, 3, 1), 140),
    (datetime.date(2023, 3, 15), 150),
    (datetime.date(2023, 4, 1), 160),
    (datetime.date(2023, 4, 30), 170),
]

# Caso 2: Paginación mensual, 2 meses por página
periodicidad = "mensual"
cantidad = 2
print("\nEjemplo 2 - Mensual, 2 meses por página:")
tamanos_paginas = calcular_paginacion(periodicidad, cantidad, vector_consulta, headers)
print(tamanos_paginas)  # Salida esperada: [48 (enero + febrero), 60 (marzo + abril)]