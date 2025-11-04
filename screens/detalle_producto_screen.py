from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.uix.image import Image
from kivymd.app import MDApp
from data_manager import data_manager


class DetalleProductoScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.producto = None
        self.build_ui()

    def build_ui(self):
        if not self.producto:
            return

        # Incrementar vistas del producto
        data_manager.increment_product_views(self.producto['id'])

        # Layout principal
        main_layout = MDBoxLayout(orientation='vertical')

        # Toolbar superior
        toolbar = MDTopAppBar(
            title="Detalle del Producto",
            left_action_items=[["arrow-left", lambda x: self.volver()]],
        )
        main_layout.add_widget(toolbar)

        # Scroll para el contenido
        scroll = MDScrollView()
        content_layout = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=None, height=dp(600))

        # Imagen del producto (placeholder)
        img = Image(
            source=self.producto.get('imagen', ''),
            size_hint=(1, None),
            height=dp(200),
            allow_stretch=True
        )
        content_layout.add_widget(img)

        # Nombre del producto
        nombre = MDLabel(
            text=self.producto['nombre'],
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height=dp(40)
        )
        content_layout.add_widget(nombre)

        # Precio
        precio = MDLabel(
            text=f"Precio: ${self.producto['precio']}",
            font_style="H6",
            theme_text_color="Primary",
            halign="center",
            size_hint_y=None,
            height=dp(30)
        )
        content_layout.add_widget(precio)

        # Descripción
        descripcion = MDLabel(
            text=f"Descripción: {self.producto['descripcion']}",
            font_style="Body1",
            halign="left",
            size_hint_y=None,
            height=dp(60)
        )
        content_layout.add_widget(descripcion)

        # Vendedor
        vendedor = MDLabel(
            text=f"Vendedor: {self.producto['vendedor']}",
            font_style="Body2",
            halign="left",
            size_hint_y=None,
            height=dp(30)
        )
        content_layout.add_widget(vendedor)

        # Visualizaciones
        vistas = MDLabel(
            text=f"Visualizaciones: {self.producto['vistas']}",
            font_style="Body2",
            halign="left",
            size_hint_y=None,
            height=dp(30)
        )
        content_layout.add_widget(vistas)

        # Botones de acción
        buttons_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(50)
        )

        # Botón Contactar vendedor
        btn_contactar = MDRaisedButton(
            text="Contactar vendedor",
            on_release=self.contactar_vendedor
        )
        buttons_layout.add_widget(btn_contactar)

        # Botón Ver más del vendedor
        btn_ver_mas = MDRaisedButton(
            text="Ver más del vendedor",
            on_release=self.ver_mas_vendedor
        )
        buttons_layout.add_widget(btn_ver_mas)

        content_layout.add_widget(buttons_layout)

        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)

        self.add_widget(main_layout)

    def volver(self):
        """Volver a la pantalla de productos"""
        app = MDApp.get_running_app()
        app.change_screen('productos')

    def contactar_vendedor(self, instance):
        """Contactar al vendedor"""
        dialog = MDDialog(
            title="Contactar Vendedor",
            text=f"¿Deseas contactar a {self.producto['vendedor']}?\n\nSimulación: Se abriría WhatsApp con el número del vendedor.",
            size_hint=(0.8, 0.4),
            buttons=[
                MDRaisedButton(
                    text="WhatsApp",
                    on_release=lambda x: self.abrir_whatsapp()
                ),
                MDRaisedButton(
                    text="Cancelar",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def abrir_whatsapp(self):
        """Simulación de abrir WhatsApp"""
        print(f"Abriendo WhatsApp para contactar a {self.producto['vendedor']}")
        # Aquí iría la lógica real para abrir WhatsApp

    def ver_mas_vendedor(self, instance):
        """Ver más productos del vendedor"""
        dialog = MDDialog(
            title="Productos del Vendedor",
            text=f"Simulación: Mostraría otros productos de {self.producto['vendedor']}.\n\nEn una app real, esto navegaría a una pantalla con todos los productos del vendedor.",
            size_hint=(0.8, 0.4),
            buttons=[
                MDRaisedButton(
                    text="Ver productos",
                    on_release=lambda x: print("Navegando a productos del vendedor")
                ),
                MDRaisedButton(
                    text="Cerrar",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
