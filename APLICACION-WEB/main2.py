import sys
from PyQt5 import QtWidgets, QtCore
from pruebabackend import ConsolaDBBackend
from qtdesign import Ui_Form
from bd.conexion_bd import base_ddatos


if __name__ == "__main__":
    # Crear una instancia de QApplication
    app = QtWidgets.QApplication(sys.argv)

    # Crear el contenedor principal de la ventana
    MainWindow = QtWidgets.QWidget()

    # Crear una instancia de la clase Ui_Form
    ui = Ui_Form()

    # Configurar la interfaz para el contenedor principal
    ui.setupUi(MainWindow)


    # Mostrar la ventana principal
    MainWindow.show()

    # Ejecutar el bucle principal de la aplicación
    sys.exit(app.exec_())