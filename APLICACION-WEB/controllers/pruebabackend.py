from prettytable import PrettyTable
import pg8000
from models.conexion_bd import base_ddatos
from datetime import datetime
from decimal import Decimal
import os
import json

# Función para limpiar la consola
def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

class ConsolaDBBackend:
    def __init__(self, conexion_bd, usuario, esquema, tabla):
        self.conexion = conexion_bd
        self.esquema = esquema
        self.tabla = tabla
        self.datos = []  # Sin ID
        self.datosall = []  # Con ID
        self.headers = []
        self.usuario = usuario
        self.nuevas_filas_indices = []  # Lista para almacenar índices de filas nuevas

    def cargar_datos(self):
        if self.conexion.conn:
            try:
                
                self.headers = []
                cursor = self.conexion.conn.cursor()
                
                cadenanombres = self.conexion.header(cursor, self.headers, self.esquema, self.tabla)

                # Ejecutar la primera consulta y almacenar los datos sin ID
                query1 = "SELECT {} FROM {}.{} ORDER BY fecha DESC LIMIT 10".format(cadenanombres,self.esquema,self.tabla) 
                print (query1)
                cursor.execute(query1)  # `None` porque no hay parámetros
                self.datos = [list(row) for row in cursor.fetchall()]
                #self.datos = cursor.fetchall()  # Obtener los resultados
                
                #Ejecutar la segunda consulta y almacenar los datos con ID
                query2 = "SELECT * FROM {}.{} ORDER BY fecha DESC LIMIT 10".format(self.esquema,self.tabla)
                cursor.execute(query2)  # `None` porque no hay parámetros
                self.datosall = [list(row) for row in cursor.fetchall()] 
                #self.datosall = cursor.fetchall()  # Obtener los resultados
                print("datos all")
                print(self.datosall)
                cursor.close()  # Cerrar el cursor después de usarlo
                
            except Exception as e:
                print("Error al cargar datos: {}".format(e))

    def deshacer_ultimo_cambio(self):
        # 0: falso, 1: verdadero, 2: ocultar (1 verdadero + 1 ocultar)
        bandera = 0

        try:
            # Paso 1: Ejecutar la consulta para obtener el historial de modificaciones
            query = """
                SELECT *
                FROM public2.historial_modificaciones
                WHERE usuario = {}
                AND tabla_afectada = {}
                AND estado = 'vigente'  -- Condición añadida
                AND accion NOT IN ('Inicio de sesion', 'Cierre de sesion')
                AND fecha >= (
                    SELECT MAX(fecha)
                    FROM public2.historial_modificaciones
                    WHERE usuario = {} AND accion = 'Inicio de sesion'
                )
                ORDER BY fecha DESC
                LIMIT 2;
            """.format(self.usuario, self.tabla, self.usuario)

            cursor = self.conexion.conn.cursor()
            cursor.execute(query)
            cambios = cursor.fetchall()
            cursor.close()  # Cerrar el cursor después de obtener los resultados

            # Si no hay cambios registrados, salir de la función
            if not cambios:
                print("No hay cambios recientes para deshacer.")
                return bandera
            
            # Si hay un solo cambio registrado, marcar como "oculto"
            if len(cambios) == 1:
                bandera = 2
            
            ultimo_cambio = cambios[0]

            print("Cantidad de filas obtenidas: {}".format(len(cambios)))
            print("Datos obtenidos: {}".format(cambios))
            print("Último cambio: {}".format(ultimo_cambio))

            # Descomponer el registro (pg8000 devuelve listas)
            id_cambio, tabla_afectada, accion, detalle_json, fecha, usuario, estado = ultimo_cambio

            # Marcar el cambio como "deshecho"
            cursor = self.conexion.conn.cursor()
            cursor.execute("""
                UPDATE public2.historial_modificaciones
                SET estado = 'deshecho'
                WHERE id = %s;
            """, (id_cambio,))
            self.conexion.conn.commit()
            cursor.close()

            # Convertir el detalle JSONB a un diccionario
            detalle = detalle_json

            # Obtener el ID de la fila afectada desde el detalle
            id_fila_afectada = detalle.get("id_{}".format(self.tabla))

            # Paso 2: Filtrar los valores del detalle según los headers
            detalle_filtrado = [detalle[header] for header in self.headers if header in detalle]

            # Desactivar triggers antes de modificar datos
            cursor = self.conexion.conn.cursor()
            cursor.execute("ALTER TABLE public.{} DISABLE TRIGGER {}_historial;".format(self.tabla, self.tabla))
            self.conexion.conn.commit()
            cursor.close()

            if accion == 'INSERT':
                # Si fue un insert, eliminar el registro
                self.conexion.eliminar(id_fila_afectada, 'public', tabla_afectada)
                self.cargar_datos()
                print("Registro con ID {} eliminado de la tabla {}.".format(id_fila_afectada, tabla_afectada))
                bandera += 1

            elif accion == 'UPDATE':
                # Si fue un update, restaurar el registro anterior
                self.conexion.editar(id_fila_afectada, None, detalle_filtrado, 'public', tabla_afectada)
                print(detalle_filtrado)
                print("Registro con ID {} restaurado a su estado anterior en la tabla {}.".format(id_fila_afectada, tabla_afectada))
                self.cargar_datos()
                bandera += 1

            elif accion == 'DELETE':
                # Si fue un delete, insertar nuevamente el registro
                self.conexion.insertar(id_fila_afectada, detalle_filtrado, 'public', tabla_afectada)
                print("Registro con ID {} restaurado en la tabla {}.".format(id_fila_afectada, tabla_afectada))
                self.cargar_datos()
                bandera += 1

            else:
                print("No se pudo realizar el cambio.")
                bandera = 0

            # Reactivar triggers después de modificar datos
            cursor = self.conexion.conn.cursor()
            cursor.execute("ALTER TABLE public.{} ENABLE TRIGGER {}_historial;".format(self.tabla, self.tabla))
            self.conexion.conn.commit()
            cursor.close()

        except Exception as e:
            print("Error al deshacer el último cambio: {}".format(e))
            bandera = 0

        return bandera

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
                    tabla.add_row(["----- {} -----".format(nombre_mes)] + [""] * len(self.headers))
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
            print("id superficial: {}".format(indice_superficial))
            id_real = self.datosall[indice_superficial][0]
            print("id real: {}".format(id_real))
            self.conexion.eliminar(id_real, self.esquema, self.tabla)
            
            # También eliminar de self.datos si está presente
            self.datos.pop(indice_superficial)
        self.cargar_datos()

    def validar(self, valor, esquema, tabla, columna, permite_nulo=False):

        # Consultar tipo de dato directamente desde la base de datos
        cursor = self.conexion.conn.cursor()
        query = """
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
            raise ValueError("No se pudo obtener el tipo de dato para la columna '{}'.".format(columna))

        tipo_esperado = tipo_dato[0]  # pg8000 devuelve listas, así que esto sigue funcionando

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
                    raise ValueError("El valor '{}' no puede ser negativo.".format(valor))
            except ValueError:
                raise ValueError("El valor '{}' no es un número válido.".format(valor))
            return True

        elif tipo_esperado == 'date':
            try:
                fecha = datetime.strptime(valor, "%Y-%m-%d")
                if fecha > datetime.today():
                    raise ValueError("El valor '{}' no puede ser una fecha futura.".format(valor))
            except ValueError:
                raise ValueError("El valor '{}' no tiene un formato de fecha válido (yyyy-mm-d).".format(valor))
            return True

        else:
            raise ValueError("El tipo de dato '{}' no está soportado.".format(tipo_esperado))
        
    def agregar_fila(self):
        nueva_fila = [None] * len(self.headers)  # Crear una nueva fila vacía
        self.datos.append(nueva_fila)  # Agregar la nueva fila a los datos
        self.nuevas_filas_indices.append(len(self.datos) - 1)  # Guardar el índice de la nueva fila



    def filtro_por_fecha(self, fecha_inicio, fecha_fin):
        if 'produccion_c' in self.tabla:
            datos_filtrados = self.filtrar_por_fecha_diaria(fecha_inicio, fecha_fin)
        elif any(x in self.tabla for x in ['produccion_g', 'potencial', 'diferida']):
            datos_filtrados = self.filtrar_por_fecha_mensual(fecha_inicio, fecha_fin)
        return datos_filtrados 

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
    def __init__(self):
        self.backend = None  # Se inicializa como None hasta que se complete el inicio de sesión
        self.iniciar_sesion()
        self.menu_principal()

    def iniciar_sesion(self):
        print("--- Inicio de sesión ---")
        sesion=False
        while sesion==False:
            self.usuario = input("Usuario: ")
            contraseña = input("Contraseña: ")
            tabla = input("Tabla: ")

            
            conexion = base_ddatos()
            if conexion.verificar_iniciar_sesion(self.usuario, contraseña):
                self.backend = ConsolaDBBackend(conexion, self.usuario, "public", tabla)
                self.backend.cargar_datos()
                print("Inicio de sesión exitoso.")
                sesion=True
            else:
                print("Credenciales incorrectas. Intente de nuevo.")
           

    def menu_principal(self):
        while True:
            #limpiar_consola()
            self.vista_general(self.backend.datos)
            print("\nMenú Principal:")
            print("1) Agregar fila")
            print("2) Editar fila")
            print("3) Eliminar fila")
            print("4) Filtro por fecha")
            print("5) Filtro por valores")
            print("6) Opciones de Separación")
            print("7) Cerrar sesión y salir")
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
                self.cerrar_sesion()
                print("Saliendo del programa.")
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    def cerrar_sesion(self):
        if self.backend:
            self.backend.conexion.cerrar_sesion(self.usuario)
            print("Sesión cerrada correctamente.")

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

                    nuevo_valor = input("Ingrese el nuevo valor para '{}': ".format(self.backend.headers[columna]))
                    cambios[columna] = nuevo_valor
                    fila[columna] = nuevo_valor  # Actualizar dinámicamente la fila
                except ValueError as e:
                    print("Error: {}".format(e))
                    continue

            if cambios:
                self.backend.agregar_datos(operacion, indice, cambios)

        except (ValueError, IndexError) as e:
            print("Error: {e}".format(e))

    def filtro_por_fecha(self):
        if 'produccion_c' in self.backend.tabla:
            print("Filtrando datos diarios (real crudo).")
            fecha_inicio = input("Ingrese la fecha de inicio (día-mes-año): ")
            fecha_fin = input("Ingrese la fecha de fin (día-mes-año): ")

            try:
                datos_filtrados = self.backend.filtrar_por_fecha_diaria(fecha_inicio, fecha_fin)
                print("Filtrado entre {} y {}. Datos:".format(fecha_inicio,fecha_fin))
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
                print("Filtrado entre {} y {}. Datos:".format(fecha_inicio,fecha_fin))
                self.vista_general(datos_filtrados)
                input("teclee para seguir")
            except ValueError as e:
                print(e)

    def filtro_por_valores(self):
        print("\nSeleccione el campo numérico para aplicar el filtro:")
        campos_numericos = [header for header in self.backend.headers if header not in ['fecha', 'id']]
        for i, campo in enumerate(campos_numericos):
            print("{}) {}".format(i + 1,campo))

        opcion = input("\nSeleccione una opción: ")
        try:
            campo_seleccionado = campos_numericos[int(opcion) - 1]
            valor_min = input("Ingrese el valor mínimo para {}: ".format(campo_seleccionado))
            valor_max = input("Ingrese el valor máximo para {}: ".format(campo_seleccionado))

            datos_filtrados = self.backend.filtrar_por_valores(campo_seleccionado, valor_min, valor_max)
            print("Filtrado entre {} y {}. Datos:".format(valor_min,valor_max))
            self.vista_general(datos_filtrados)
            input("teclee para seguir")
        except (ValueError, IndexError) as e:
            print("Error en la selección o en los valores ingresados:", e)


    def eliminar_fila(self):
        print("Seleccione una fila para eliminar:")
        for i, fila in enumerate(self.backend.datos):  # Cambiar a self.backend.datos
            print("{}) {}".format(i,fila))
        entrada = input("Índice: ")
        print("Entrada recibida:", repr(entrada))  # `repr()` te muestra exactamente lo que se recibe
        indice = int(entrada)  # Aquí sabrás si el error viene por un valor inesperado.
        print("indice ingresado: {}".format(indice))
        try:
            self.backend.eliminar_fila(indice)  # Llamada al método del backend
            print("Fila eliminada.")
        except (IndexError, ValueError) as e:
            print("Error: {}".format(e))

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
    frontend = ConsolaDBFrontend()