from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.button import MDIconButton
from data_manager import data_manager


class CategoriaCard(MDCard):
    def __init__(self, categoria, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(160), dp(120))
        self.padding = dp(15)
        self.spacing = dp(10)
        self.elevation = 1
        self.radius = [dp(10)]
        self.md_bg_color = categoria.get('color', (0.9, 0.9, 0.9, 1))
        
        # Ícono de la categoría
        icon_label = MDLabel(
            text=categoria['icono'],
            font_style="H4",
            halign="center",
            size_hint_y=0.5
        )
        self.add_widget(icon_label)
        
        # Nombre de la categoría
        nombre = MDLabel(
            text=categoria['nombre'],
            font_style="Body1",
            halign="center",
            size_hint_y=0.3
        )
        self.add_widget(nombre)
        
        # Cantidad de productos
        cantidad = MDLabel(
            text=f"{categoria['cantidad']} productos",
            font_style="Caption",
            theme_text_color="Secondary",
            halign="center",
            size_hint_y=0.2
        )
        self.add_widget(cantidad)


class CategoriasScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        # Layout principal
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Toolbar superior
        toolbar = MDTopAppBar(
            title="Categorías",
            left_action_items=[["menu", lambda x: self.toggle_nav_drawer()]],
            right_action_items=[["magnify", lambda x: self.search()]]
        )
        main_layout.add_widget(toolbar)
        
        # Scroll para las categorías
        scroll = MDScrollView()
        
        # Grid de categorías
        categories_grid = MDGridLayout(
            cols=2,
            spacing=dp(15),
            padding=dp(15),
            size_hint_y=None,
            adaptive_height=True
        )
        
        # Cargar categorías desde data_manager
        categorias = data_manager.get_categories()
        
        # Agregar tarjetas de categorías
        for categoria in categorias:
            categories_grid.add_widget(CategoriaCard(categoria))
        
        scroll.add_widget(categories_grid)
        main_layout.add_widget(scroll)
        
        # Custom Bottom Bar
        from components.custom_bottom_bar import CustomBottomBar
        bottom_bar = CustomBottomBar(
            current_screen="categorias",
            navigation_callback=self.navigate_to_screen
        )
        main_layout.add_widget(bottom_bar)
        
        self.add_widget(main_layout)
    
    def toggle_nav_drawer(self):
        """Abrir/cerrar el sidebar"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.toggle_nav_drawer()
    
    def search(self):
        """Abrir búsqueda"""
        pass
    
    def navigate_to_screen(self, screen_name):
        if screen_name == "categorias":
            pass  # Already on this screen
        else:
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            app.change_screen(screen_name)

    def goto_productos(self):
        """Ir a productos"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.change_screen('productos')

    def goto_mis_productos(self):
        """Ir a mis productos"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.change_screen('mis_productos')

    def goto_categorias(self):
        """Ya estamos en categorías"""
        pass

