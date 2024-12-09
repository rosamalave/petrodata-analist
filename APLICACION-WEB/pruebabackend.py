from prettytable import PrettyTable
from bd.conexion_bd import base_ddatos
from datetime import datetime
from decimal import Decimal
import os

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

class ConsolaDBBackend:
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

        cursor.execute(f"SELECT {cadenanombres} FROM {self.esquema}.{self.tabla} ORDER BY id_{self.tabla} ASC LIMIT 10")
        self.datos = cursor.fetchall()
        cursor.execute(f"SELECT * FROM {self.esquema}.{self.tabla} ORDER BY id_{self.tabla} ASC LIMIT 10")
        self.datosall = cursor.fetchall()
        cursor.close()

    def agregar_fila(self):
        nueva_fila = [None] * len(self.headers)
        self.datos.append(nueva_fila)

    def eliminar_fila(self, indice_superficial):
        if indice_superficial < 0 or indice_superficial >= len(self.datosall):
            raise IndexError("Índice fuera de rango.")
        id_real = self.datosall[indice_superficial][0]
        self.conexion.eliminar(id_real, self.esquema, self.tabla)
        self.cargar_datos()

    def validar(self, valor, columna, permite_nulo=False):
        cursor = self.conexion.conn.cursor()
        query = f"""
        SELECT data_type
        FROM information_schema.columns
        WHERE table_schema = %s
        AND table_name = %s
        AND column_name = %s
        """
        cursor.execute(query, (self.esquema, self.tabla, columna))
        tipo_dato = cursor.fetchone()
        cursor.close()

        if not tipo_dato:
            raise ValueError(f"No se pudo obtener el tipo de dato para la columna '{columna}'.")
        tipo_esperado = tipo_dato[0]

        if valor is None or str(valor).strip() == "":
            if permite_nulo:
                return True
            else:
                raise ValueError("El valor no puede ser nulo o vacío.")
        # Validación según tipo de dato
        # (continuar con las validaciones específicas como en el código original)

    def aplicar_filtro_por_fecha(self, datos, fecha_inicio, fecha_fin, indice_fecha):
        return [fila for fila in datos if fecha_inicio <= fila[indice_fecha] <= fecha_fin]

    def aplicar_filtro_por_valores(self, datos, valor_min, valor_max, indice_campo):
        return [fila for fila in datos if valor_min <= fila[indice_campo] <= valor_max]


class ConsolaDBFrontend:
    def __init__(self, backend):
        self.backend = backend

    def menu_principal(self):
        while True:
            self.vistageneral(self.backend.datos)
            print("\nMenú Principal:")
            print("1) Agregar fila")
            print("2) Eliminar fila")
            print("3) Filtro por fecha")
            print("4) Filtro por valores")
            print("5) Salir")
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.backend.agregar_fila()
                print("\nFila vacía agregada.")
            elif opcion == "2":
                self.eliminar_fila()
            elif opcion == "3":
                self.filtro_por_fecha()
            elif opcion == "4":
                self.filtro_por_valores()
            elif opcion == "5":
                print("Saliendo del programa.")
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    def filtro_por_fecha(self):
        if 'produccion_c' in self.backend.tabla:
            # Filtro para datos diarios (real crudo)
            fecha_inicio = input("Fecha inicio (AAAA-MM-DD): ")
            fecha_fin = input("Fecha fin (AAAA-MM-DD): ")
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

        elif 'produccion_g' in self.tabla or 'potencial' in self.tabla or 'diferida' in self.tabla:
            # Filtro para datos promedios mensuales
            fecha_inicio = input("Fecha inicio (AAAA-MM): ")
            fecha_fin = input("Fecha fin (AAAA-MM): ")
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m").date()
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m").date()
            
        datos_filtrados = self.backend.aplicar_filtro_por_fecha(self.backend.datos, fecha_inicio, fecha_fin, indice_fecha=0)
        self.vistageneral(datos_filtrados)

    def filtro_por_valores(self):
        print("Seleccione un campo numérico para filtrar:")
        campos_numericos = [header for header in self.backend.headers if header not in ['fecha', 'id']]  # Filtramos las fechas y la columna ID
        for i, campo in enumerate(campos_numericos):
            print(f"{i+1}) {campo}")
        opcion = int(input("Seleccione una opción: "))
        valor_min = Decimal(input("Valor mínimo: "))
        valor_max = Decimal(input("Valor máximo: "))
        datos_filtrados = self.backend.aplicar_filtro_por_valores(self.backend.datos, valor_min, valor_max, indice_campo=opcion)
        self.vistageneral(datos_filtrados)

    def eliminar_fila(self):
        print("Seleccione una fila para eliminar:")
        for i, fila in enumerate(self.backend.datosall):
            print(f"{i}) {fila}")
        indice = int(input("Índice: "))
        try:
            self.backend.eliminar_fila(indice)
            print("Fila eliminada.")
        except (IndexError, ValueError) as e:
            print(f"Error: {e}")

    def vistageneral(self, data):
        tabla = PrettyTable()
        tabla.field_names = self.backend.headers
        for fila in data:
            tabla.add_row(fila)
        print(tabla)


# Ejemplo de uso
if __name__ == "__main__":
    conexion = base_ddatos()
    backend = ConsolaDBBackend(conexion, "public", "produccion_c")
    frontend = ConsolaDBFrontend(backend)
    frontend.menu_principal()
