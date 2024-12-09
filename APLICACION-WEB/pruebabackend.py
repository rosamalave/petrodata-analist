from prettytable import PrettyTable
from bd.conexion_bd import base_ddatos
from datetime import datetime
from decimal import Decimal
import os

def limpiar_consola():
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

        cursor.execute(f"SELECT {cadenanombres} FROM {self.esquema}.{self.tabla} ORDER BY id_{self.tabla} ASC LIMIT 10")
        self.datos = cursor.fetchall()
        cursor.execute(f"SELECT * FROM {self.esquema}.{self.tabla} ORDER BY id_{self.tabla} ASC LIMIT 10")
        self.datosall = cursor.fetchall()
        cursor.close()

    def menu_principal(self):
        while True:
            self.vistageneral(self.datos)
            print("\nMenú Principal:")
            print("1) Agregar fila")
            print("2) Editar fila")
            print("3) Eliminar fila")
            print("4) Opción de Separadores")
            print("5) Filtrar datos")
            print("6) Salir")
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.agregar_fila()
                print("\nFila vacía agregada. Ahora puede editarla seleccionando la opción 2.")
            elif opcion == "2":
                self.editar_fila()
            elif opcion == "3":
                self.eliminarfila()
                print("\nFila eliminada con éxito.")
            elif opcion == "4":
                self.opciones_separacion()
            elif opcion == "5":
                self.menu_filtros()
            elif opcion == "6":
                print("Saliendo del programa.")
                break      
            else:
                print("Opción inválida. Intente de nuevo.")
                
    def menu_filtros(self):
        while True:
            print("\nMenú de Filtros:")
            print("1) Filtro por rango de fechas")
            print("2) Filtro por valores numéricos")
            print("3) Volver al menú principal")
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.filtro_por_fecha()
            elif opcion == "2":
                self.filtro_por_valores()
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    def filtro_por_fecha(self):
        if 'produccion_c' in self.tabla:
            # Filtro para datos diarios (real crudo)
            fecha_inicio = input("Ingrese la fecha de inicio (día-mes-año): ")
            fecha_fin = input("Ingrese la fecha de fin (día-mes-año): ")
            fecha_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y").date()
            fecha_fin = datetime.strptime(fecha_fin, "%d-%m-%Y").date()
            
            # Filtrar los datos por las fechas ingresadas
            datos_filtrados = [fila for fila in self.datos if fecha_inicio <= fila[0] <= fecha_fin]
            self.vistageneral(datos_filtrados)

        elif 'produccion_g' in self.tabla or 'potencial' in self.tabla or 'diferida' in self.tabla:
            # Filtro para datos promedios mensuales
            fecha_inicio = input("Ingrese el mes de inicio (mes-año): ")
            fecha_fin = input("Ingrese el mes de fin (mes-año): ")
            fecha_inicio = datetime.strptime(fecha_inicio, "%m-%Y").date()
            fecha_fin = datetime.strptime(fecha_fin, "%m-%Y").date()
            
            # Filtrar los datos por las fechas ingresadas
            datos_filtrados = [fila for fila in self.datos if fecha_inicio <= fila[1] <= fecha_fin]
            self.vistageneral(datos_filtrados)

        # Validar que el rango de fechas sea válido
        if fecha_inicio > fecha_fin:
            print("El rango de fechas es inválido. La fecha de inicio no puede ser posterior a la fecha de fin.")
        else:
            print(f"Filtrando datos entre {fecha_inicio.strftime('%d-%m-%Y')} y {fecha_fin.strftime('%d-%m-%Y')}...")
            self.vistageneral(datos_filtrados)

    def filtro_por_valores(self):
        print("\nSeleccione el campo numérico para aplicar el filtro:")
        campos_numericos = [header for header in self.headers if header not in ['fecha', 'id']]  # Filtramos las fechas y la columna ID
        for i, campo in enumerate(campos_numericos):
            print(f"{i+1}) {campo}")
        
        opcion = input("\nSeleccione una opción: ")
        try:
            campo_seleccionado = campos_numericos[int(opcion) - 1]
            valor_min = input(f"Ingrese el valor mínimo para {campo_seleccionado}: ")
            valor_max = input(f"Ingrese el valor máximo para {campo_seleccionado}: ")
            valor_min = Decimal(valor_min)
            valor_max = Decimal(valor_max)

            # Validar que el rango sea válido
            if valor_min > valor_max:
                print(f"El rango para {campo_seleccionado} es inválido. El valor mínimo no puede ser mayor que el máximo.")
            else:
                # Filtrar los datos por los valores numéricos
                datos_filtrados = [fila for fila in self.datos if valor_min <= fila[self.headers.index(campo_seleccionado)] <= valor_max]
                print(f"Filtrando datos para {campo_seleccionado} entre {valor_min} y {valor_max}...")
                self.vistageneral(datos_filtrados)
        except (IndexError, ValueError):
            print("Opción inválida. Intente de nuevo.")

    def agregar_fila(self):
        nueva_fila = [None] * len(self.headers)
        self.datos.append(nueva_fila)
        print("\nFila vacía agregada. Ahora puede editarla.")

    def editar_fila(self):
        # Implementar la lógica para editar fila aquí
        pass

    def eliminarfila(self):
        try:
            indice = input("\nIngrese el índice de la fila que desea eliminar: ").strip()
            if not indice.isdigit():
                raise ValueError("El índice debe ser un número entero.")
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
        indice = int(indice)
        indice = self.datosall[indice][0]
        self.conexion.eliminar(indice, self.esquema, self.tabla)
        self.cargar_datos()

    def opciones_separacion(self):
        while True:
            print("\nOpciones de Separación:")
            print("1) Anual")
            print("2) Mensual")
            print("3) Volver")
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.aplicar_separador("anual")
                break
            elif opcion == "2":
                self.aplicar_separador("mensual")
                break
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Intente de nuevo.")
                
    def aplicar_separador(self, tipo_periodo):
        tabla = PrettyTable()
        tabla.field_names = ["Índice"] + self.headers
        
        filas_con_indices = [[i] + list(fila) for i, fila in enumerate(self.datos)]
        
        ultimo_periodo = None
        for fila in filas_con_indices:
            fecha = fila[1]
            if tipo_periodo == "anual":
                periodo = fecha.year
            elif tipo_periodo == "mensual":
                periodo = (fecha.year, fecha.month)

            if ultimo_periodo != periodo:
                if tipo_periodo == "anual":
                    tabla.add_row(["----- " + str(periodo) + " -----"] + [""] * (len(self.headers)))
                elif tipo_periodo == "mensual":
                    nombre_mes = fecha.strftime("%B")
                    tabla.add_row([f"----- {nombre_mes} -----"] + [""] * (len(self.headers)))

                ultimo_periodo = periodo

            tabla.add_row(fila)

        print(tabla)

    def validar(self, valor, esquema, tabla, columna, permite_nulo=False):
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

        if valor is None or str(valor).strip() == "":
            if permite_nulo:
                return True
            else:
                raise ValueError("El valor no puede ser nulo o vacío.")
        
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
                raise ValueError(f"El valor '{valor}' no es una fecha válida.")
            return True
        else:
            raise ValueError(f"Tipo de dato no soportado '{tipo_esperado}'.")

    def vistageneral(self, data):
        tabla = PrettyTable()
        tabla.field_names = self.headers
        for fila in data:
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