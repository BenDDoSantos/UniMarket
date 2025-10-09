from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from kivy.uix.anchorlayout import AnchorLayout


class MisProductosScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        # Layout principal
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Toolbar superior
        toolbar = MDTopAppBar(
            title="Mis Productos",
            left_action_items=[["menu", lambda x: self.toggle_nav_drawer()]],
            right_action_items=[["dots-vertical", lambda x: self.show_options()]]
        )
        main_layout.add_widget(toolbar)
        
        # Contenedor para lista y botón flotante
        content_layout = MDBoxLayout(orientation='vertical')
        
        # Scroll para la lista de productos
        scroll = MDScrollView()
        
        # Lista de mis productos
        products_list = MDList()
        
        # Datos de ejemplo de productos del usuario
        mis_productos = [
            {"nombre": "Calculadora Científica", "estado": "Activo", "precio": "$15.000"},
            {"nombre": "Libro de Cálculo I", "estado": "Vendido", "precio": "$25.000"},
            {"nombre": "Mouse Inalámbrico", "estado": "Activo", "precio": "$12.000"},
            {"nombre": "Cuadernos", "estado": "Activo", "precio": "$3.000"},
        ]
        
        for producto in mis_productos:
            item = TwoLineAvatarIconListItem(
                text=producto['nombre'],
                secondary_text=f"{producto['estado']} - {producto['precio']}",
            )
            
            # Ícono a la izquierda
            item.add_widget(IconLeftWidget(icon="package-variant"))
            
            # Ícono de editar a la derecha
            item.add_widget(IconRightWidget(icon="pencil"))
            
            products_list.add_widget(item)
        
        scroll.add_widget(products_list)
        content_layout.add_widget(scroll)
        
        # Botón flotante para agregar producto
        fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": 0.9, "center_y": 0.1},
            on_release=self.add_producto
        )
        content_layout.add_widget(fab)
        
        main_layout.add_widget(content_layout)
        
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
    
    def show_options(self):
        """Mostrar opciones"""
        pass
    
    def add_producto(self, instance):
        """Agregar nuevo producto"""
        print("Agregar nuevo producto")
    
    def goto_productos(self):
        """Ir a productos"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.change_screen('productos')
    
    def goto_mis_productos(self):
        """Ya estamos en mis productos"""
        pass
    
    def goto_categorias(self):
        """Ir a categorías"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.change_screen('categorias')

