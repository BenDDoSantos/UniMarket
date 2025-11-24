from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from custom_file_manager import CustomFileManager
from data_manager import data_manager


class AgregarProductoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.selected_images = []
        self.selected_category = None

        # Requerido por CustomFileManager
        self.file_manager = CustomFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

        self.build_ui()

    # ------------------------------------------------------------
    # ---------------------- UI PRINCIPAL -------------------------
    # ------------------------------------------------------------

    def build_ui(self):

        root = MDBoxLayout(
            orientation="vertical"
        )
        self.add_widget(root)

        # ---------------- TOP BAR (BOTÓN VOLVER) ----------------
        toolbar = MDTopAppBar(
            title="Agregar Producto",
            elevation=2,
            left_action_items=[["arrow-left", lambda x: self.volver()]],
            pos_hint={"top": 1},
        )
        root.add_widget(toolbar)

        # ---------------- SCROLLVIEW ----------------
        scroll = MDScrollView(size_hint=(1, 1), do_scroll_y=True)
        root.add_widget(scroll)

        # CONTENEDOR PRINCIPAL
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=[dp(20), dp(20), dp(20), dp(20)],
            spacing=dp(25),
            size_hint_y=None,
        )
        main_layout.bind(minimum_height=main_layout.setter("height"))
        scroll.add_widget(main_layout)

        # ---------------- CAMPOS ----------------
        self.nombre_field = MDTextField(
            hint_text="Nombre del producto",
            mode="rectangle",
        )
        main_layout.add_widget(self.nombre_field)

        self.precio_field = MDTextField(
            hint_text="Precio",
            mode="rectangle",
            input_filter="float",
        )
        main_layout.add_widget(self.precio_field)

        self.descripcion_field = MDTextField(
            hint_text="Descripción",
            mode="rectangle",
            multiline=True,
        )
        main_layout.add_widget(self.descripcion_field)

        # ---------------- CATEGORÍA ----------------
        self.category_button = MDRaisedButton(
            text="Seleccionar categoría",
            on_release=self.open_category_menu,
            size_hint=(1, None),
            height=dp(45),
        )
        main_layout.add_widget(self.category_button)

        # ---------------- MINIATURAS ----------------
        main_layout.add_widget(MDLabel(text="Imágenes seleccionadas:", bold=True))

        self.thumbnail_scroll = MDScrollView(
            size_hint_y=None,
            height=dp(110),
            do_scroll_x=True,
            bar_width=dp(3),
            scroll_type=['bars'],
        )

        self.thumbnail_container = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            padding=dp(10),
            size_hint_x=None,
            height=dp(110),
            width=0,
        )

        self.thumbnail_scroll.add_widget(self.thumbnail_container)
        main_layout.add_widget(self.thumbnail_scroll)

        # ---------------- SELECCIONAR IMÁGENES ----------------
        image_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(45),
            spacing=dp(10),
        )

        self.image_label = MDLabel(
            text="No se ha seleccionado imagen",
            halign="left",
            valign="center",
        )
        self.image_label.bind(size=self.image_label.setter("text_size"))

        select_image_btn = MDIconButton(
            icon="camera",
            on_release=self.open_image_picker,
        )

        image_layout.add_widget(self.image_label)
        image_layout.add_widget(select_image_btn)
        main_layout.add_widget(image_layout)

        # ---------------- BOTONES ----------------
        buttons_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            size_hint_y=None,
            height=dp(50),
        )

        cancelar_btn = MDFlatButton(
            text="Cancelar",
            on_release=self.cancelar,
            theme_text_color="Custom",
            text_color=(0.3, 0.3, 0.3, 1),
        )

        guardar_btn = MDRaisedButton(
            text="Guardar",
            md_bg_color=self.theme_cls.primary_color,
            elevation=2,
            on_release=self.guardar,
        )

        buttons_layout.add_widget(cancelar_btn)
        buttons_layout.add_widget(guardar_btn)
        main_layout.add_widget(buttons_layout)

    # ------------------------------------------------------------
    # --------------------- BOTÓN VOLVER -------------------------
    # ------------------------------------------------------------

    def volver(self):
        app = MDApp.get_running_app()
        app.change_screen("mis_productos")

    # ------------------------------------------------------------
    # ------------------------ GUARDAR ----------------------------
    # ------------------------------------------------------------

    def cancelar(self, instance):
        self.volver()

    def guardar(self, instance):
        try:
            nombre = self.nombre_field.text.strip()
            precio = self.precio_field.text.strip()
            descripcion = self.descripcion_field.text.strip()

            if not data_manager.current_user:
                self.show_dialog("Error", "Debes iniciar sesión para agregar productos")
                return

            if not nombre:
                self.show_dialog("Campo obligatorio", "El nombre del producto es obligatorio")
                return

            if not precio:
                self.show_dialog("Campo obligatorio", "El precio es obligatorio")
                return

            try:
                precio_val = float(precio)
            except:
                self.show_dialog("Error", "El precio debe ser un número válido")
                return

            if not descripcion:
                self.show_dialog("Campo obligatorio", "La descripción es obligatoria")
                return

            if not self.selected_images:
                self.show_dialog("Campo obligatorio", "Debes seleccionar al menos una imagen")
                return

            product_data = {
                "nombre": nombre,
                "precio": precio_val,
                "descripcion": descripcion,
                "categoria": self.selected_category,
                "imagenes": self.selected_images,
                "vistas": 0,
                "vendedor": data_manager.current_user["email"],
                "estado": "Activo",
            }

            data_manager.add_product(product_data)

            self.show_dialog("Éxito", "Producto guardado exitosamente")

            self.nombre_field.text = ""
            self.precio_field.text = ""
            self.descripcion_field.text = ""
            self.selected_category = None
            self.category_button.text = "Seleccionar categoría"
            self.selected_images = []
            self.image_label.text = "No se ha seleccionado imagen"
            self.refresh_thumbnails()

            self.volver()

        except Exception as e:
            self.show_dialog("Error", str(e))

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

    # ------------------------------------------------------------
    # -------- FILEMANAGER: EXIT + SELECT_PATH  ------------------
    # ------------------------------------------------------------

    def exit_manager(self, *args):
        try:
            self.file_manager.close()
        except:
            pass

    def select_path(self, path):
        """Compatibilidad con CustomFileManager"""
        relative_path = data_manager.copy_image_to_assets(path)
        if relative_path:
            self.selected_images.append(relative_path)
            self.image_label.text = f"{len(self.selected_images)} imágenes seleccionadas"
            self.refresh_thumbnails()
        self.exit_manager()

    # ------------------------------------------------------------
    # ------------------ SELECCIONAR IMÁGENES WINDOWS ------------
    # ------------------------------------------------------------

    def open_image_picker(self, instance):
        from kivy import platform

        if platform == "win":
            try:
                import tkinter as tk
                from tkinter import filedialog
            except:
                self.image_label.text = "Tkinter no disponible"
                return

            root = tk.Tk()
            root.withdraw()

            paths = filedialog.askopenfilenames(
                title="Seleccionar imágenes",
                filetypes=[("Imagenes", "*.jpg *.jpeg *.png *.webp")],
            )

            root.destroy()

            if paths:
                for p in paths:
                    rel = data_manager.copy_image_to_assets(p)
                    if rel:
                        self.selected_images.append(rel)

                self.image_label.text = f"{len(self.selected_images)} imágenes seleccionadas"
                self.refresh_thumbnails()

        else:
            self.image_label.text = "Solo disponible en Windows"

    # ------------------------------------------------------------
    # ------------------------ MINIATURAS -------------------------
    # ------------------------------------------------------------

    def refresh_thumbnails(self):
        self.thumbnail_container.clear_widgets()

        if not self.selected_images:
            self.thumbnail_container.width = 0
            return

        total_width = 0
        from screens.image_thumbnail import ImageThumbnail

        for path in self.selected_images:
            thumb = ImageThumbnail(
                path=path,
                parent_screen=self,
                size_hint=(None, None),
                size=(dp(80), dp(80)),
            )
            self.thumbnail_container.add_widget(thumb)
            total_width += dp(80) + self.thumbnail_container.spacing

        self.thumbnail_container.width = total_width

    def remove_image(self, path):
        if path in self.selected_images:
            self.selected_images.remove(path)
            self.image_label.text = (
                f"{len(self.selected_images)} imágenes seleccionadas"
                if self.selected_images else "No se ha seleccionado imagen"
            )
            self.refresh_thumbnails()

    # ------------------------------------------------------------
    # ---------------------- CATEGORÍAS ---------------------------
    # ------------------------------------------------------------

    def open_category_menu(self, instance):
        categorias = data_manager.get_categories()

        menu_items = [
            {
                "text": categoria["nombre"],
                "viewclass": "OneLineListItem", 
                "on_release": lambda x=categoria["nombre"]: self.select_category(x),
            }
            for categoria in categorias
        ]

        self.category_menu = MDDropdownMenu(
            caller=self.category_button,
            items=menu_items,
            width_mult=4,
        )
        self.category_menu.open()

    def select_category(self, categoria):
        self.selected_category = categoria
        self.category_button.text = categoria
        self.category_menu.dismiss()



