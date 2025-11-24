import os
from kivymd.uix.screen import MDScreen
from kivymd.uix.carousel import MDCarousel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import AsyncImage
from kivymd.app import MDApp
from kivy.metrics import dp


class VisorImagenesScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.imagenes = []
        self.indice_inicial = 0
        self.root_path = os.getcwd()

    def on_pre_enter(self, *args):
        """Cada vez que entro, reconstruyo el visor con las imágenes actuales."""
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        layout = MDBoxLayout(orientation="vertical")

        # Toolbar con botón atrás
        toolbar = MDTopAppBar(
            title="Visor de Imágenes",
            left_action_items=[["arrow-left", lambda x: self.volver()]],
            elevation=10,
            size_hint_y=None,
            height=dp(56),
        )
        layout.add_widget(toolbar)

        # Carrusel para las imágenes
        carousel = MDCarousel(
            size_hint_y=1,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        for ruta_relativa in self.imagenes:
            # Si la ruta ya es absoluta, úsala tal cual
            if os.path.isabs(ruta_relativa):
                ruta_absoluta = ruta_relativa
            else:
                ruta_absoluta = os.path.join(self.root_path, ruta_relativa)

            async_img = AsyncImage(
                source=ruta_absoluta,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(1, 1),
            )
            carousel.add_widget(async_img)

        layout.add_widget(carousel)
        self.add_widget(layout)

        # Ir a la imagen inicial (si existe)
        if 0 <= self.indice_inicial < len(self.imagenes):
            carousel.index = self.indice_inicial

    def volver(self):
        app = MDApp.get_running_app()
        app.change_screen("detalle_producto")
