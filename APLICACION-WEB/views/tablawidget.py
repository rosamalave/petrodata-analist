import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  
from controllers.pruebabackend import ConsolaDBFrontend
import traceback
import os
import controllers.config

#quitar cierre de sesion con frontend 
#quitar iniciar sesion 

class EditableTable(tk.Frame):
    def __init__(self, layout, backend):
        super().__init__(layout.notebook)
        self.mainlayout = layout
        self.backend = backend

        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 🟢 Sidebar ahora está en la parte INFERIOR con disposición HORIZONTAL
        self.sidebar = tk.Frame(main_frame, height=50, bg="white")
        self.sidebar.pack(side=tk.BOTTOM, fill=tk.X)  # Se expande horizontalmente

        self.headers = self.backend.headers + ["Acciones"]  
        print("Headers cargados:", self.headers)

        self.create_filter_widgets()

        # 🟢 Botones alineados horizontalmente
        self.btn_add_row = tk.Button(self.sidebar, text="Agregar Fila", command=self.add_empty_row)
        self.btn_add_row.pack(side=tk.LEFT, padx=5, pady=10)

        self.btn_delete_row = tk.Button(self.sidebar, text="Eliminar Fila", command=self.delete_row, state=tk.DISABLED)
        self.btn_delete_row.pack(side=tk.LEFT, padx=5, pady=10)

        self.btn_undo_filter = tk.Button(self.sidebar, text="Deshacer Filtro", command=self.undo_filter, state=tk.DISABLED)
        self.btn_undo_filter.pack(side=tk.LEFT, padx=5, pady=10)

        self.btn_undo = tk.Button(self.sidebar, text="Deshacer Cambio", command=self.deshacer_ultimo_cambio, state=tk.DISABLED)
        self.btn_undo.pack(side=tk.LEFT, padx=5, pady=10)

        close_button = tk.Button(self.sidebar, text="Cerrar", command=self.close_tab)
        close_button.pack(side=tk.LEFT, padx=5, pady=10)

        # 🟢 Tabla en la parte superior
        table_frame = tk.Frame(main_frame)
        table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(table_frame, columns=self.headers, show="headings")

        style = ttk.Style()
        style.configure("Treeview", background="white",  foreground="black", fieldbackground="white")  # Color de fondo
        style.configure("Treeview.Heading", background="white", font=('Poppins', 10))

        for col in self.headers:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center", stretch=True)  

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.enable_editing)

        self.check_icon = controllers.config.cargar_imagen('check2.ico', (20, 20))  
        self.cancel_icon = controllers.config.cargar_imagen('cancel2.ico', (20, 20))  
            
        self.load_data(self.backend.datos)

        self.entry_vars = {}  
        self.entries = {}  
        self.current_item = None  
        self.previous_values = None  
        self.btn_save = None
        self.btn_cancel = None

        self.is_filter_applied = False  # Variable que indica si un filtro está activo
            # Evento de redimensionar la ventana
        self.bind("<Configure>", self.on_resize)

    def create_filter_widgets(self):
        return

    def filtro_por_valores(self, columna, min_val, max_val):
        """Filtra los datos según la columna y el rango de valores"""
        datos_filtrados = self.backend.filtrar_por_valores(columna, min_val, max_val)
        
        if datos_filtrados:
            self.load_data(datos_filtrados)
            self.is_filter_applied = True  # Marcamos que el filtro está activo
            self.btn_undo_filter.config(state=tk.NORMAL)  # Habilitamos el botón de deshacer filtro
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron datos que coincidan con los criterios.")

    def undo_filter(self):
        """Deshace el filtro y restaura los datos originales"""
        self.load_data(self.backend.datos)  # Restaura todos los datos
        self.is_filter_applied = False  # Marcamos que el filtro no está activo
        self.btn_undo_filter.config(state=tk.DISABLED)  # Deshabilitamos el botón de deshacer filtro

    def load_data(self, data):
        """Carga los datos en la tabla sin modificar self.backend.datos."""
        self.tree.delete(*self.tree.get_children())  # Limpiar la tabla antes de cargar datos

        for row in data:
            row_with_actions = row + [""]  # Agregar espacio vacío para "Acciones"
            self.tree.insert("", tk.END, values=row_with_actions)

    def add_empty_row(self):
        """Agrega una fila vacía""" 
        self.backend.agregar_fila()
        print("\nFila vacía agregada.")
        self.load_data(self.backend.datos)

    def delete_row(self):
        """Elimina la fila seleccionada de la base de datos y actualiza la tabla."""
        if not self.current_item:
            return

        # Obtener la posición de la fila seleccionada en la lista de datos
        row_index = self.tree.index(self.current_item)

        # Verificar que el índice es válido
        if row_index < 0 or row_index >= len(self.backend.datos):
            messagebox.showerror("Error", "No se pudo identificar la fila en la base de datos.")
            return

        # Confirmar la eliminación
        confirmar = messagebox.askyesno("Eliminar fila", "¿Está seguro de que desea eliminar esta fila?")
        if not confirmar:
            return

        # Intentar eliminar la fila de la base de datos
        try:
            self.backend.eliminar_fila(row_index)
            del self.backend.datos[row_index]  # Eliminar de la lista en memoria
            self.load_data(self.backend.datos)  # Recargar la tabla
            messagebox.showinfo("Éxito", "Fila eliminada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", "No se pudo eliminar la fila: {}".format(e))

        self.clear_entries()
        self.btn_delete_row.config(state=tk.DISABLED)

    def enable_editing(self, event):
        """Habilita la edición de una fila completa al hacer doble clic"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Limpiar ediciones previas
        self.clear_entries()

        self.current_item = selected_item[0]
        self.previous_values = self.tree.item(self.current_item, "values")  # Guardar valores originales

        # Crear cuadros de entrada en lugar de los valores actuales
        self.entries = {}
        self.entry_vars = {}

        headers = self.headers  # Asegúrate de que `self.headers` contenga los nombres de las columnas
        for i, col_name in enumerate(headers):  # Recorremos las columnas en el orden de headers
            if col_name.lower() == "acciones":  # Excluimos la columna "Acciones"
                continue

            # Obtener el valor actual para la celda
            value = self.previous_values[i]

            # Obtener la posición de la celda seleccionada
            col_id = "#{}".format(i+1)
            x, y, width, height = self.tree.bbox(self.current_item, column=col_id)

            if width == 0:
                continue

            # Variable de control para el Entry
            var = tk.StringVar(value=value)
            self.entry_vars[i] = var  # Usamos índice en lugar de nombre de columna

            # Crear el Entry con texto centrado
            entry = tk.Entry(self.tree, textvariable=var, font=("Arial", 10), justify="center")
            entry.place(x=x, y=y, width=width, height=height)
            self.entries[i] = entry  # Guardamos el Entry con el índice

            # Enfocar el primer campo editable (opcional)
            if i == 0:  # Primer campo editable
                entry.focus_set()

        # Agregar botones al final de la fila
        self.add_action_buttons()

        # Mostrar el botón de eliminar en la barra lateral
        self.btn_delete_row.config(state=tk.NORMAL)

    def add_action_buttons(self):
        """Añade botones de guardar y cancelar en la columna Acciones"""
        x, y, width, height = self.tree.bbox(self.current_item, column=len(self.headers) - 1)

        if self.btn_save:
            self.btn_save.destroy()
        if self.btn_cancel:
            self.btn_cancel.destroy()

        self.btn_save = tk.Button(self.tree, image=self.check_icon, command=self.save_changes, borderwidth=0)
        self.btn_save.place(x=x + 10, y=y, width=20, height=20)

        self.btn_cancel = tk.Button(self.tree, image=self.cancel_icon, command=self.cancel_edit, borderwidth=0)
        self.btn_cancel.place(x=x + 30, y=y, width=20, height=20)

    def save_changes(self):
        """Guarda los cambios realizados en la fila seleccionada."""
        if not self.current_item or not self.tree.exists(self.current_item):
            messagebox.showwarning("Advertencia", "No se ha seleccionado ninguna fila válida.")
            return

        try:
            row_index = self.tree.index(self.current_item)
            print("DEBUG: Índice de fila en la lista de datos: {} (tipo: {})".format(row_index, type(row_index)))

            if not (0 <= row_index < len(self.backend.datos)):
                messagebox.showerror("Error", "El índice está fuera del rango de datos.")
                return
        except Exception as e:
            print("ERROR: Al obtener el índice de la fila. Detalles: {}".format(str(e)))
            messagebox.showerror("Error", "No se pudo obtener el índice de la fila. Revisa la consola para más detalles.")
            return

        try:
            cambios = {}
            fila_actual = []

            # Excluir la columna "Acciones" obteniendo solo las columnas de la base de datos
            num_columnas_validas = len(self.backend.headers)

            for i in range(num_columnas_validas):  # Solo recorremos columnas válidas
                if i not in self.entry_vars:
                    print("WARNING: La clave '{}' no está en entry_vars.".format(i))
                    continue

                try:
                    nuevo_valor = self.entry_vars[i].get()
                    fila_actual.append(nuevo_valor)
                    cambios[i] = nuevo_valor
                except Exception as e:
                    print("ERROR: Al obtener el valor de la entrada para la columna {}. Detalles: {}".format(i, str(e)))

            print("DEBUG: Cambios a guardar: {}".format(cambios))

            if not cambios:
                print("WARNING: No se han realizado cambios.")
                return
        except Exception as e:
            print("ERROR: Al procesar los cambios. Detalles: {}".format(str(e)))
            messagebox.showerror("Error", "No se pudieron procesar los cambios. Revisa la consola para más detalles.")
            return

        # Guardar cambios y habilitar botón de deshacer
        try:
            if row_index < len(self.backend.datos):
                print("DEBUG: Datos actuales en backend: {}".format(self.backend.datos[row_index]))

                if row_index not in self.backend.nuevas_filas_indices:
                    self.backend.agregar_datos(self.backend.editar_fila, row_index, cambios)
                else:
                    self.backend.agregar_datos(self.backend.insertar_fila, row_index, cambios)
                    self.backend.nuevas_filas_indices.remove(row_index)

                new_values = [self.entry_vars[i].get() for i in range(len(self.headers)-1)]
                print("DEBUG: Nuevos valores a guardar en el Treeview: {}".format(new_values))

                self.tree.item(self.current_item, values=new_values + [""])
                self.clear_entries()
                self.load_data(self.backend.datos)  # Recargar datos sin "Acciones"
                
                # Habilitar el botón de deshacer
                self.btn_undo.config(state=tk.NORMAL)
                
        except Exception as e:
            print("ERROR: Al guardar los cambios. Detalles: {}".format(str(e)))
            messagebox.showerror("Error", "No se pudieron guardar los cambios. Revisa la consola para más detalles.")


    def cancel_edit(self):
        """Cancela la edición y restaura los valores originales"""
        if self.previous_values:
            self.tree.item(self.current_item, values=self.previous_values)
        self.clear_entries()

    def clear_entries(self):
        """Elimina los cuadros de entrada y resetea variables"""
        for entry in self.entries.values():
            entry.destroy()
        self.entries.clear()
        self.entry_vars.clear()
        self.current_item = None
        self.previous_values = None

        if self.btn_save:
            self.btn_save.destroy()
            self.btn_save = None
        if self.btn_cancel:
            self.btn_cancel.destroy()
            self.btn_cancel = None

        self.btn_delete_row.config(state=tk.DISABLED)
    def deshacer_ultimo_cambio(self):
        """Deshace el último cambio realizado en los datos."""
        try:
            deshecho = self.backend.deshacer_ultimo_cambio()
            
            if deshecho == 0:
                print("Error: No se pudo realizar el cambio de deshacer.")
                self.reiniciar_interfaz()
            elif deshecho == 1:
                print("Cambio deshecho exitosamente.")
                self.load_data(self.backend.datos)
            elif deshecho == 3:
                print("Deshacer finalizado.")
                self.btn_undo.config(state=tk.DISABLED)
                self.load_data(self.backend.datos)
        except Exception as e:
            print("Error al deshacer el cambio: {}".format(str(e)))
            messagebox.showerror("Error", "No se pudo deshacer el cambio. Revisa la consola para más detalles.")
            
    def reiniciar_interfaz(self):
        """Reinicia la interfaz en caso de error."""
        self.clear_entries()
        self.load_data(self.backend.datos)
        self.btn_undo.config(state=tk.DISABLED)

    def on_resize(self, event):
        """Reajusta la posición de los botones y los Entry cuando la ventana cambia de tamaño"""
        if self.current_item:
            # Recalcular la posición de los botones
            x, y, width, height = self.tree.bbox(self.current_item, column=len(self.headers) - 1)

            # Ajustar los botones según el nuevo tamaño
            spacing = 10
            button_width = 20
            total_width = width - (2 * spacing)
            offset = (total_width - (button_width * 2 + spacing)) / 2

            if self.btn_save:
                self.btn_save.place(x=x + offset, y=y, width=button_width, height=button_width)
            if self.btn_cancel:
                self.btn_cancel.place(x=x + offset + button_width + spacing, y=y, width=button_width, height=button_width)

            # Recalcular la posición y tamaño de los Entry
            for i, entry in enumerate(self.entries.values()):
                x, y, width, height = self.tree.bbox(self.current_item, column=i)
                if width > 0:
                    entry.place(x=x, y=y, width=width, height=height)

    def close_tab(self):
        """Pide al MainLayout que cierre la pestaña de esta tabla."""
        index = self.mainlayout.notebook.index(self)
        self.mainlayout.close_tab(index)
