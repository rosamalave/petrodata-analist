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
        
    def eliminar(self,esquema,tabla):
        cursor=self.conn.cursor()
        id=self.buscar
        if id != -1:
            cursor.execute(f"DELETE * FROM {esquema}.{tabla} WHERE id_{tabla} = {id}")
        self.conn.commit()
        cursor.close()
        
    def editar (self,producto,nuevaf,esquema,tabla):
        #sirve recibiendo de nuevo toda la fila completa y cambiando todos los campos
        #-incluso los no editados
        cursor=self.conn.cursor()
        self.conversionformatotabla(cursor, nuevaf,esquema,tabla)

        #header en vector
        nombres=[]
        #extrayendo header en una cadena
        headers=self.header(cursor,nombres,esquema,tabla)
        #extrayendo datos en una cadena
        datos=""
        i=0
        for col in nuevaf:
            if "id" not in col:
                datos=datos+nombres[i]+'= "'+col+'", '
            i=i+1
        if datos.endswith(", "):
            datos = datos[:-2]

        cursor.execute(f"UPDATE {esquema}.{tabla} SET {datos} WHERE id_{tabla} = {id}")
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
        bdtype= cursor.fetchall()

        for i in range (len(nuevaf)):
            if bdtype(i)=='date':
                nuevaf[i] = datetime.strptime(nuevaf[i], "%Y-%m-%d").date()  # Convierte a datetime.date
            elif bdtype(i)=='bigint':
                nuevaf[i]=int(nuevaf[i])
            elif bdtype(i)=='numeric':
                nuevaf[i]=Decimal(nuevaf[i])

        #nocierracursor
        #v vector a insertar
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

        return cadenanombres
    
        #nocierra cursor
        #modifica vector nombres
        #retorna en un string el vector nombres
