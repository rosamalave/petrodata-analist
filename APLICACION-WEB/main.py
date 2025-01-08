import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox
from vistalogin import vistalogin
from homepage import HomePage

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Aplicación")
        self.setFixedSize(1366, 768)

        # Crear un QTabWidget para manejar las pestañas
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        # Inicializa la vista de inicio de sesión
        self.login_view = vistalogin(self.show_home_page)
        self.tab_widget.addTab(self.login_view, "Inicio de Sesión")

        # Diccionario para controlar pestañas abiertas
        self.open_tabs = {}

    def show_home_page(self, usuario, conexion):
        # Crear HomePage
        self.home_page = HomePage(usuario, conexion, self.open_table_tab)
        self.tab_widget.addTab(self.home_page, "Home Page")
        self.tab_widget.setCurrentWidget(self.home_page)

        # Eliminar la pestaña de inicio de sesión
        self.tab_widget.removeTab(0)

    def open_table_tab(self, esquema, tabla):
        tab_name = f"{esquema}.{tabla}"

        # Verificar si ya está abierta
        if tab_name in self.open_tabs:
            index = self.open_tabs[tab_name]
            self.tab_widget.setCurrentIndex(index)
            return

        # Crear nueva pestaña
        try:
            table_view = self.home_page.create_table_view(esquema, tabla)
            index = self.tab_widget.addTab(table_view, tab_name)
            self.tab_widget.setCurrentWidget(table_view)
            self.open_tabs[tab_name] = index
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir la tabla: {str(e)}")

    def closeEvent(self, event):
        # Asegurarse de que el cierre de sesión sea seguro
        if self.tab_widget.count() > 1:
            reply = QMessageBox.question(
                self,
                "Cerrar aplicación",
                "¿Está seguro de cerrar la aplicación? Esto cerrará todas las pestañas.",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.No:
                event.ignore()
                return
        self.login_view.cerrarsesion()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())