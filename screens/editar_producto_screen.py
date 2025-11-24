from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivymd.app import MDApp
from data_manager import data_manager
import os


class EditarProductoScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.producto = None
        self.selected_images = []
        self.selected_category = None

    # =====================================================
    # Cargar producto
    # =====================================================
    def cargar_producto(self, producto):
        self.producto = producto
        self.selected_images = list(producto.get("imagenes", []))
        self.selected_category = producto.get("categoria")

        self.clear_widgets()
        self.build_ui()

    # =====================================================
    # UI COMPLETA
    # =====================================================
    def build_ui(self):

        root = MDBoxLayout(orientation="vertical")
        self.add_widget(root)

        # ----- TOPBAR -----
        toolbar = MDTopAppBar(
            title="Editar Producto",
            elevation=2,
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
        )
        root.add_widget(toolbar)

        # ====== SCROLL ======
        scroll = MDScrollView()
        root.add_widget(scroll)

        content = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(15), dp(20), dp(20)],
            spacing=dp(18),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))
        scroll.add_widget(content)

        # ===== INPUTS =====
        self.nombre_field = MDTextField(
            hint_text="Nombre del producto",
            mode="rectangle",
            text=self.producto.get("nombre", "")
        )
        content.add_widget(self.nombre_field)

        self.precio_field = MDTextField(
            hint_text="Precio",
            mode="rectangle",
            input_filter="float",
            text=str(self.producto.get("precio", "")),
        )
        content.add_widget(self.precio_field)

        self.descripcion_field = MDTextField(
            hint_text="Descripción",
            mode="rectangle",
            multiline=True,
            text=self.producto.get("descripcion", "")
        )
        content.add_widget(self.descripcion_field)

        # ===== ESTADO =====
        self.estado_button = MDRaisedButton(
            text=f"Estado: {self.producto.get('estado', 'Activo')}",
            size_hint=(1, None),
            height=dp(45),
            on_release=self.open_estado_menu
        )
        content.add_widget(self.estado_button)

        # ===== CATEGORÍA =====
        self.category_button = MDRaisedButton(
            text=self.selected_category if self.selected_category else "Seleccionar categoría",
            on_release=self.open_category_menu,
            size_hint=(1, None),
            height=dp(45)
        )
        content.add_widget(self.category_button)

        # ===== TÍTULO IMÁGENES =====
        content.add_widget(MDLabel(text="Imágenes:", bold=True, padding=[0, dp(10)]))

        # ===== MINIATURAS ORDENADAS =====
        self.thumbnail_scroll = MDScrollView(
            size_hint_y=None,
            height=dp(100),
            do_scroll_x=True,
            bar_width=dp(4),
            scroll_type=["bars"],
        )

        self.thumbnail_container = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            padding=dp(10),
            size_hint_x=None,
            height=dp(100),
            width=0,
            pos_hint={"center_y": 0.5},
        )


        self.thumbnail_scroll.add_widget(self.thumbnail_container)
        content.add_widget(self.thumbnail_scroll)

        self.refresh_thumbnails()

        # ===== BOTÓN AGREGAR IMÁGENES =====
        add_img_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40),
        )
        self.image_label = MDLabel(text="Agregar imágenes…")
        add_img_layout.add_widget(self.image_label)

        add_img_button = MDIconButton(icon="camera", on_release=self.open_image_picker)
        add_img_layout.add_widget(add_img_button)

        content.add_widget(add_img_layout)

        # ===== BOTONES ABAJO =====
        botones = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            size_hint_y=None,
            height=dp(55)
        )

        cancelar_btn = MDFlatButton(text="Cancelar", on_release=self.go_back)
        guardar_btn = MDRaisedButton(text="Guardar Cambios", on_release=self.guardar_cambios)

        botones.add_widget(cancelar_btn)
        botones.add_widget(guardar_btn)

        content.add_widget(botones)

    # =====================================================
    # MINIATURAS ORDENADAS
    # =====================================================
    def refresh_thumbnails(self):

        self.thumbnail_container.clear_widgets()

        if not self.selected_images:
            self.thumbnail_container.width = 0
            return

        from screens.image_thumbnail import ImageThumbnail

        total_width = 0

        for index, img in enumerate(self.selected_images):

            thumb = ImageThumbnail(
                path=img,
                parent_screen=self,
                size_hint=(None, None),
                size=(dp(80), dp(80)),
            )

            self.thumbnail_container.add_widget(thumb)
            total_width += dp(80)
            if index < len(self.selected_images) - 1:
                total_width += self.thumbnail_container.spacing

        self.thumbnail_container.width = total_width

    # =====================================================
    # ELIMINAR MINIATURA
    # =====================================================
    def remove_image(self, path):
        filename = os.path.basename(path)
        self.selected_images = [
            i for i in self.selected_images if os.path.basename(i) != filename
        ]
        self.refresh_thumbnails()

    # =====================================================
    # MENÚ ESTADO
    # =====================================================
    def open_estado_menu(self, instance):

        estados = ["Activo", "Pausado", "Vendido"]

        items = [
            {"text": e, "viewclass": "OneLineListItem", "on_release": lambda x=e: self.set_estado(x)}
            for e in estados
        ]

        self.estado_menu = MDDropdownMenu(
            caller=self.estado_button,
            items=items,
            width_mult=3
        )
        self.estado_menu.open()

    def set_estado(self, estado):
        self.estado_button.text = f"Estado: {estado}"
        self.producto["estado"] = estado
        self.estado_menu.dismiss()

    # =====================================================
    # MENÚ CATEGORÍA
    # =====================================================
    def open_category_menu(self, instance):
        categorias = data_manager.get_categories()

        items = [
            {"text": c["nombre"], "viewclass": "OneLineListItem", "on_release": lambda x=c["nombre"]: self.set_categoria(x)}
            for c in categorias
        ]

        self.category_menu = MDDropdownMenu(
            caller=self.category_button,
            items=items,
            width_mult=4
        )
        self.category_menu.open()

    def set_categoria(self, categoria):
        self.selected_category = categoria
        self.category_button.text = categoria
        self.category_menu.dismiss()

    # =====================================================
    # IMAGE PICKER WINDOWS
    # =====================================================
    def open_image_picker(self, instance):
        from kivy import platform
        if platform != "win":
            return

        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()

        paths = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            filetypes=[("Imagenes", "*.jpg *.jpeg *.png *.webp")]
        )
        root.destroy()

        if paths:
            for p in paths:
                rel = data_manager.copy_image_to_assets(p)
                if rel:
                    self.selected_images.append(rel)

            self.refresh_thumbnails()

    # =====================================================
    # GUARDAR CAMBIOS
    # =====================================================
    def guardar_cambios(self, instance):
        nombre = self.nombre_field.text.strip()
        precio = self.precio_field.text.strip()
        descripcion = self.descripcion_field.text.strip()

        if not nombre or not precio or not descripcion:
            self.show_dialog("Error", "Todos los campos son obligatorios.")
            return

        data_manager.update_product(self.producto["id"], {
            "nombre": nombre,
            "precio": float(precio),
            "descripcion": descripcion,
            "categoria": self.selected_category,
            "estado": self.producto.get("estado", "Activo"),
            "imagenes": self.selected_images,
        })

        data_manager.save_all_data()

        self.show_dialog("Éxito", "Cambios guardados correctamente.", callback=self.go_back)

    def show_dialog(self, title, message, callback=None):
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDRaisedButton(text="OK", on_release=lambda x: (dialog.dismiss(), callback() if callback else None))
            ]
        )
        dialog.open()

    # =====================================================
    # NAVEGACIÓN
    # =====================================================
    def go_back(self, *args):
        MDApp.get_running_app().change_screen("mis_productos")


