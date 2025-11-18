from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.app import MDApp
from data_manager import data_manager


class ProductCard(MDCard):
    def __init__(self, producto, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(160), dp(220))
        self.padding = dp(10)
        self.spacing = dp(5)
        self.elevation = 1
        self.radius = [dp(10)]

        # Imagen del producto o placeholder
        if producto.get("imagen") and producto["imagen"]:
            img = Image(source=producto["imagen"], size_hint_y=0.6, allow_stretch=True, keep_ratio=False)
        else:
            img = Image(source="", size_hint_y=0.6, allow_stretch=True, keep_ratio=False)
        self.add_widget(img)

        # Nombre
        nombre = MDLabel(
            text=producto["nombre"],
            font_style="Body2",
            halign="left",
            size_hint_y=0.2
        )
        self.add_widget(nombre)

        # Precio
        precio = MDLabel(
            text=f"${producto['precio']}",
            font_style="H6",
            theme_text_color="Primary",
            halign="left",
            size_hint_y=0.2
        )
        self.add_widget(precio)


class ProductosScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_category = None  # Para filtrar por categoría
        self.build_ui()

    def build_ui(self):
        # Layout principal
        main_layout = MDBoxLayout(orientation="vertical")

        # === NAVBAR SUPERIOR ===
        title_text = f"Productos{f' - {self.selected_category}' if self.selected_category else ''}"
        toolbar = MDTopAppBar(
            title=title_text,
            elevation=2,
            size_hint_y=None,
            height=dp(56),
            left_action_items=[["menu", lambda x: self.toggle_nav_drawer()]],
            right_action_items=[["magnify", lambda x: self.search()], ["filter-variant", lambda x: self.clear_filter()] if self.selected_category else ["magnify", lambda x: self.search()]],
        )
        main_layout.add_widget(toolbar)

        # === SCROLL DE PRODUCTOS ===
        scroll = MDScrollView(size_hint_y=1)

        products_grid = MDGridLayout(
            cols=2,
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None,
            adaptive_height=True,
        )

        # Cargar productos desde data_manager
        self.productos_ejemplo = data_manager.get_all_products()

        # Filtrar por categoría si está seleccionada
        if self.selected_category:
            productos_filtrados = [p for p in self.productos_ejemplo if p.get("categoria") == self.selected_category]
        else:
            productos_filtrados = self.productos_ejemplo

        for producto in productos_filtrados:
            card = ProductCard(producto)
            card.bind(on_release=lambda x, p=producto: self.ver_detalle(p))
            products_grid.add_widget(card)

        scroll.add_widget(products_grid)
        main_layout.add_widget(scroll)

        # Custom Bottom Bar
        from components.custom_bottom_bar import CustomBottomBar
        bottom_bar = CustomBottomBar(
            current_screen="productos",
            navigation_callback=self.navigate_to_screen
        )
        main_layout.add_widget(bottom_bar)

        # Agregar todo a la pantalla
        self.add_widget(main_layout)

    # ===== FUNCIONES =====

    def toggle_nav_drawer(self):
        MDApp.get_running_app().toggle_nav_drawer()

    def search(self):
        self.search_dialog = MDDialog(
            title="Buscar productos",
            type="custom",
            content_cls=MDTextField(
                hint_text="Buscar por nombre...", on_text_validate=self.filtrar_productos
            ),
            buttons=[
                MDRaisedButton(text="Buscar", on_release=self.filtrar_productos),
                MDRaisedButton(text="Cancelar", on_release=lambda x: self.search_dialog.dismiss()),
            ],
        )
        self.search_dialog.open()

    def navigate_to_screen(self, screen_name):
        if screen_name == "productos":
            pass  # Already on this screen
        else:
            MDApp.get_running_app().change_screen(screen_name)

    def goto_productos(self):
        pass

    def goto_mis_productos(self):
        MDApp.get_running_app().change_screen("mis_productos")

    def goto_categorias(self):
        MDApp.get_running_app().change_screen("categorias")

    def ver_detalle(self, producto):
        data_manager.increment_product_views(producto["id"])
        app = MDApp.get_running_app()
        detalle_screen = app.sm.get_screen("detalle_producto")
        detalle_screen.producto = producto
        detalle_screen.clear_widgets()
        detalle_screen.build_ui()
        app.change_screen("detalle_producto")

    def filtrar_productos(self, instance=None):
        search_text = self.search_dialog.content_cls.text.lower()
        self.search_dialog.dismiss()

        scroll = self.children[0].children[1]
        grid = scroll.children[0]
        grid.clear_widgets()

        # Aplicar filtro de búsqueda sobre los productos ya filtrados por categoría
        if self.selected_category:
            base_productos = [p for p in self.productos_ejemplo if p.get("categoria") == self.selected_category]
        else:
            base_productos = self.productos_ejemplo

        filtrados = [p for p in base_productos if search_text in p["nombre"].lower()]

        for producto in filtrados:
            card = ProductCard(producto)
            card.bind(on_release=lambda x, p=producto: self.ver_detalle(p))
            grid.add_widget(card)

    def clear_filter(self):
        """Limpiar filtro de categoría y mostrar todos los productos"""
        self.selected_category = None
        self.clear_widgets()
        self.build_ui()

    def set_category_filter(self, categoria):
        """Establecer filtro de categoría desde categorías_screen"""
        self.selected_category = categoria
        self.clear_widgets()
        self.build_ui()
