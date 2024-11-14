import psycopg2
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

# Conexión a PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="PETROJUNIN_DATA",
    user="postgre",
    password="Junindata"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM public.produccion_c")

# Ejemplo de cómo llenar la QTableWidget con datos
rows = cursor.fetchall() #almacenando cada fila en tuplas (datos de tantas dimensiones como columnas tenga la tabla)

tabla_produccion = QTableWidget()
tabla_produccion.setRowCount(len(rows))
tabla_produccion.setColumnCount(len(rows[0]))  # Asume que cada fila tiene el mismo número de columnas

for i, row in enumerate(rows):
    for j, col in enumerate(row):
        tabla_produccion.setItem(i, j, QTableWidgetItem(str(col)))

conn.close()
