from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from data_manager import data_manager

class EditarProductoScreen(MDScreen):
    def __init__(self, producto=None, **kwargs):
        super().__init__(**kwargs)
        self.producto = producto or {}
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
            Snackbar(text="El nombre del producto es obligatorio").open()
            return
        if not precio:
            Snackbar(text="El precio es obligatorio").open()
            return
        if not descripcion:
            Snackbar(text="La descripción es obligatoria").open()
            return
        if not estado:
            Snackbar(text="El estado es obligatorio").open()
            return

        # Actualizar producto usando data_manager
        updated_data = {
            'nombre': nombre,
            'precio': int(precio),
            'descripcion': descripcion,
            'estado': estado
        }
        data_manager.update_product(self.producto['id'], updated_data)

        Snackbar(text="Producto actualizado exitosamente", duration=2.0).open()
        app = MDApp.get_running_app()
        # Refrescar la pantalla de mis productos
        mis_productos_screen = app.sm.get_screen('mis_productos')
        mis_productos_screen.clear_widgets()
        mis_productos_screen.build_ui()
        self.go_back()
