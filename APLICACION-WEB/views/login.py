from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
from widgets.combobox import ButtonCustom
from models.conexion_bd import base_ddatos

class LoginView:
    
    def __init__(self, root, on_login):

        self.on_login=on_login
        self.conexion = base_ddatos()
        self.root = root
 
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path(
            r"R:\Rosa\PASANTIAS\PROYECTO-PDVSA\APLICACION-WEB\resources\images\login"
        )

        self.canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=519,
            width=862,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(0.0, 0.0, 862.0, 519.0, fill="#FFFFFF", outline="")

        self.canvas.create_text(
            560.0,
            271.0,
            anchor="nw",
            text="Usuario",
            fill="#667085",
            font=("Poppins Medium", 9 * -1),
        )

        self.canvas.create_text(
            562.0,
            324.0,
            anchor="nw",
            text="Contraseña",
            fill="#667085",
            font=("Poppins Medium", 9 * -1),
        )

        # Botón Ingresar
        self.button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            relief="flat",
        )
        self.button_1.place(x=606.0, y=404.0, width=136.8457, height=30.4102)

        # Botón Usuario
        options = ["Marielys", "Luis"]
        self.button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = ButtonCustom(
            self.root, options, self.button_image_2, width=227.06, height=22.3
        )
        self.button_2.place(x=561.0, y=293.0, width=227, height=22)

        # Imágenes
        self.image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(675.0, 112.0, image=self.image_1)

        self.image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(239.0, 265.0, image=self.image_2)

        self.image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(29.0, 25.0, image=self.image_3)

        self.canvas.create_text(
            44.0,
            17.0,
            anchor="nw",
            text="GBD PetroJunin",
            fill="#144A96",
            font=("Poppins Medium", 10 * -1),
        )

        # Botón Contraseña
        self.button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat",
        )
        self.button_3.place(x=562.0, y=345.0, width=227.0625, height=22.3008)

        # Entry para la contraseña
        self.entry = Entry(
            self.root, bg="#fafcfd", fg="black", bd=0, highlightthickness=0, font=("Poppins", 8)
        )

        # Eventos
        self.entry.bind("<Return>", self.on_entry_confirm)
        self.button_3.bind("<Button-1>", self.show_entry)

        # Textos adicionales
        self.canvas.create_text(
            605.0,
            180.0,
            anchor="nw",
            text="Inicio de sesión",
            fill="#1D2838",
            font=("Poppins Bold", 18 * -1),
        )

        self.canvas.create_text(
            568.0,
            216.0,
            anchor="nw",
            text="Bienvenid@, seleccione su usuario e",
            fill="#667084",
            font=("Poppins Medium", 11 * -1),
        )

        self.canvas.create_text(
            610.0,
            232.0,
            anchor="nw",
            text=" ingrese su contraseña",
            fill="#667084",
            font=("Poppins Medium", 11 * -1),
        )

        self.root.resizable(False, False)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def show_entry(self, event):
        """Muestra el campo de entrada sobre el botón de contraseña."""
        self.entry.place(
            x=self.button_3.winfo_x() + 8,
            y=self.button_3.winfo_y() + 3.5,
            width=self.button_3.winfo_width() * 0.92,
            height=self.button_3.winfo_height() * 0.7,
        )
        self.button_3.config(state="disabled")  # Deshabilitar el botón
        self.entry.focus()  # Dar foco al entry

    def on_entry_confirm(self, event):
        """Captura el texto ingresado en el campo de entrada."""
        texto_ingresado = self.entry.get()
        print("Texto ingresado:", texto_ingresado)
        self.entry.place_forget()  # Ocultar el entry
        self.button_3.config(state="normal")  # Habilitar el botón nuevamente

    def login(self):
        self.obtener_creds()
        
        if self.conexion.verificar_iniciar_sesion(self.usuario, self.contraseña):
            self.existe = True
            print("inicio de sesion exitoso")
            self.on_login(self.usuario, self.conexion)

    def obtener_creds(self):
        """Obtiene el usuario y la contraseña seleccionados e imprime el resultado."""
        self.usuario = self.button_2.selected_option.get()
        self.usuario =self.usuario.lower()
        self.contraseña = self.entry.get()
        print("Usuario: {}, Contraseña: {}".format(self.usuario, self.contraseña))

    def cerrarsesion(self):
        self.conexion.cerrar_sesion(self.usuario)

if __name__ == "__main__":
    root = Tk()
    app = LoginView(root, None)
    root.mainloop()