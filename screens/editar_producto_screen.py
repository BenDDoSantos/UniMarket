from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from os.path import dirname, join
from data_manager import data_manager

class EditarProductoScreen(MDScreen):
    def __init__(self, producto=None, **kwargs):
        super().__init__(**kwargs)
        self.producto = producto or {}
        self.selected_image_path = None
        self.selected_category = None
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.build_ui()

    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical')

        # Toolbar
        toolbar = MDTopAppBar(
            title="Editar Producto",
            left_action_items=[["arrow-left", lambda x: self.go_back()]]
        )
        layout.add_widget(toolbar)

        # Contenido
        content = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        # Título
        title = MDLabel(
            text="Editar Producto",
            font_style="H5",
            halign="center"
        )
        content.add_widget(title)

        # Campo Nombre
        self.nombre_field = MDTextField(
            hint_text="Nombre del producto",
            mode="rectangle",
            text=self.producto.get('nombre', '')
        )
        content.add_widget(self.nombre_field)

        # Campo Precio
        self.precio_field = MDTextField(
            hint_text="Precio",
            mode="rectangle",
            input_filter="float",
            text=str(self.producto.get('precio', '')).replace('$', '').replace('.', '').replace(',', '')
        )
        content.add_widget(self.precio_field)

        # Campo Descripción
        self.descripcion_field = MDTextField(
            hint_text="Descripción",
            mode="rectangle",
            multiline=True,
            text=self.producto.get('descripcion', '')
        )
        content.add_widget(self.descripcion_field)

        # Campo Estado
        self.estado_field = MDTextField(
            hint_text="Estado",
            mode="rectangle",
            text=self.producto.get('estado', '')
        )
        content.add_widget(self.estado_field)

        # Selector de categoría
        category_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        current_category = self.producto.get("categoria", "")
        self.category_button = MDRaisedButton(
            text=current_category if current_category else "Seleccionar categoría",
            on_release=self.open_category_menu,
            size_hint=(1, None),
            height=dp(40)
        )
        category_layout.add_widget(self.category_button)
        content.add_widget(category_layout)

        # Seleccionar imagen
        image_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        current_image = self.producto.get("imagen", "")
        if current_image:
            self.image_label = MDLabel(
                text=f"Imagen actual: {current_image.split('/')[-1]}",
                halign="left",
                valign="center"
            )
        else:
            self.image_label = MDLabel(
                text="No se ha seleccionado imagen",
                halign="left",
                valign="center"
            )
        self.image_label.bind(size=self.image_label.setter('text_size'))
        select_image_btn = MDIconButton(
            icon="camera",
            on_release=self.open_file_manager
        )
        image_layout.add_widget(self.image_label)
        image_layout.add_widget(select_image_btn)
        content.add_widget(image_layout)

        # Espacio flexible
        content.add_widget(MDBoxLayout())

        # Botones
        buttons_layout = MDBoxLayout(orientation='horizontal', spacing=dp(20), size_hint_y=None, height=dp(50))

        cancelar_btn = MDFlatButton(
            text="Cancelar",
            on_release=self.go_back
        )
        buttons_layout.add_widget(cancelar_btn)

        guardar_btn = MDRaisedButton(
            text="Guardar Cambios",
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.guardar_cambios
        )
        buttons_layout.add_widget(guardar_btn)

        content.add_widget(buttons_layout)

        layout.add_widget(content)

        self.add_widget(layout)

    def go_back(self, instance=None):
        app = MDApp.get_running_app()
        app.change_screen('mis_productos')

    def guardar_cambios(self, instance):
        nombre = self.nombre_field.text.strip()
        precio = self.precio_field.text.strip()
        descripcion = self.descripcion_field.text.strip()
        estado = self.estado_field.text.strip()

        # Validar campos obligatorios
        if not nombre:
            dialog = MDDialog(
                title="Error",
                text="El nombre del producto es obligatorio",
                buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
            return
        if not precio:
            dialog = MDDialog(
                title="Error",
                text="El precio es obligatorio",
                buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
            return
        if not descripcion:
            dialog = MDDialog(
                title="Error",
                text="La descripción es obligatoria",
                buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
            return
        if not estado:
            dialog = MDDialog(
                title="Error",
                text="El estado es obligatorio",
                buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
            return

        # Obtener categoría (usar la seleccionada o la actual)
        categoria = self.selected_category if self.selected_category else self.producto.get("categoria", "")

        # Actualizar producto usando data_manager
        updated_data = {
            'nombre': nombre,
            'precio': int(precio),
            'descripcion': descripcion,
            'estado': estado,
            'categoria': categoria,
            'imagen': self.selected_image_path if self.selected_image_path else self.producto.get("imagen", "")
        }
        data_manager.update_product(self.producto['id'], updated_data)

        # Mostrar diálogo de éxito
        dialog = MDDialog(
            title="Éxito",
            text="Producto actualizado exitosamente",
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.success_callback(dialog))]
        )
        dialog.open()

    def success_callback(self, dialog):
        dialog.dismiss()
        app = MDApp.get_running_app()
        # Refrescar la pantalla de productos
        try:
            productos_screen = app.sm.get_screen('productos')
            productos_screen.clear_widgets()
            productos_screen.build_ui()
        except Exception as e:
            print(f"Error al refrescar productos_screen: {e}")
        # Refrescar la pantalla de mis productos
        mis_productos_screen = app.sm.get_screen('mis_productos')
        mis_productos_screen.clear_widgets()
        mis_productos_screen.build_ui()
        self.go_back()

    def open_file_manager(self, instance):
        self.file_manager.show(join(dirname(__file__), '..'))

    def select_path(self, path):
        self.selected_image_path = path
        self.image_label.text = f"Imagen seleccionada: {path.split('/')[-1]}"
        self.exit_manager()

    def exit_manager(self, *args):
        self.file_manager.close()

    def open_category_menu(self, instance):
        """Abrir menú desplegable para seleccionar categoría"""
        categorias = data_manager.get_categories()
        menu_items = [
            {
                "text": categoria["nombre"],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=categoria["nombre"]: self.select_category(x),
            } for categoria in categorias
        ]

        self.category_menu = MDDropdownMenu(
            caller=self.category_button,
            items=menu_items,
            width_mult=4,
        )
        self.category_menu.open()

    def select_category(self, categoria):
        """Seleccionar categoría del menú"""
        self.selected_category = categoria
        self.category_button.text = categoria
        self.category_menu.dismiss()
