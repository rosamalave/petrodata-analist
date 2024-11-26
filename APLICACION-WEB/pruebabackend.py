from prettytable import PrettyTable
from bd.conexion_bd import base_ddatos
from datetime import datetime
from decimal import Decimal
import os

def limpiar_consola():
    """
    Limpia la consola de manera universal (funciona en Windows y Unix).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


class ConsolaDB:
    def __init__(self, conexion_bd, esquema, tabla):
        self.conexion = conexion_bd
        self.esquema = esquema
        self.tabla = tabla
        self.datos = [] #sin id
        self.datosall = [] #con id
        self.headers = []
        self.cargar_datos()
        
    def cargar_datos(self):
        cursor = self.conexion.conn.cursor()
        self.headers = []  # Inicializamos el vector de nombres
        cadenanombres = self.conexion.header(cursor, self.headers, self.esquema, self.tabla)
        
        print(f"SELECT {cadenanombres} FROM {self.esquema}.{self.tabla} ORDER BY id_{self.tabla} ASC LIMIT 10")
        cursor.execute(f"SELECT {cadenanombres} FROM {self.esquema}.{self.tabla} ORDER BY id_{self.tabla} ASC LIMIT 10")
        self.datos = cursor.fetchall()
        cursor.execute(f"SELECT * FROM {self.esquema}.{self.tabla} ORDER BY id_{self.tabla} ASC LIMIT 10")
        self.datosall = cursor.fetchall()
        cursor.close()
        
    def menu_principal(self):
        while True:
            self.mostrar_tabla()
            opcion = input("\n1) Editar fila\n2) Agregar fila\n3) Salir\nSeleccione una opción: ")
            if opcion == "1":
                self.activar_editar()
            elif opcion == "2":
                self.agregar_fila()
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    def mostrar_tabla(self):
        tabla = PrettyTable()
        tabla.field_names = ["Índice"] + self.headers  # Agregamos el encabezado del índice
    
        # Preparamos todas las filas con su índice
        filas_con_indices = [[i] + list(fila) for i, fila in enumerate(self.datos)]
    
        # Agregamos todas las filas a la tabla
        for fila in filas_con_indices:
            tabla.add_row(fila)
    
        print(tabla)

    def activar_editar(self):
        self.mostrar_tabla()
        try:
            indice = int(input("\nIngrese el índice de la fila que desea editar: ")) 
            if indice < 0 or indice >= len(self.datos):
                raise ValueError("Índice fuera de rango.")
        except ValueError as e:
            print(e)
            return

        fila_original = list(self.datos[indice])
        print(f"fila original: {fila_original}")

        self.mostrar_fila_editando(self.headers, fila_original, indice)

        while True:
            celda = input("\n¿Qué celda desea editar? (introduzca índice o 'x' para salir): ")
            if celda.lower() == "x":
                print("\nEdición finalizada.")
                break
            try:
                columna = int(celda)
                if columna < 0 or columna >= len(self.headers):
                    raise ValueError("Columna fuera de rango.")
                
                nuevo_valor = input(f"Ingrese el nuevo valor para '{self.headers[columna]}': ")
                
                # Validar el valor directamente (incluye obtener tipo de dato y validación)
                self.validar(nuevo_valor, self.esquema, self.tabla, self.headers[columna])

                fila_original[columna] = nuevo_valor
                self.mostrar_fila_editando(self.headers, fila_original, indice)
            except ValueError as e:
                print(f"Error: {e}")
                continue
        print(f"fila editada: {fila_original}")
        # Usamos `conversionformatotabla` antes de guardar cambios
        cursor = self.conexion.conn.cursor()
        self.conexion.conversionformatotabla(cursor, fila_original, self.esquema, self.tabla)
        print(f"fila editada y convertida: {fila_original}")
        cursor.close()
        self.guardar_cambios(indice, fila_original)

    def mostrar_fila_editando(self, headers, fila_original, indice_fila):
        subindices = [str(i) for i in range(len(headers))]
        tabla = PrettyTable()
        tabla.add_row(subindices)
        tabla.add_row(headers)
        tabla.add_row(fila_original)

        print("\n--- Editando Fila ---")
        print(f"Índice de la fila: {indice_fila}")
        print(tabla)

    def guardar_cambios(self, indice, fila_editada):
        id_fila=self.datosall[indice][0] #consultando el id en la tabla con columnas id 
        self.conexion.editar(id_fila, None, fila_editada, self.esquema, self.tabla)
        print("\nCambios guardados exitosamente.")
        self.cargar_datos()

    def agregar_fila(self):
        nueva_fila = [None] * len(self.headers)
        self.datos.append(nueva_fila)
        print("\nFila vacía agregada. Ahora puede editarla.")
        self.activar_editar()
        self.datos.pop()  # Retira fila vacía si no se guarda

    def insertar_fila(self, nueva_fila):
        # Validar cada valor de la nueva fila antes de insertarlo
        for i, valor in enumerate(nueva_fila):
            self.validar(valor, self.esquema, self.tabla, self.headers[i])
        
        cursor = self.conexion.conn.cursor()
        self.conexion.conversionformatotabla(cursor, nueva_fila, self.esquema, self.tabla)
        cursor.close()
        self.conexion.insertar(None, nueva_fila, self.esquema, self.tabla)
        print("\nNueva fila insertada exitosamente.")
        self.cargar_datos()

    def validar(self, valor, esquema, tabla, columna, permite_nulo=False):
        """
        - Números no negativos
        - Fechas no mayores a hoy
        :param valor: El dato a validar.
        :param permite_nulo: Indica si se permite que el valor sea nulo.
        :return: True si el dato es válido.
        :raises ValueError: Si el dato no cumple con las reglas lógicas.
        """
        # Consultar tipo de dato directamente desde la base de datos
        cursor = self.conexion.conn.cursor()
        query = f"""
        SELECT data_type
        FROM information_schema.columns
        WHERE table_schema = %s
        AND table_name = %s
        AND column_name = %s
        """
        cursor.execute(query, (esquema, tabla, columna))
        tipo_dato = cursor.fetchone()
        cursor.close()

        if not tipo_dato:
            raise ValueError(f"No se pudo obtener el tipo de dato para la columna '{columna}'.")

        tipo_esperado = tipo_dato[0]

        # Validar si el valor es nulo
        if valor is None or str(valor).strip() == "":
            if permite_nulo:
                return True
            else:
                raise ValueError("El valor no puede ser nulo o vacío.")
        
        # Validar tipo de dato esperado
        if tipo_esperado in ('int', 'bigint', 'numeric'):
            try:
                # Convertir a float para validar que es un número
                numero = float(valor)
                if numero < 0:
                    raise ValueError(f"El valor '{valor}' no puede ser negativo.")
            except ValueError:
                raise ValueError(f"El valor '{valor}' no es un número válido.")
            return True

        elif tipo_esperado == 'date':
            try:
                # Validar fecha en formato 'dd/mm/yyyy'
                fecha = datetime.strptime(valor, "%d/%m/%Y")
                if fecha > datetime.today():
                    raise ValueError(f"El valor '{valor}' no puede ser una fecha futura.")
            except ValueError:
                raise ValueError(f"El valor '{valor}' no tiene un formato de fecha válido (dd/mm/yyyy).")
            return True

        else:
            raise ValueError(f"El tipo de dato '{tipo_esperado}' no está soportado.")

# Ejemplo de uso
if __name__ == "__main__":
    conexion = base_ddatos()  # Asume que 'base_ddatos()' está definida para la conexión.
    app = ConsolaDB(conexion, "public", "produccion_c")
    app.menu_principal()
