import psycopg2
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from datetime import datetime
from decimal import Decimal

# Conexión a PostgreSQL
class base_ddatos():


    def __init__(self):

        #objeto de tipo conexion que guarda metodos: cursor, commit, rollback, close
        self.conn = psycopg2.connect(host="localhost", database="PETROJUNIN_DATA", user="postgres", password="Junindata" )


    def conversionformatotabla(self, cursor, nuevaf, nesquema, ntabla):
        #v vector a insertar
        #bdtype tupla con tipos de datos 

        cursor.execute(f"SELECT data_type FROM information_schema.columns WHERE table_schema = '{nesquema}' AND table_name = '{ntabla}' AND column_name NOT LIKE 'id%'")
        bdtype= cursor.fetchall()

        for i in range (len(nuevaf)):
            if bdtype(i)=='date':
                nuevaf[i] = datetime.strptime(nuevaf[i], "%Y-%m-%d").date()  # Convierte a datetime.date
            elif bdtype(i)=='bigint':
                nuevaf[i]=int(nuevaf[i])
            elif bdtype(i)=='numeric':
                nuevaf[i]=Decimal(nuevaf[i])



    def insertar(self,producto,nuevaf,nesquema,ntabla):
        cursor=self.conn.cursor()
        self.conversionformatotabla(cursor, nuevaf,nesquema,ntabla)
        cursor.execute("INSERT INTO public.producto(id_producto)VALUES (%s)", producto)
        cursor.execute("INSERT INTO public.produccion_c(fecha, diluente, bpd) VALUES(%s, %s, %s)", (nuevaf[0], nuevaf[1], nuevaf[2]))
        self.conn.commit()

    

#produccionc 3 
#potencial 6
#producciong 2
#producciondiferida 3
#diferida np 28
#diferida p 8