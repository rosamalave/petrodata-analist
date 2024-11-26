import psycopg2
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from datetime import datetime
from decimal import Decimal
import sys

# Conexión a PostgreSQL

class base_ddatos():

    def __init__(self):

        #objeto de tipo conexion que guarda metodos: cursor, commit, rollback, close
        self.conn = psycopg2.connect(host="localhost", database="juninpruebas", user="postgres", password="Junindata" )

    def insertar(self,producto,nuevaf,esquema,tabla):
        cursor=self.conn.cursor()
        print(nuevaf)
        
        self.conversionformatotabla(cursor, nuevaf,esquema,tabla)
    
        #extrayendo headers en una cadena
        nombres=[]
        headers=self.header(cursor,nombres,esquema,tabla)
                
        #extrayendo datos en una cadena
        #def agregar datos/editar validar nuevaf
        datos=""
        for col in nuevaf:
            datos=datos+col+", "
        if datos.endswith(", "):
            datos = datos[:-2]

        cursor.execute(f"INSERT INTO {esquema}.{tabla}({headers}) VALUES({datos})")
        self.conn.commit()
        cursor.close()

        #usada para editar e insertar informacion de 0 (puede ser la misma funcion)
        
    def eliminar(self,id,esquema,tabla):
        cursor=self.conn.cursor()
        id=self.buscar(cursor,id,esquema,tabla)
        if id != -1:
            cursor.execute(f"DELETE * FROM {esquema}.{tabla} WHERE id_{tabla} = {id}")
        self.conn.commit()
        cursor.close()
        
    def editar(self, id, producto, nuevaf, esquema, tabla):
    
        #Edita una fila en la base de datos actualizando todos los campos de la tabla, incluso los no editados.

        cursor = self.conn.cursor()
    
        # Asegurarse de que los datos estén en el formato adecuado para la tabla
        self.conversionformatotabla(cursor, nuevaf, esquema, tabla)

        # Extraer los nombres de las columnas (header)
        nombres = []
        self.header(cursor, nombres, esquema, tabla)  # nombres contendrá los encabezados de la tabla

        # Generar la cadena dinámica para el SET usando comprensión de listas y `join`
        campos_set = ", ".join([f"{col} = %s" for col in nombres])

        # Verificar si el registro con `id` existe en la tabla
        if self.buscar(cursor, id, esquema, tabla):
            # Construir y ejecutar la consulta dinámica
            query = f"UPDATE {esquema}.{tabla} SET {campos_set} WHERE id_{tabla} = %s"
            print(f"Ejecutando consulta: {query}")
            # Ejecutar la consulta con parámetros seguros
            cursor.execute(query, nuevaf + [id])

        # Guardar los cambios en la base de datos
        self.conn.commit()
        cursor.close()


    def buscar(self,cursor,id,esquema,tabla):
        cursor.execute(f"SELECT * FROM {esquema}.{tabla} WHERE id_{tabla} = {id}")
        if cursor.rowcount == 0 or cursor.rowcount ==-1:
            print("fila no existe.")
            return -1
        else:
            return id
        
    def conversionformatotabla(self, cursor, nuevaf, esquema, tabla):
        cursor.execute(f"SELECT data_type FROM information_schema.columns WHERE table_schema = '{esquema}' AND table_name = '{tabla}' AND column_name NOT LIKE 'id%'")
        bdtype = cursor.fetchall()
        print(f"Fila seleccionada: {nuevaf}")
        print(f"bdtype: {bdtype}")
    
        j = 0
        for i in range(len(nuevaf)):
            tipo_dato = bdtype[j][0]  # Extrae el tipo de dato desde la tupla
            print(f"Tipo de dato de columna {i} en {j}: {tipo_dato}")
            if i == j:
                if tipo_dato == 'date':  # Si el tipo es 'date'
                    if isinstance(nuevaf[i], str):  # Convierte solo si es cadena
                        nuevaf[i] = datetime.strptime(nuevaf[i], "%Y-%m-%d").date()
                elif tipo_dato == 'bigint':  # Si el tipo es 'bigint'
                    nuevaf[i] = int(nuevaf[i]) if not isinstance(nuevaf[i], int) else nuevaf[i]
                elif tipo_dato == 'numeric':  # Si el tipo es 'numeric'
                    nuevaf[i] = Decimal(nuevaf[i]) if not isinstance(nuevaf[i], Decimal) else nuevaf[i]
            j += 1

        #nocierracursor
        #nuevaf vector a insertar
        #bdtype tupla con tipos de datos       

    def header(self,cursor,nombres,esquema,tabla):
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{esquema}' AND table_name = '{tabla}' AND column_name NOT LIKE 'id%'")

        #extrayendo headers en un vector
        for col in cursor.fetchall():
            nombres.append(str(col[0]))

        #extrayendo headers en una cadena
        cadenanombres=""
        for col in nombres:
            cadenanombres=cadenanombres+col+", "

        return cadenanombres[:-2]
    
        #nocierra cursor
        #modifica vector nombres
        #retorna en un string el vector nombres
