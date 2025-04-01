from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Frame
from views.tablawidget import EditableTable
from controllers.pruebabackend import ConsolaDBBackend

# Asumiendo que las rutas de los recursos se mantienen igual
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"R:\Rosa\PASANTIAS\PROYECTO-PDVSA\APLICACION-WEB\resources\images\homepage")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class HomePage(Frame):
    def __init__(self, parent):
        super().__init__(parent.notebook, bg="#FFFFFF", width=720, height=50)
        self.mainlayout = parent
        self.notebook = parent.notebook  # Referencia al notebook de MainLayout
        self.estadoslide=True
        self.backend= None
        self.setup_ui()

    def setup_ui(self):
        # Crear un lienzo de fondo
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=465,
            width=720,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Botón 1
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_button_1_click(),
            relief="flat"
        )
        self.button_1.place(
            x=523.0, y=71.25, width=144.4, height=71.77
        )

        # Botón 2
        self.button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_button_2_click(),
            relief="flat"
        )
        self.button_2.place(
            x=523.0, y=153.01, width=144.4, height=71.77
        )

        self.button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
        self.button_5 = Button(
            self,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_button_5_click(),
            relief="flat"
        )
        self.button_5.place(
            x=523.0, y=71.25, width=144.4, height=71.77
        )
        self.button_5.place_forget()

        # Botón 2
        self.button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
        self.button_6 = Button(
            self,
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_button_6_click(),
            relief="flat"
        )
        self.button_6.place(
            x=523.0, y=153.01, width=144.4, height=71.77
        )
        self.button_6.place_forget()
        # Rectángulos
        self.canvas.create_rectangle(56.0, 106.0, 459.0, 237.0, fill="#D9D9D9", outline="")
        self.canvas.create_rectangle(56.0, 291.0, 459.0, 420.0, fill="#D9D9D9", outline="")

        # Texto de bienvenida
        self.canvas.create_text(
            39.0, 31.0, anchor="nw", text="Bienvenid@ Marielys", fill="#000000", font=("Poppins Regular", 20 * -1)
        )

        # Botón 3
        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_button_slider(),
            relief="flat"
        )
        self.button_3.place(x=571.78, y=24.0, width=46.83, height=37.25)

        # Texto compromiso
        self.canvas.create_text(
            307.0, 267.0, anchor="nw", text="Compromiso semana #1", fill="#000000", font=("Poppins Regular", 12 * -1)
        )

        # Texto Plan de Producción
        self.canvas.create_text(
            341.0, 83.0, anchor="nw", text="Plan de Producción", fill="#000000", font=("Poppins Regular", 12 * -1)
        )

        # Botón 4
        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
        self.button_4 = Button(
            self,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_button_slider(),
            relief="flat"
        )
        self.button_4.place(x=571.78, y=234.78, width=46.83, height=37.25)

        # Imagen
        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(596.0, 353.0, image=self.image_image_1)

        # Texto secuencia pozos caídos
        self.canvas.create_text(
            531.0, 394.0, anchor="nw", text="secuencia pozos caidos", fill="#000000", font=("Poppins Regular", 11 * -1)
        )

    # Métodos de acción de los botones
    def on_button_1_click(self):
        self.create_table_view('produccion_c')

    def on_button_2_click(self):
        self.create_table_view('produccion_g')

    def on_button_5_click(self):
        self.create_table_view('diferida')

    def on_button_6_click(self):
        self.create_table_view('potencial')

    def create_table_view(self, tabla):
        print("Creando vista con tabla: {}".format(tabla))
        # Aquí, debes crear la instancia de EditableTable y pasar los parámetros
        # Ejemplo:
        self.backend = ConsolaDBBackend(self.mainlayout.conexion, self.mainlayout.usuario, "public", tabla)
        self.backend.cargar_datos()
        new_table = EditableTable(self.mainlayout, self.backend)  # Pasar la referencia a 'parent' (MainLayout)
        self.mainlayout.add_tab(new_table,tabla)  # Agregar la tabla al notebook

    def on_button_slider(self):
        self.estadoslide = not self.estadoslide 
        if self.estadoslide:
            self.button_1.place(x=523.0, y=71.25, width=144.4, height=71.77)
            self.button_2.place(x=523.0, y=153.01, width=144.4, height=71.77)
            self.button_5.place_forget()
            self.button_6.place_forget()
        else:
            self.button_5.place(x=523.0, y=71.25, width=144.4, height=71.77)
            self.button_6.place(x=523.0, y=153.01, width=144.4, height=71.77)
            self.button_1.place_forget()
            self.button_2.place_forget()
            
# Código para probar la clase
if __name__ == "__main__":
    root = Tk()
    root.geometry("720x465")
    root.configure(bg="#FFFFFF")
    root.resizable(False, False)

    homepage_frame = HomePage(root, None)
    homepage_frame.pack(fill="both", expand=True)

    root.mainloop()