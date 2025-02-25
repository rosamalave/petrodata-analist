import pg8000
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from datetime import datetime
from decimal import Decimal
import sys
# Conexión a PostgreSQL

class base_ddatos():

    def __init__(self):
        self.conn = None

    def verificar_iniciar_sesion(self, usuario, contrasena):
        try:
            conn_temp = pg8000.connect(
                host="localhost",
                database="juninpruebas",
                user="postgres",
                password="Junindata"
            )
            cursor = conn_temp.cursor()

            consulta = "SELECT * FROM public2.usuario WHERE usuario = %s AND passwordd = %s"
            cursor.execute(consulta, (usuario, contrasena))
            existe = cursor.fetchone() is not None
            cursor.close()
            conn_temp.close()

            if not existe:
                print("Usuario o contraseña incorrectos en la tabla de la aplicación.")
                return False

            try:
                self.conn = pg8000.connect(
                    host="localhost",
                    database="juninpruebas",
                    user=usuario,
                    password=contrasena
                )
                print("Sesión iniciada correctamente.")
                cursor = self.conn.cursor()
                cursor.execute("SELECT public2.registrar_inicio_sesion();")
                self.conn.commit()
                cursor.close()
                return True
            except Exception as e:
                print("Error al conectar a PostgreSQL: {}".format(e))
                return False
            
        except Exception as e:
            print("Error durante el inicio de sesión: {}".format(e))
            return False

    def cerrar_sesion(self, usuario):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT public2.registrar_cierre_sesion();")
                self.conn.commit()
                cursor.close()
                print("Sesión de {} cerrada exitosamente.".format(usuario))
            except Exception as e:
                print("Error al registrar el cierre de sesión: {}".format(e))
            finally:
                self.conn.close()
                self.conn = None
                print("Conexión cerrada.")
                
    def insertar(self, producto, nuevaf, esquema, tabla):
        cursor = self.conn.cursor()
        print("Fila editada en insertar: {}".format(nuevaf))
        self.conversionformatotabla(cursor, nuevaf, esquema, tabla)
        print("Fila en insertar convertida: {}".format(nuevaf))
        
        nombres = []
        headers = self.header(cursor, nombres, esquema, tabla)
        print("Cadena headers: {}".format(headers))

        campos = ", ".join(["%s" for _ in nombres]) 
               
        consulta = "INSERT INTO {}.{}({}) VALUES({})".format(esquema, tabla, headers, campos)
        print("Consulta de insertar: {}".format(consulta))
        cursor.execute(consulta, nuevaf)
        self.conn.commit()
        cursor.close()

    def editar(self, id, producto, nuevaf, esquema, tabla):
        cursor = self.conn.cursor()
        print("fila en editar sin convertir {}".format(nuevaf))
        self.conversionformatotabla(cursor, nuevaf, esquema, tabla)
        print("fila convertida {}".format(nuevaf))

        nombres = []
        self.header(cursor, nombres, esquema, tabla)

        campos = ", ".join(["{} = %s".format(col) for col in nombres])

        if self.buscar(cursor, id, esquema, tabla):
            consulta = "UPDATE {}.{} SET {} WHERE id_{} = %s".format(esquema, tabla, campos, tabla)
            print("Ejecutando consulta: {}".format(consulta))
            cursor.execute(consulta, nuevaf + [id])

        self.conn.commit()
        cursor.close()

    def eliminar(self, id, esquema, tabla):
        cursor = self.conn.cursor()
        id = self.buscar(cursor, id, esquema, tabla)
        if id != -1:
            cursor.execute("DELETE FROM {}.{} WHERE id_{} = {}".format(esquema, tabla, tabla, id))
        self.conn.commit()
        cursor.close()

    def buscar(self, cursor, id, esquema, tabla):
        cursor.execute("SELECT * FROM {}.{} WHERE id_{} = {}".format(esquema, tabla, tabla, id))
        if cursor.rowcount == 0 or cursor.rowcount == -1:
            print("fila no existe.")
            return -1
        else:
            return id
        
    def conversionformatotabla(self, cursor, nuevaf, esquema, tabla):
        cursor.execute("SELECT data_type FROM information_schema.columns WHERE table_schema = '{}' AND table_name = '{}' AND column_name NOT LIKE 'id%'".format(esquema, tabla))
        bdtype = cursor.fetchall()
        print("Fila seleccionada: {}".format(nuevaf))
        print("bdtype: {}".format(bdtype))
    
        j = 0
        for i in range(len(nuevaf)):
            tipo_dato = bdtype[j][0]
            print("Tipo de dato de columna {} en {}: {}".format(i, j, tipo_dato))
            if i == j:
                if tipo_dato == 'date':  
                    if isinstance(nuevaf[i], str):  
                        nuevaf[i] = datetime.strptime(nuevaf[i], "%Y-%m-%d").date()
                elif tipo_dato == 'bigint':
                    nuevaf[i] = int(nuevaf[i]) if not isinstance(nuevaf[i], int) else nuevaf[i]
                elif tipo_dato == 'numeric':
                    nuevaf[i] = Decimal(nuevaf[i]) if not isinstance(nuevaf[i], Decimal) else nuevaf[i]
            j += 1

    def header(self, cursor, nombres, esquema, tabla):
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = '{}' AND table_name = '{}' AND column_name NOT LIKE 'id%'".format(esquema, tabla))

        for col in cursor.fetchall():
            nombres.append(str(col[0]))

        cadenanombres = ", ".join(["{}".format(col) for col in nombres])

        return cadenanombres
