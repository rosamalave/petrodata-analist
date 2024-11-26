from prettytable import PrettyTable
from bd.conexion_bd import base_ddatos
from datetime import datetime
from decimal import Decimal
import os

#funciona todo pero trabaja con los indices de la lista generada desde la base de datos en si
#cambiar enfoque para que trabaje directamente con los id de la base de datos ya que no siempre los id
#van a representar continuidad para representar los indices del 0 al 1 
#averiguar: es posible que la base de datos te de el indice superficial numeral de continuidad?
#averiguar: es posible programar un script que cada vez que se elimine una fila se reinicie
#el conteo para mantener continuidad

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
        self.datos = []  # Sin ID
        self.datosall = []  # Con ID
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
            self.vistageneral()
            opcion = input("\n1) Agregar fila\n2) Editar fila\n3) Eliminar fila\n4) Salir\nSeleccione una opción: ")

            if opcion == "1":
                # Agregar una nueva fila
                self.agregar_fila()
                print("\nFila vacía agregada. Ahora puede editarla seleccionando la opción 2.")

            elif opcion == "2":
                try:
                    # Solicitar el índice de la fila a editar
                    indice = input("\nIngrese el índice de la fila que desea editar: ").strip()
                    if not indice.isdigit():
                        raise ValueError("El índice debe ser un número entero.")
                    indice = int(indice)

                    # Determinar si se trata de inserción o edición
                    fila = list(self.datos[indice])
                    if all(celda is None for celda in fila):
                        operacion = self.insertarfila
                    else:
                        operacion = self.editarfila

                    # Gestionar la fila según la operación
                    self.agregardatos(operacion, indice)

                except (ValueError, IndexError) as e:
                    print(f"Error: {e}")
            elif opcion=="3":
                # eliminar una fila
                self.eliminarfila()
                print("\nFila eliminada con exito.")
            elif opcion == "4":
                print("Saliendo del programa.")
                break
            
            else:
                print("Opción inválida. Intente de nuevo.")

    def agregardatos(self, operacion, indice):
        """
        Gestionar la edición o inserción de una fila.    
        :param operacion: Función a ejecutar (self.insertarfila o self.editarfila).
        :param indice: Índice de la fila a editar o insertar.
        """
        fila = list(self.datos[indice])

        self.vistaedicion(self.headers, fila, indice)

        while True:
            celda = input("\n¿Qué celda desea editar? (introduzca índice o 'x' para finalizar): ")
            if celda.lower() == "x":
                print("\nOperación finalizada.")
                break
            try:
                columna = int(celda)
                if columna < 0 or columna >= len(self.headers):
                    raise ValueError("Columna fuera de rango.")

                nuevo_valor = input(f"Ingrese el nuevo valor para '{self.headers[columna]}': ")

                # Validar el valor antes de asignarlo
                self.validar(nuevo_valor, self.esquema, self.tabla, self.headers[columna])
                fila[columna] = nuevo_valor
                self.vistaedicion(self.headers, fila, indice)
            except ValueError as e:
                print(f"Error: {e}")
                continue

        # Llamar a la operación final (insertar o editar)
        operacion(indice, fila)
        self.cargar_datos()


    def editarfila(self, indice, fila_editada):
        indice=self.datosall[indice][0]
        self.conexion.editar(indice, None, fila_editada, self.esquema, self.tabla)
        print("\nFila editada correctamente.")


    def insertarfila(self, _, nueva_fila):
        self.conexion.insertar(None, nueva_fila, self.esquema, self.tabla)
        print("\nNueva fila insertada correctamente.")
    
    def eliminarfila(self):
        try:
            # Solicitar el índice de la fila a editar
            indice = input("\nIngrese el índice de la fila que desea editar: ").strip()
            if not indice.isdigit():
                raise ValueError("El índice debe ser un número entero.")
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
        indice = int(indice)
        indice=self.datosall[indice][0]
        self.conexion.eliminar(indice, self.esquema, self.tabla)
        self.cargar_datos()
        
    def agregar_fila(self):
        nueva_fila = [None] * len(self.headers)
        self.datos.append(nueva_fila)
        print("\nFila vacía agregada. Ahora puede editarla.")


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
                numero = float(valor)
                if numero < 0:
                    raise ValueError(f"El valor '{valor}' no puede ser negativo.")
            except ValueError:
                raise ValueError(f"El valor '{valor}' no es un número válido.")
            return True

        elif tipo_esperado == 'date':
            try:
                fecha = datetime.strptime(valor, "%Y-%m-%d")
                if fecha > datetime.today():
                    raise ValueError(f"El valor '{valor}' no puede ser una fecha futura.")
            except ValueError:
                raise ValueError(f"El valor '{valor}' no tiene un formato de fecha válido (yyyy-mm-d).")
            return True

        else:
            raise ValueError(f"El tipo de dato '{tipo_esperado}' no está soportado.")

    def vistageneral(self):
    
        tabla = PrettyTable()
        tabla.field_names = ["Índice"] + self.headers  # Agregamos el encabezado del índice
    
        # Preparamos todas las filas con su índice
        filas_con_indices = [[i] + list(fila) for i, fila in enumerate(self.datos)]
    
        # Agregamos todas las filas a la tabla
        for fila in filas_con_indices:
            tabla.add_row(fila)
    
        print(tabla)


    def vistaedicion(self, headers, fila_original, indice_fila):
        subindices = [str(i) for i in range(len(headers))]
        tabla = PrettyTable()
        tabla.add_row(subindices)
        tabla.add_row(headers)
        tabla.add_row(fila_original)

        print("\n--- Editando Fila ---")
        print(f"Índice de la fila: {indice_fila}")
        print(tabla)

    
# Ejemplo de uso
if __name__ == "__main__":
    conexion = base_ddatos()  # Asume que 'base_ddatos()' está definida para la conexión.
    app = ConsolaDB(conexion, "public", "produccion_c")
    app.menu_principal()
