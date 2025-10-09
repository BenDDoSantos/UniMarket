from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDIconButton
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout


class ProductCard(MDCard):
    def __init__(self, producto, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(160), dp(220))
        self.padding = dp(10)
        self.spacing = dp(5)
        self.elevation = 2
        self.radius = [dp(10)]
        
        # Imagen del producto (placeholder)
        img = Image(
            source='',  # Aquí iría la imagen del producto
            size_hint_y=0.6,
            allow_stretch=True
        )
        self.add_widget(img)
        
        # Nombre del producto
        nombre = MDLabel(
            text=producto['nombre'],
            font_style="Body2",
            size_hint_y=0.2,
            halign="left"
        )
        self.add_widget(nombre)
        
        # Precio
        precio = MDLabel(
            text=f"${producto['precio']}",
            font_style="H6",
            theme_text_color="Primary",
            size_hint_y=0.2,
            halign="left"
        )
        self.add_widget(precio)


class ProductosScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        # Layout principal
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Toolbar superior
        toolbar = MDTopAppBar(
            title="Productos",
            left_action_items=[["menu", lambda x: self.toggle_nav_drawer()]],
            right_action_items=[["magnify", lambda x: self.search()]]
        )
        main_layout.add_widget(toolbar)
        
        # Scroll para los productos
        scroll = MDScrollView()
        
        # Grid de productos
        products_grid = MDGridLayout(
            cols=2,
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None,
            adaptive_height=True
        )
        
        # Datos de ejemplo
        productos_ejemplo = [
            {"nombre": "Calculadora Científica", "precio": 15000},
            {"nombre": "Libro de Cálculo", "precio": 25000},
            {"nombre": "Laptop HP", "precio": 450000},
            {"nombre": "Mouse Inalámbrico", "precio": 12000},
            {"nombre": "Cuaderno Universitario", "precio": 3000},
            {"nombre": "Mochila", "precio": 35000},
            {"nombre": "Auriculares", "precio": 28000},
            {"nombre": "Tablet Samsung", "precio": 180000},
        ]
        
        # Agregar tarjetas de productos
        for producto in productos_ejemplo:
            products_grid.add_widget(ProductCard(producto))
        
        scroll.add_widget(products_grid)
        main_layout.add_widget(scroll)
        
        # Bottom bar (custom): three buttons left/center/right
        from kivymd.uix.button import MDIconButton
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
        """Ya estamos en productos"""
        pass
    
    def goto_mis_productos(self):
        """Ir a mis productos"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.change_screen('mis_productos')
    
    def goto_categorias(self):
        """Ir a categorías"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.change_screen('categorias')

