import os
from kivymd.uix.screen import MDScreen
from kivymd.uix.carousel import MDCarousel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.image import AsyncImage
from kivymd.app import MDApp
from kivy.metrics import dp


class VisorImagenesScreen(MDScreen):
    def __init__(self, imagenes=None, indice_inicial=0, **kwargs):
        super().__init__(**kwargs)
        self.imagenes = imagenes or []
        self.indice_inicial = indice_inicial
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.build_ui()

    def build_ui(self):
        # Toolbar with back button
        toolbar = MDTopAppBar(
            title="Visor de Imágenes",
            left_action_items=[["arrow-left", lambda x: self.volver()]],
            pos_hint={"top": 1}
        )
        self.add_widget(toolbar)

        # Carousel for images
        carousel = MDCarousel(
            size_hint_y=None,
            height=dp(600),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        for ruta_relativa in self.imagenes:
            ruta_absoluta = os.path.join(self.root_path, ruta_relativa)
            async_img = AsyncImage(
                source=ruta_absoluta,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(1, 1),
            )
            carousel.add_widget(async_img)

        self.add_widget(carousel)

        # Go to the initial image in the carousel
        if 0 <= self.indice_inicial < len(self.imagenes):
            carousel.go_to(self.indice_inicial)

    def volver(self):
        app = MDApp.get_running_app()
        app.change_screen("detalle_producto")
