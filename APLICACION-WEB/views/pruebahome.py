from PyQt5.QtWidgets import(
QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
QPushButton, QSlider, QFrame, QStackedWidget
)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt

class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home Page - Petrojunín")
        self.setGeometry(100, 100, 900, 600)

        # Contenedor principal
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        # Layout principal
        main_layout = QVBoxLayout(self.main_widget)

        # ===========================
        # 1. HEADER
        # ===========================
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 10, 10, 10)

        # Logo PDVSA
        logo_label = QLabel()
        logo_pixmap = QPixmap("pdvsalogo.png") # Reemplaza con la ruta de tu imagen
        logo_label.setPixmap(logo_pixmap.scaled(80, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        # Espaciador central
        header_layout.addStretch()

        # Texto clicable "Historial"
        historial_label = QLabel('<a href="#">Historial</a>')
        historial_label.setOpenExternalLinks(False) # Para manejar clics internamente
        historial_label.setCursor(QCursor(Qt.PointingHandCursor))
        header_layout.addWidget(historial_label, alignment=Qt.AlignRight)

        # Icono de usuario con hover y clic
        user_button = QPushButton("Usuario")
        user_button.setCursor(QCursor(Qt.PointingHandCursor))
        user_button.setStyleSheet(
        "QPushButton { border: none; background: transparent; color: black; }"
        "QPushButton:hover { color: blue; }"
        )
        header_layout.addWidget(user_button, alignment=Qt.AlignRight)

        # ===========================
        # 2. CUERPO
        # ===========================
        # Sección 1: Portada con imagen y texto
        portada_layout = QVBoxLayout()
        portada_layout.setContentsMargins(0, 0, 0, 0)

        portada_container = QWidget()
        portada_container.setStyleSheet("background-color: transparent;")
        portada_container.setLayout(QVBoxLayout())

        portada_image_label = QLabel()
        portada_pixmap = QPixmap("portadahome.png") # Reemplaza con la ruta de tu imagen
        portada_image_label.setPixmap(portada_pixmap.scaled(900, 200, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        portada_image_label.setAlignment(Qt.AlignCenter)

        # Texto superpuesto
        portada_text = QLabel("PETROJUNIN")
        portada_text.setAlignment(Qt.AlignCenter)
        portada_text.setStyleSheet(
        "font-size: 48px; font-weight: bold; color: #242d52;"
        "margin-top: -100px; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);"
        )

        # Añadir widgets al contenedor de portada
        portada_layout.addWidget(portada_image_label)
        portada_layout.addWidget(portada_text)

        # Sección 2: Bienvenida y slider
        bienvenida_layout = QVBoxLayout()
        bienvenida_label = QLabel("¡BIENVENIDO, USUARIO!")
        bienvenida_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        bienvenida_layout.addWidget(bienvenida_label, alignment=Qt.AlignLeft)

        # Línea separadora
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        bienvenida_layout.addWidget(separator)

        # Slider con categorías
        slider_layout = QHBoxLayout()
        categorias_label = QLabel("CATE<br>GORÍAS")
        categorias_label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
        categorias_label.setAlignment(Qt.AlignCenter)
        slider_layout.addWidget(categorias_label)

        # Slider de botones
        slider_stack = QStackedWidget()

        slide1 = QWidget()
        slide1_layout = QHBoxLayout()
        slide1.setLayout(slide1_layout)

        btn_produccion = QPushButton("Producción Crudo")
        btn_produccion.setStyleSheet("background-color: #242d52; color: white; border-radius: 15px; padding: 10px;")
        btn_equipos = QPushButton("Potencial")
        btn_equipos.setStyleSheet("background-color: #242d52; color: white; border-radius: 15px; padding: 10px;")
        slide1_layout.addWidget(btn_produccion)
        slide1_layout.addWidget(btn_equipos)

        slide2 = QWidget()
        slide2_layout = QHBoxLayout()
        slide2.setLayout(slide2_layout)

        btn_servicios = QPushButton("Diferida")
        btn_servicios.setStyleSheet("background-color: #242d52; color: white; border-radius: 15px; padding: 10px;")
        btn_presupuesto = QPushButton("Producción Gas")
        btn_presupuesto.setStyleSheet("background-color: #242d52; color: white; border-radius: 15px; padding: 10px;")
        slide2_layout.addWidget(btn_servicios)
        slide2_layout.addWidget(btn_presupuesto)

        slider_stack.addWidget(slide1)
        slider_stack.addWidget(slide2)

        # Botones de navegación del slider
        prev_button = QPushButton("<")
        prev_button.setCursor(QCursor(Qt.PointingHandCursor))
        prev_button.clicked.connect(lambda: slider_stack.setCurrentIndex(0))
        next_button = QPushButton(">")
        next_button.setCursor(QCursor(Qt.PointingHandCursor))
        next_button.clicked.connect(lambda: slider_stack.setCurrentIndex(1))

        slider_layout.addWidget(prev_button)
        slider_layout.addWidget(slider_stack)
        slider_layout.addWidget(next_button)

        bienvenida_layout.addLayout(slider_layout)

        # ===========================
        # Añadir layouts al principal
        # ===========================
        main_layout.addLayout(header_layout)
        main_layout.addLayout(portada_layout)
        main_layout.addLayout(bienvenida_layout)


if __name__ == "__main__":
    app = QApplication([])
    window = HomePage()
    window.show()
    app.exec_()