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


class CategoriaCard(MDCard):
    def __init__(self, categoria, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(160), dp(120))
        self.padding = dp(15)
        self.spacing = dp(10)
        self.elevation = 2
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
        
        # Datos de ejemplo de categorías
        categorias = [
            {"nombre": "Libros", "icono": "📚", "cantidad": 45, "color": (0.8, 0.9, 1, 1)},
            {"nombre": "Electrónica", "icono": "💻", "cantidad": 32, "color": (1, 0.9, 0.8, 1)},
            {"nombre": "Útiles", "icono": "✏️", "cantidad": 28, "color": (0.9, 1, 0.8, 1)},
            {"nombre": "Ropa", "icono": "👕", "cantidad": 18, "color": (1, 0.8, 0.9, 1)},
            {"nombre": "Deportes", "icono": "⚽", "cantidad": 15, "color": (0.8, 1, 0.9, 1)},
            {"nombre": "Instrumentos", "icono": "🎸", "cantidad": 12, "color": (0.95, 0.85, 1, 1)},
            {"nombre": "Muebles", "icono": "🪑", "cantidad": 8, "color": (1, 0.95, 0.8, 1)},
            {"nombre": "Otros", "icono": "📦", "cantidad": 25, "color": (0.9, 0.9, 0.9, 1)},
        ]
        
        # Agregar tarjetas de categorías
        for categoria in categorias:
            categories_grid.add_widget(CategoriaCard(categoria))
        
        scroll.add_widget(categories_grid)
        main_layout.add_widget(scroll)
        
        # Bottom bar (custom): three buttons left/center/right
        bottom_bar = MDBoxLayout(size_hint_y=None, height=dp(56), padding=(dp(6), 0, dp(6), 0), spacing=dp(10))

        # Left - Productos
        left_anchor = AnchorLayout(anchor_x='left', anchor_y='center')
        left_box = MDBoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(80), dp(56)), spacing=0)
        left_btn = MDIconButton(icon='shopping', on_release=lambda x: self.goto_productos())
        left_label = MDLabel(text='Productos', halign='center', font_style='Caption')
        left_box.add_widget(left_btn)
        left_box.add_widget(left_label)
        left_anchor.add_widget(left_box)

        # Center - Categorias
        center_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        center_box = MDBoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(80), dp(56)), spacing=0)
        center_btn = MDIconButton(icon='format-list-bulleted', on_release=lambda x: self.goto_categorias())
        center_label = MDLabel(text='Categor\u00edas', halign='center', font_style='Caption')
        center_box.add_widget(center_btn)
        center_box.add_widget(center_label)
        center_anchor.add_widget(center_box)

        # Right - Mis Productos
        right_anchor = AnchorLayout(anchor_x='right', anchor_y='center')
        right_box = MDBoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(100), dp(56)), spacing=0)
        right_btn = MDIconButton(icon='briefcase', on_release=lambda x: self.goto_mis_productos())
        right_label = MDLabel(text='Mis Productos', halign='center', font_style='Caption')
        right_box.add_widget(right_btn)
        right_box.add_widget(right_label)
        right_anchor.add_widget(right_box)

        bottom_bar.add_widget(left_anchor)
        bottom_bar.add_widget(center_anchor)
        bottom_bar.add_widget(right_anchor)

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

