import pg8000
from datetime import datetime
from decimal import Decimal
import sys

# Conexión a PostgreSQL

class base_ddatos():

    def __init__(self):
        # Conexión inicial vacía, se establecerá al iniciar sesión
        self.conn = None

    def verificar_iniciar_sesion(self, usuario, contrasena):
        # Conexión inicial para verificar credenciales en la tabla usuario
        try:
            # Conexión temporal con usuario maestro para verificar credenciales
            conn_temp = pg8000.connect(                
                user="postgres",
                host="localhost",
                port=5433,
                database="juninpruebas",
                password="JUNINDATA",
                ssl=False,
            )
            cursor = conn_temp.cursor()

            # Verificar credenciales en la tabla de la aplicación
            consulta = "SELECT * FROM public2.usuario WHERE usuario = %s AND passwordd = %s"
            cursor.execute(consulta, (usuario, contrasena))
            existe = cursor.fetchone() is not None
            cursor.close()
            conn_temp.close()

            if not existe:
                print("Usuario o contraseña incorrectos en la tabla de la aplicación.")
                return False

            # Si las credenciales son válidas, intentar conexión con PostgreSQL usando esas credenciales
            try:
                self.conn = pg8000.connect(
                    user=usuario,
                    host="localhost",
                    port=5433,
                    database="juninpruebas",
                    password=contrasena,
                    ssl=False,
                )
                print("Sesión iniciada correctamente.")
                cursor = self.conn.cursor()
                cursor.execute("SELECT public.registrar_inicio_sesion();")
                self.conn.commit()
                cursor.close()
                return True
            except self.conn.OperationalError as e:
                print("Error al conectar a PostgreSQL: {}".format(e))
                return False
            
        except self.conn.OperationalError as e:
            print("Error durante el inicio de sesión: {}".format(e))
            return False

    def cerrar_sesion(self, usuario):
        """
        Cierra la conexión y registra el cierre de sesión.
        """
        if self.conn:
            try:
                cursor = self.conn.cursor()
                # Registrar el cierre de sesión si existe un método o función para ello
                cursor.execute("SELECT public.registrar_cierre_sesion();")
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
        
        #extrayendo headers en una cadena
        nombres = []
        headers = self.header(cursor, nombres, esquema, tabla)
        print("Cadena headers: {}".format(headers))

        campos = ", ".join(["%s" for col in nombres]) 
               
        consulta = "INSERT INTO {}.{}({}) VALUES({})".format(esquema, tabla, headers, campos)
        print("Consulta de insertar: {}".format(consulta))
        cursor.execute(consulta, nuevaf)
        self.conn.commit()
        cursor.close()

    def editar(self, id, producto, nuevaf, esquema, tabla):
        #Edita una fila en la base de datos actualizando todos los campos de la tabla, incluso los no editados.
        cursor = self.conn.cursor()
        print("fila en editar sin convertir {}".format(nuevaf))
        # Asegurarse de que los datos estén en el formato adecuado para la tabla
        self.conversionformatotabla(cursor, nuevaf, esquema, tabla)
        print("fila convertida {}".format(nuevaf))
        # Extraer los nombres de las columnas (header)
        nombres = []
        self.header(cursor, nombres, esquema, tabla)  # nombres contendrá los encabezados de la tabla

        # Generar la cadena dinámica para el SET usando comprensión de listas y join
        campos = ", ".join(["{} = %s".format(col) for col in nombres])

        # Verificar si el registro con id existe en la tabla
        if self.buscar(cursor, id, esquema, tabla):
            # Construir y ejecutar la consulta dinámica
            consulta = "UPDATE {}.{} SET {} WHERE id_{} = %s".format(esquema, tabla, campos, tabla)
            print("Ejecutando consulta: {}".format(consulta))
            # Ejecutar la consulta con parámetros seguros
            cursor.execute(consulta, nuevaf + [id])

        # Guardar los cambios en la base de datos
        self.conn.commit()
        cursor.close()

    def eliminar(self, id, esquema, tabla):
        cursor = self.conn.cursor()
        id = self.buscar(cursor, id, esquema, tabla)
        if id != -1:
            try:
                query="SET session_replication_role = 'replica';" 
                cursor.execute(query) 
                query="DELETE FROM {}.{} WHERE id_{} = {}".format(esquema, tabla, tabla, id)
                cursor.execute(query)
                query="SET session_replication_role = 'replica';"
                cursor.execute(query)
                self.conn.commit()
            except Exception as e:
                print("Error al eliminar de la bd: {}".format(e))
            
        else: 
            print("No se pudo encontrar la fila a eliminar")
        cursor.close()

    def buscar(self, cursor, id, esquema, tabla):

        query="SELECT * FROM {}.{} WHERE id_{} = {}".format(esquema, tabla, tabla, id)

        cursor.execute(query)
        filaid=cursor.fetchall()
        print("{}=={}".format(filaid[0][0],id))

        #if cursor.rowcount == 0 or cursor.rowcount == -1:
        if filaid[0][0]!=id:
            print("fila no existe.")
            return -1
        else:
            print("id encontrado en buscar: {}".format(id))
            return id
        
    def conversionformatotabla(self, cursor, nuevaf, esquema, tabla):
        cursor.execute("SELECT data_type FROM information_schema.columns WHERE table_schema = '{}' AND table_name = '{}' AND column_name NOT LIKE 'id%%'".format(esquema, tabla))
        bdtype = cursor.fetchall()
        print("Fila seleccionada: {}".format(nuevaf))
        print("bdtype: {}".format(bdtype))
    
        j = 0
        for i in range(len(nuevaf)):
            tipo_dato = bdtype[j][0]  # Extrae el tipo de dato desde la tupla
            print("Tipo de dato de columna {} en {}: {}".format(i, j, tipo_dato))
            if i == j:
                if tipo_dato == 'date':  # Si el tipo es 'date'
                    if isinstance(nuevaf[i], str):  # Convierte solo si es cadena
                        nuevaf[i] = datetime.strptime(nuevaf[i], "%Y-%m-%d").date()
                elif tipo_dato == 'bigint':  # Si el tipo es 'bigint'
                    nuevaf[i] = int(nuevaf[i]) if not isinstance(nuevaf[i], int) else nuevaf[i]
                elif tipo_dato == 'numeric':  # Si el tipo es 'numeric'
                    nuevaf[i] = Decimal(nuevaf[i]) if not isinstance(nuevaf[i], Decimal) else nuevaf[i]
            j += 1

    def header(self, cursor, nombres, esquema, tabla):
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = '{}' AND table_name = '{}' AND column_name NOT LIKE 'id%%'".format(esquema, tabla))

        #extrayendo headers en un vector
        for col in cursor.fetchall():
            nombres.append(str(col[0]))

        #extrayendo headers en una cadena
        cadenanombres = ", ".join([col for col in nombres])

        return cadenanombres