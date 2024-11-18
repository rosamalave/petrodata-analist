import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem
from primera_tabla import Ui_Form
from conexion_bd import base_ddatos
#esquema= "public" o "public2" | tabla= "produccion_c"
class MainApp(QWidget):
    def __init__(self, esquema,tabla):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Crear una instancia de la clase de conexión a la base de datos
        self.conectarbd = base_ddatos()

        # Inicializar la tabla en la interfaz con los datos desde la base de datos
        self.inicializar_tabla(esquema,tabla)  # Pasa el nombre de la tabla a inicializar

        # Conectar el botón "aggfila" al método agregar_fila
        self.ui.aggfila.clicked.connect(self.agregar_fila)

    def inicializar_tabla(self, esquema,tabla):
        # Crear un cursor
        cursor = self.conectarbd.conn.cursor()

        # Ejecutar consulta para obtener header de la tabla
        nombres = []
        self.conectarbd.header(cursor,nombres,esquema,tabla)
        
        # Ejecutar consulta para obtener datos de la tabla
        cursor.execute(f"SELECT * FROM {esquema}.{tabla}")
        rows = cursor.fetchall()  # Obtiene todas las filas

        # Configurar la tabla en la interfaz
        self.ui.tabla.setRowCount(len(rows))
        self.ui.tabla.setColumnCount(len(rows[0]))  # Configura el número de columnas según la base de datos

        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                self.ui.tabla.setItem(i, j, QTableWidgetItem(str(col)))  # Agrega los datos a la tabla
        
        self.ui.tabla.setColumnHidden(0, True)  # Oculta la primera columna
        self.ui.tabla.setColumnHidden(1, True)  # Oculta la segunda columna
        #asignando encabezados a la tabla
        for col in range(len(nombres)):
            self.ui.tabla.setHorizontalHeaderItem(col+2, QTableWidgetItem(nombres[col]))
        
        cursor.close()

    def agregareditar(self, producto,esquema,tabla):
        #falta modulo de validacion

        #extrayendo datos de la fila editada
        filaseleccionada = self.ui.tabla.currentRow()
        if filaseleccionada != -1:  # Si hay una fila seleccionada
            nuevaf = []
            for col in range(self.table.columnCount()):
                item = self.table.item(filaseleccionada, col)
                if item:
                    nuevaf.append(item.text())  # Guardar el texto de la celda
            print(f"Fila seleccionada:{nuevaf}")  # Mostrar la fila en la consola (opcional)

        if None == self.posicionfila():
            self.conectarbd.insertar(producto,nuevaf,esquema,tabla)
        else:
            self.conectarbd.editar(producto,nuevaf,esquema,tabla)


    def agregar_fila(self):
        # Obtiene el número de filas actuales y añade una nueva al final
        nfilas = self.ui.tabla.rowCount()
        self.ui.tabla.insertRow(nfilas)

        # Opcional: Si deseas que las celdas de la nueva fila estén vacías
        for col in range(self.ui.tabla.columnCount()):
            item = QTableWidgetItem("")  # Crea un item vacío
            self.ui.tabla.setItem(nfilas, col, item)  # Añade el item vacío a la nueva fila

    def posicionfila(self):
        # Obtener el índice de la fila seleccionada
        filaseleccionada = self.ui.tabla.currentRow()

        if filaseleccionada != -1:  # Verifica que haya una fila seleccionada
            #item(variable,posicion fila)
            item_id = self.item(filaseleccionada, 1)  # Columna 1 contiene el 'id'
            if item_id:  # Verifica que el item no sea None
                return int(item_id.text())  # Devuelve el id como entero
        return None  # Si no hay fila seleccionada, devuelve None

    


#def agregar datos/editar que retorne una cadena de  texto de una vez


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Inicia el MainApp y especifica el nombre de la tabla que deseas cargar al inicio
    mainApp = MainApp("public","produccion_c")
    mainApp.show()
    sys.exit(app.exec_())