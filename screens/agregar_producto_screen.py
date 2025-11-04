from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import Snackbar
from os.path import dirname, join
from data_manager import data_manager

class AgregarProductoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_image_path = None
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.build_ui()

    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        # Título
        title = MDLabel(
            text="Agregar Nuevo Producto",
            font_style="H5",
            halign="center"
        )
        layout.add_widget(title)

        # Campo Nombre
        self.nombre_field = MDTextField(
            hint_text="Nombre del producto",
            mode="rectangle"
        )
        layout.add_widget(self.nombre_field)

        # Campo Precio
        self.precio_field = MDTextField(
            hint_text="Precio",
            mode="rectangle",
            input_filter="float"
        )
        layout.add_widget(self.precio_field)

        # Campo Descripción
        self.descripcion_field = MDTextField(
            hint_text="Descripción",
            mode="rectangle",
            multiline=True
        )
        layout.add_widget(self.descripcion_field)

        # Seleccionar imagen
        image_layout = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
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
        layout.add_widget(image_layout)

        # Espacio flexible
        layout.add_widget(MDBoxLayout())

        # Botones
        buttons_layout = MDBoxLayout(orientation='horizontal', spacing=dp(20), size_hint_y=None, height=dp(50))

        cancelar_btn = MDFlatButton(
            text="Cancelar",
            on_release=self.cancelar
        )
        buttons_layout.add_widget(cancelar_btn)

        guardar_btn = MDRaisedButton(
            text="Guardar",
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.guardar
        )
        buttons_layout.add_widget(guardar_btn)

        layout.add_widget(buttons_layout)

        self.add_widget(layout)

    def cancelar(self, instance):
        app = MDApp.get_running_app()
        app.change_screen('mis_productos')

    def guardar(self, instance):
        nombre = self.nombre_field.text.strip()
        precio = self.precio_field.text.strip()
        descripcion = self.descripcion_field.text.strip()

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

        # Convertir precio a número
        try:
            precio_val = float(precio)
        except ValueError:
            Snackbar(text="El precio debe ser un número válido").open()
            return

        # Guardar producto usando data_manager
        product_data = {
            'nombre': nombre,
            'precio': precio_val,
            'descripcion': descripcion,
            'imagen': self.selected_image_path or '',
            'vistas': 0,
            'vendedor': data_manager.current_user['email'],
            'estado': 'Activo'
        }
        data_manager.add_product(product_data)

        Snackbar(text="Producto guardado exitosamente").open()
        app = MDApp.get_running_app()
        app.change_screen('mis_productos')
        # Refrescar la pantalla de mis productos después de cambiar
        mis_productos_screen = app.sm.get_screen('mis_productos')
        mis_productos_screen.clear_widgets()
        mis_productos_screen.build_ui()

    def open_file_manager(self, instance):
        self.file_manager.show(join(dirname(__file__), '..'))

    def select_path(self, path):
        self.selected_image_path = path
        self.image_label.text = f"Imagen seleccionada: {path.split('/')[-1]}"
        self.exit_manager()

    def exit_manager(self, *args):
        self.file_manager.close()
