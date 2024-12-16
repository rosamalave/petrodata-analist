from prettytable import PrettyTable
from bd.conexion_bd import base_ddatos
from datetime import datetime
from decimal import Decimal
import os


# Función para limpiar la consola
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
        self.nuevas_filas_indices = []  # Lista para almacenar índices de filas nuevas1
        self.cargar_datos()

    def cargar_datos(self):
        cursor = self.conexion.conn.cursor()
        self.headers = []
        cadenanombres = self.conexion.header(cursor, self.headers, self.esquema, self.tabla)
        cursor.execute(f"SELECT {cadenanombres} FROM {self.esquema}.{self.tabla} ORDER BY id_{self.tabla} ASC LIMIT 100")
        self.datos = cursor.fetchall()
        cursor.execute(f"SELECT * FROM {self.esquema}.{self.tabla} ORDER BY id_{self.tabla} ASC LIMIT 100")
        self.datosall = cursor.fetchall()
        cursor.close()


    def aplicar_separador(self, tipo_periodo, tabla, filas_con_indices):

        ultimo_periodo = None

        for fila in filas_con_indices:
            fecha = fila[1]
            if tipo_periodo == "anual":
                periodo = fecha.year
            elif tipo_periodo == "mensual":
                periodo = (fecha.year, fecha.month)

            if ultimo_periodo != periodo:
                if tipo_periodo == "anual":
                    tabla.add_row(["----- " + str(periodo) + " -----"] + [""] * len(self.headers))
                elif tipo_periodo == "mensual":
                    nombre_mes = fecha.strftime("%B")
                    tabla.add_row([f"----- {nombre_mes} -----"] + [""] * len(self.headers))
                ultimo_periodo = periodo

            tabla.add_row(fila)
        return tabla

    def agregar_datos(self, operacion, indice, cambios):
        fila_actualizada = list(self.datos[indice])
        for columna, nuevo_valor in cambios.items():
            self.validar(nuevo_valor, self.esquema, self.tabla, self.headers[columna])
            fila_actualizada[columna] = nuevo_valor
        operacion(indice, fila_actualizada)
        self.cargar_datos()

    def editar_fila(self, indice, fila_editada):
        id_fila = self.datosall[indice][0]
        self.conexion.editar(id_fila, None, fila_editada, self.esquema, self.tabla)

    def insertar_fila(self, _, nueva_fila):
        self.conexion.insertar(None, nueva_fila, self.esquema, self.tabla)

    def validar(self, valor, esquema, tabla, columna, permite_nulo=False):

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

    def agregar_fila(self):
        nueva_fila = [None] * len(self.headers)  # Crear una nueva fila vacía
        self.datos.append(nueva_fila)  # Agregar la nueva fila a los datos
        self.nuevas_filas_indices.append(len(self.datos) - 1)  # Guardar el índice de la nueva fila

    def eliminar_fila(self, indice_superficial):
        if indice_superficial < 0:
            raise IndexError("Índice fuera de rango.")
    
        # Verificar si la fila a eliminar es una fila nueva
        if indice_superficial in self.nuevas_filas_indices:  # Comprobar si el índice está en nuevas filas
            # Eliminar solo de self.datos y de nuevas_filas_indices
            self.datos.pop(indice_superficial)
            self.nuevas_filas_indices.remove(indice_superficial)
        else:
            # Si no es una fila nueva, eliminar de la base de datos
            id_real = self.datosall[indice_superficial][0]
            self.conexion.eliminar(id_real, self.esquema, self.tabla)
            # También eliminar de self.datos si está presente
            self.datos.pop(indice_superficial)
        self.cargar_datos()
    def filtrar_por_fecha_diaria(self, fecha_inicio, fecha_fin):
        fecha_inicio = datetime.strptime(fecha_inicio, "%d-%m-%Y").date()
        fecha_fin = datetime.strptime(fecha_fin, "%d-%m-%Y").date()

        if fecha_inicio > fecha_fin:
            raise ValueError("El rango de fechas es inválido.")
        
        return [fila for fila in self.datos if fecha_inicio <= fila[0] <= fecha_fin]

    def filtrar_por_fecha_mensual(self, fecha_inicio, fecha_fin):
        """Filtra los datos mensuales entre dos fechas."""
        fecha_inicio = datetime.strptime(fecha_inicio, "%m-%Y").date()
        fecha_fin = datetime.strptime(fecha_fin, "%m-%Y").date()

        if fecha_inicio > fecha_fin:
            raise ValueError("El rango de fechas es inválido.")

        return [fila for fila in self.datos if fecha_inicio <= fila[0] <= fecha_fin]

    def filtrar_por_valores(self, campo, valor_min, valor_max):
        valor_min = Decimal(valor_min)
        valor_max = Decimal(valor_max)

        if valor_min > valor_max:
            raise ValueError("El rango de valores es inválido.")

        indice_campo = self.headers.index(campo)
        return [fila for fila in self.datos if valor_min <= fila[indice_campo] <= valor_max]

class ConsolaDBFrontend:

    def __init__(self, backend):
        self.backend = backend

    def menu_principal(self):
        while True:
            limpiar_consola()
            self.vista_general(self.backend.datos)
            print("\nMenú Principal:")
            print("1) Agregar fila")
            print("2) Editar fila")
            print("3) Eliminar fila")
            print("4) Filtro por fecha")
            print("5) Filtro por valores")
            print("6) Opciones de Separación")
            print("7) Salir")
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                self.backend.agregar_fila()
                print("\nFila vacía agregada.")
            elif opcion == "2":
                self.gestionar_fila()
            elif opcion == "3":
                self.eliminar_fila()
            elif opcion == "4":
                self.filtro_por_fecha()
            elif opcion == "5":
                self.filtro_por_valores()
            elif opcion == "6":
                self.opciones_separacion()
            elif opcion == "7":
                print("Saliendo del programa.")
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    def gestionar_fila(self):
        try:
            indice = input("\nIngrese el índice de la fila que desea editar: ").strip()
            if not indice.isdigit():
                raise ValueError("El índice debe ser un número entero.")
            indice = int(indice)

            fila = list(self.backend.datos[indice])
            if all(celda is None for celda in fila):
                operacion = self.backend.insertar_fila
            else:
                operacion = self.backend.editar_fila

            cambios = {}
            while True:
                self.vista_edicion(self.backend.headers, fila, indice)
                celda = input("\n¿Qué celda desea editar? (introduzca índice o 'x' para finalizar): ")
                if celda.lower() == "x":
                    print("\nOperación finalizada.")
                    break
                try:
                    columna = int(celda)
                    if columna < 0 or columna >= len(self.backend.headers):
                        raise ValueError("Columna fuera de rango.")

                    nuevo_valor = input(f"Ingrese el nuevo valor para '{self.backend.headers[columna]}': ")
                    cambios[columna] = nuevo_valor
                    fila[columna] = nuevo_valor  # Actualizar dinámicamente la fila
                except ValueError as e:
                    print(f"Error: {e}")
                    continue

            if cambios:
                self.backend.agregar_datos(operacion, indice, cambios)

        except (ValueError, IndexError) as e:
            print(f"Error: {e}")

    def filtro_por_fecha(self):
        if 'produccion_c' in self.backend.tabla:
            print("Filtrando datos diarios (real crudo).")
            fecha_inicio = input("Ingrese la fecha de inicio (día-mes-año): ")
            fecha_fin = input("Ingrese la fecha de fin (día-mes-año): ")

            try:
                datos_filtrados = self.backend.filtrar_por_fecha_diaria(fecha_inicio, fecha_fin)
                print(f"Filtrado entre {fecha_inicio} y {fecha_fin}. Datos:")
                self.vista_general(datos_filtrados)
                input("teclee para seguir")
            except ValueError as e:
                print(e)

        elif any(x in self.backend.tabla for x in ['produccion_g', 'potencial', 'diferida']):
            print("Filtrando datos mensuales (promedios).")
            fecha_inicio = input("Ingrese el mes de inicio (mes-año): ")
            fecha_fin = input("Ingrese el mes de fin (mes-año): ")
            try:
                datos_filtrados = self.backend.filtrar_por_fecha_mensual(fecha_inicio, fecha_fin)
                print(f"Filtrado entre {fecha_inicio} y {fecha_fin}. Datos:")
                self.vista_general(datos_filtrados)
                input("teclee para seguir")
            except ValueError as e:
                print(e)

    def filtro_por_valores(self):
        print("\nSeleccione el campo numérico para aplicar el filtro:")
        campos_numericos = [header for header in self.backend.headers if header not in ['fecha', 'id']]
        for i, campo in enumerate(campos_numericos):
            print(f"{i + 1}) {campo}")

        opcion = input("\nSeleccione una opción: ")
        try:
            campo_seleccionado = campos_numericos[int(opcion) - 1]
            valor_min = input(f"Ingrese el valor mínimo para {campo_seleccionado}: ")
            valor_max = input(f"Ingrese el valor máximo para {campo_seleccionado}: ")

            datos_filtrados = self.backend.filtrar_por_valores(campo_seleccionado, valor_min, valor_max)
            print(f"Filtrado entre {valor_min} y {valor_max}. Datos:")
            self.vista_general(datos_filtrados)
            input("teclee para seguir")
        except (ValueError, IndexError) as e:
            print("Error en la selección o en los valores ingresados:", e)


    def eliminar_fila(self):
        print("Seleccione una fila para eliminar:")
        for i, fila in enumerate(self.backend.datos):  # Cambiar a self.backend.datos
            print(f"{i}) {fila}")
        indice = int(input("Índice: "))
        try:
            self.backend.eliminar_fila(indice)  # Llamada al método del backend
            print("Fila eliminada.")
        except (IndexError, ValueError) as e:
            print(f"Error: {e}")

    def opciones_separacion(self):

        while True:
            print("\nOpciones de Separación:")
            print("1) Anual")
            print("2) Mensual")
            print("3) Volver")
            opcion = input("\nSeleccione una opción: ")

            tabla = PrettyTable()
            tabla.field_names = ["Índice"] + self.backend.headers
            filas_con_indices = [[i] + list(fila) for i, fila in enumerate(self.backend.datos)]

            if opcion == "1":
                print(self.backend.aplicar_separador("anual", tabla, filas_con_indices))
                input("teclee para seguir")
                break
            elif opcion == "2":
                print(self.backend.aplicar_separador("mensual", tabla, filas_con_indices))
                input("teclee para seguir")
                break
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    def vista_general(self, data):
        tabla = PrettyTable()
        tabla.field_names = ["Índice"] + self.backend.headers  # Agregamos el encabezado del índice
    
        # Preparamos todas las filas con su índice
        filas_con_indices = [[i] + list(fila) for i, fila in enumerate(data)]
    
        # Agregamos todas las filas a la tabla
        for fila in filas_con_indices:
            tabla.add_row(fila)
    
        print(tabla)
        
    def vista_edicion(self, headers, fila_original, indice_fila):
        tabla = PrettyTable()
        tabla.add_row(headers)
        tabla.add_row(fila_original)
        print("\n--- Editando Fila ---")
        print(tabla)

if __name__ == "__main__":
    conexion = base_ddatos()
    backend = ConsolaDBBackend(conexion, "public", "produccion_c")
    frontend = ConsolaDBFrontend(backend)
    frontend.menu_principal()