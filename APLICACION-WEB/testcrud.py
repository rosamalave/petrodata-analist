import sys
import pytest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QApplication
from main import MainApp  # Asegúrate de importar tu clase MainApp
from bd.conexion_bd import base_ddatos


@pytest.fixture(scope="session", autouse=True)
def qapplication():
    """Inicializa QApplication para las pruebas de PyQt5."""
    app = QApplication(sys.argv)
    yield app
    app.quit()


@pytest.fixture
def mock_main_app():
    # Mockea la conexión a la base de datos
    mock_bd = MagicMock(spec=base_ddatos)
    
    # Crea una instancia de MainApp con el mock de la base de datos
    app = MainApp("CRUDO", "public", "produccion_c")
    app.conectarbd = mock_bd  # Sustituye la conexión real con el mock
    
    # Simula datos en la tabla
    app.ui.tabla.rowCount = MagicMock(return_value=2)
    app.ui.tabla.setRowCount = MagicMock()
    app.ui.tabla.setItem = MagicMock()
    
    return app, mock_bd


def test_agregareditar(mock_main_app):
    app, mock_bd = mock_main_app

    # Configura el mock de la tabla para que simule una fila seleccionada
    fila_seleccionada = 0
    app.ui.tabla.currentRow = MagicMock(return_value=fila_seleccionada)

    # Simula celdas de la fila con algunos valores de prueba
    def mock_item(row, col):
        if row == fila_seleccionada:
            valores_fila = ["123", "producto_1", "valor_1", "valor_2", "valor_3"]
            return MagicMock(text=lambda: valores_fila[col])
        return None

    app.ui.tabla.item = MagicMock(side_effect=mock_item)

    # Simula que la base de datos devuelve los headers
    mock_bd.headers = MagicMock(return_value=["id", "id_producto", "col1", "col2", "col3"])

    # Llama a la función que se probará
    app.agregareditar(fila_seleccionada, "producto_1", "public", "produccion_c")
    
    # Verifica que se haya llamado al método de editar de la base de datos
    mock_bd.editar.assert_called_once()

    # Obtén los argumentos con los que se llamó a editar
    id_llamada, producto_llamado, nuevaf_llamada, esquema_llamado, tabla_llamado = mock_bd.editar.call_args[0]

    # Verifica que los datos sean los esperados
    assert id_llamada == 123  # El id debe ser un entero
    assert producto_llamado == "producto_1"
    assert nuevaf_llamada == ["valor_1", "valor_2", "valor_3"]  # Excluye 'id' y 'id_producto'
    assert esquema_llamado == "public"
    assert tabla_llamado == "produccion_c"


def test_no_editar_sin_fila_seleccionada(mock_main_app):
    app, mock_bd = mock_main_app

    # Configura el mock para que no haya una fila seleccionada
    app.ui.tabla.currentRow = MagicMock(return_value=-1)

    # Llama a la función que se probará
    app.agregareditar(-1, "CRUDO", "public", "produccion_c")
    
    # Verifica que no se haya llamado al método editar
    mock_bd.editar.assert_not_called()
