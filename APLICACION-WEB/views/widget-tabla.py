from tkinter import Tk, Frame
from tkintertable import TableCanvas, TableModel
from controllers.pruebabackend import ConsolaDBFrontend
from datetime import date
from collections import OrderedDict 

class WidgetTabla(Frame):
    def __init__(self, parent, data):
        super().__init__(parent)
        parent.title("Tabla con datos de BD")

        # DEBUG: Mostrar estructura de los datos antes de pasarlos al modelo
        print("Estructura de los datos para TableModel:")
        for key, value in data.items():
            print("Fila {}: {}".format(key,value))

        # Crear modelo de datos
        model = TableModel()
        model.importDict(data)  # Método correcto para cargar datos en Python 3.4

        # Crear y mostrar la tabla
        self.table = TableCanvas(self, model=model, editable=True)
        self.table.show()

        # Ajustar tamaño del frame
        self.pack(fill="both", expand=True)


def iniciar_sesion_y_mostrar_tabla():
    """Inicia sesión en la BD, obtiene los datos y luego crea la ventana con la tabla."""
    print("Iniciando sesión en la BD...")
    app = ConsolaDBFrontend()
    app.iniciar_sesion()  # Carga los datos

    if not app.backend.datos:
        print("Error: No se cargaron datos desde la BD.")
        return

    print("Datos cargados, creando ventana...")

    # Convertir datos a diccionario
    data = convertir_a_diccionario(app.backend.datos, app.backend.headers)

    # Crear ventana solo después de que los datos estén disponibles
    root = Tk()
    WidgetTabla(root, data)
    root.mainloop()

def convertir_a_diccionario(lista, columnas):
    """
    Convierte una lista de listas en el formato requerido por TableModel.
    - lista: datos obtenidos de la consulta a la base de datos (lista de listas).
    - columnas: nombres de las columnas.
    """
    data = OrderedDict()  # Usamos OrderedDict para mantener el orden
    for i, fila in enumerate(lista):  # i = número de fila
        data[i] = OrderedDict(
            (col, str(fila[j]) if isinstance(fila[j], date) else fila[j])  # Convierte fechas a strings
            for j, col in enumerate(columnas)
        )
    return data

# Ejecutar la aplicación solo después de iniciar sesión
if __name__ == "__main__":
    iniciar_sesion_y_mostrar_tabla()