from PyQt5 import QtWidgets, QtGui, QtCore
from controllers.pruebabackend import ConsolaDBBackend
from views.qtdesign import Ui_Form  # Importa tu diseño de tabla

class HomePage(QtWidgets.QWidget):
    def __init__(self, usuario, conexion, open_table_tab, parent=None):
        super(HomePage, self).__init__(parent)
        self.usuario = usuario
        self.conexion = conexion
        self.open_table_tab = open_table_tab  # Callback para abrir pestañas
        self.init_ui()

class HomePage(QtWidgets.QWidget):
    def __init__(self, usuario, conexion, open_table_tab, parent=None):
        super(HomePage, self).__init__(parent)
        self.usuario = usuario
        self.conexion = conexion
        self.open_table_tab = open_table_tab  # Callback para abrir pestañas
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QLabel#header {
                font-size: 24px;
                font-weight: bold;
                color: #242d52;
                text-align: center;
            }
            QPushButton {
                background-color: #242d52;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #1b223e;
            }
            QPushButton.navigation {
                font-size: 24px;
                background-color: transparent;
                border: none;
                color: #242d52;
            }
            QPushButton.navigation:hover {
                color: #1b223e;
            }
        """)

        # Layout principal
        main_layout = QtWidgets.QVBoxLayout(self)
        
        # Encabezado
        header = QtWidgets.QLabel("¡Bienvenido a PETROJUNÍN!")
        header.setObjectName("header")
        header.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(header)

        # Separador
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        main_layout.addWidget(separator)

        # Contenedor del slider
        self.slider_widget = QtWidgets.QWidget()
        self.slider_layout = QtWidgets.QStackedLayout(self.slider_widget)
        main_layout.addWidget(self.slider_widget)

        # Botones de navegación
        navigation_layout = QtWidgets.QHBoxLayout()
        prev_button = QtWidgets.QPushButton("❮")
        prev_button.setObjectName("prev_button")
        prev_button.setFixedSize(50, 50)
        prev_button.setCursor(QtCore.Qt.PointingHandCursor)
        prev_button.clicked.connect(self.show_previous_slide)
        prev_button.setObjectName("prev_button")
        prev_button.setProperty("class", "navigation")
        
        next_button = QtWidgets.QPushButton("❯")
        next_button.setObjectName("next_button")
        next_button.setFixedSize(50, 50)
        next_button.setCursor(QtCore.Qt.PointingHandCursor)
        next_button.clicked.connect(self.show_next_slide)
        next_button.setObjectName("next_button")
        next_button.setProperty("class", "navigation")

        navigation_layout.addWidget(prev_button)
        navigation_layout.addStretch()
        navigation_layout.addWidget(next_button)
        main_layout.addLayout(navigation_layout)

        # Crear los botones de tabla divididos en dos "slides"
        self.create_slider_pages()

        # Configurar la página inicial del slider
        self.current_slide_index = 0
        self.slider_layout.setCurrentIndex(self.current_slide_index)

    def create_slider_pages(self):
        tablas = [
            ("Producción Crudo", "produccion_c"),
            ("Potencial", "potencial"),
            ("Diferida", "diferidanp"),
            ("Producción Gas", "produccion_g"),
        ]

        # Cada slide tendrá dos botones
        for i in range(0, len(tablas), 2):
            slide = QtWidgets.QWidget()
            slide_layout = QtWidgets.QHBoxLayout(slide)

            # Añadir botones al slide
            for j in range(2):
                if i + j < len(tablas):
                    nombre, tabla = tablas[i + j]
                    boton = QtWidgets.QPushButton(nombre)
                    boton.setFixedSize(150, 150)
                    boton.clicked.connect(lambda _, t=tabla: self.open_table("public", t))
                    slide_layout.addWidget(boton)

            self.slider_layout.addWidget(slide)

    def show_previous_slide(self):
        self.current_slide_index = (self.current_slide_index - 1) % self.slider_layout.count()
        self.slider_layout.setCurrentIndex(self.current_slide_index)

    def show_next_slide(self):
        self.current_slide_index = (self.current_slide_index + 1) % self.slider_layout.count()
        self.slider_layout.setCurrentIndex(self.current_slide_index)

    def open_table(self, esquema, tabla):
        self.open_table_tab(esquema, tabla)

    def create_table_view(self, esquema, tabla):
        # Inicializa el backend de la tabla
        backend = ConsolaDBBackend(self.conexion, self.usuario, esquema, tabla)
        backend.cargar_datos()

        # Crear una nueva vista de tabla
        table_view = QtWidgets.QWidget()
        ui = Ui_Form(backend)
        ui.setupUi(table_view)

        return table_view
