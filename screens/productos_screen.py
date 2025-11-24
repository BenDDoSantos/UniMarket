from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivymd.app import MDApp
from data_manager import data_manager
from components.custom_bottom_bar import CustomBottomBar
import os


# =========================
#     PRODUCT CARD
# =========================
class ProductCard(MDCard):
    def __init__(self, producto, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.size_hint = (None, None)
        self.size = (dp(160), dp(220))
        self.padding = dp(8)
        self.spacing = dp(5)
        self.elevation = 1
        self.radius = [dp(10)]

        # ============== MINIATURA ================
        imagenes = producto.get("imagenes", [])
        imagen_principal = imagenes[0] if imagenes else "assets/no_image.png"

        # Usamos la ruta tal como está guardada; si es relativa, Kivy la resuelve
        if not os.path.isabs(imagen_principal):
            src = imagen_principal
        else:
            src = imagen_principal

        img = AsyncImage(
            source=src,
            size_hint_y=0.60,
            allow_stretch=True,
            keep_ratio=True,
        )
        self.add_widget(img)

        # ============== NOMBRE ===================
        nombre = MDLabel(
            text=producto.get("nombre", ""),
            font_style="Body2",
            halign="left",
            size_hint_y=0.20,
        )
        self.add_widget(nombre)

        # ============== PRECIO ===================
        precio = MDLabel(
            text=f"${producto.get('precio', 0)}",
            font_style="H6",
            theme_text_color="Primary",
            halign="left",
            size_hint_y=0.20,
        )
        self.add_widget(precio)


# =========================
#     PRODUCTOS SCREEN
# =========================
class ProductosScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_category = None
        self.build_ui()

    def on_pre_enter(self, *args):
        """Recarga la pantalla cada vez que entras."""
        self.clear_widgets()
        self.build_ui()

    # ============================================================
    #                      BUILD UI
    # ============================================================
    def build_ui(self):

        main_layout = MDBoxLayout(orientation="vertical")

        # ========== TOOLBAR ==========
        toolbar = MDTopAppBar(
            title="Productos",
            elevation=2,
            size_hint_y=None,
            height=dp(56),
            left_action_items=[["menu", lambda x: self.toggle_nav_drawer()]],
            right_action_items=[
                ["magnify", lambda x: self.search()]
            ] + (
                [["filter-variant", lambda x: self.clear_filter()]]
                if self.selected_category else []
            ),
        )

        main_layout.add_widget(toolbar)

        # ========== SCROLL ==========
        scroll = MDScrollView(size_hint_y=1)
        products_grid = MDGridLayout(
            cols=2,
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None,
            adaptive_height=True,
        )

        # CARGAR PRODUCTOS
        productos = data_manager.get_all_products()

        if self.selected_category:
            productos = [
                p for p in productos
                if p.get("categoria") == self.selected_category
            ]

        # Construir cards
        for producto in productos:
            card = ProductCard(producto)
            card.bind(on_release=lambda x, p=producto: self.ver_detalle(p))
            products_grid.add_widget(card)

        scroll.add_widget(products_grid)
        main_layout.add_widget(scroll)

        # ========== BOTTOM BAR ==========
        bottom = CustomBottomBar(
            current_screen="productos",
            navigation_callback=self.navigate_to_screen,
        )
        main_layout.add_widget(bottom)

        self.add_widget(main_layout)

    # =============================================================
    #                         FUNCIONES
    # =============================================================
    def toggle_nav_drawer(self):
        MDApp.get_running_app().toggle_nav_drawer()

    def search(self):
        self.search_dialog = MDDialog(
            title="Buscar productos",
            type="custom",
            content_cls=MDTextField(
                hint_text="Buscar por nombre...",
                on_text_validate=self.filtrar_productos,
            ),
            buttons=[
                MDRaisedButton(text="Buscar", on_release=self.filtrar_productos),
                MDRaisedButton(
                    text="Cancelar",
                    on_release=lambda x: self.search_dialog.dismiss(),
                ),
            ],
        )
        self.search_dialog.open()

    def filtrar_productos(self, instance=None):
        search_text = self.search_dialog.content_cls.text.lower()
        self.search_dialog.dismiss()

        self.clear_widgets()
        self.build_ui()

        # Re-obtenemos el grid de productos dentro del nuevo layout
        main_layout = self.children[0]
        scroll = main_layout.children[1]  # [bottom_bar, scroll, toolbar]
        grid = scroll.children[0]

        grid.clear_widgets()

        productos = data_manager.get_all_products()
        productos = [
            p for p in productos
            if search_text in p.get("nombre", "").lower()
        ]

        for producto in productos:
            card = ProductCard(producto)
            card.bind(on_release=lambda x, p=producto: self.ver_detalle(p))
            grid.add_widget(card)

    def clear_filter(self):
        self.selected_category = None
        self.clear_widgets()
        self.build_ui()

    def set_category_filter(self, category_name):
        self.selected_category = category_name
        self.clear_widgets()
        self.build_ui()

    def ver_detalle(self, producto):
        data_manager.increment_product_views(producto["id"])
        app = MDApp.get_running_app()
        detalle = app.sm.get_screen("detalle_producto")
        detalle.producto = producto
        detalle.clear_widgets()
        detalle.build_ui()
        app.change_screen("detalle_producto")


    def navigate_to_screen(self, screen_name):
        if screen_name == "productos":
            return
        MDApp.get_running_app().change_screen(screen_name)

