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
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp


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
        self.mis_productos = [
            {"nombre": "Calculadora Científica", "estado": "Activo", "precio": "$15.000", "descripcion": "Calculadora científica con funciones avanzadas", "vistas": 45, "interesados": 3, "vendedor": "Yo", "imagen": ""},
            {"nombre": "Libro de Cálculo I", "estado": "Vendido", "precio": "$25.000", "descripcion": "Libro de cálculo integral usado en primer semestre", "vistas": 78, "interesados": 5, "vendedor": "Yo", "imagen": ""},
            {"nombre": "Mouse Inalámbrico", "estado": "Activo", "precio": "$12.000", "descripcion": "Mouse óptico inalámbrico, batería incluida", "vistas": 23, "interesados": 1, "vendedor": "Yo", "imagen": ""},
            {"nombre": "Cuadernos", "estado": "Activo", "precio": "$3.000", "descripcion": "Paquete de 5 cuadernos universitarios", "vistas": 12, "interesados": 0, "vendedor": "Yo", "imagen": ""},
        ]
        
        for producto in self.mis_productos:
            item = TwoLineAvatarIconListItem(
                text=producto['nombre'],
                secondary_text=f"{producto['estado']} - {producto['precio']}",
                on_release=lambda x, p=producto: self.ver_detalle(p)
            )

            # Ícono a la izquierda
            item.add_widget(IconLeftWidget(icon="package-variant"))

            # Ícono de editar a la derecha
            edit_icon = IconRightWidget(icon="pencil")
            edit_icon.bind(on_release=lambda x, p=producto: self.editar_producto(p))
            item.add_widget(edit_icon)

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
        menu_items = [
            {
                "text": "Actualizar lista",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Actualizar lista": self.menu_callback(x),
            },
            {
                "text": "Ver estadísticas generales",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Ver estadísticas generales": self.menu_callback(x),
            },
            {
                "text": "Cerrar sesión",
                "viewclass": "OneLineListItem",
                "on_release": lambda x="Cerrar sesión": self.menu_callback(x),
            },
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.toolbar.right_action_items[0][1],  # El botón dots-vertical
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()
    
    def add_producto(self, instance):
        """Agregar nuevo producto"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.change_screen('agregar_producto')
    
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

    def ver_detalle(self, producto):
        """Ver detalle del producto"""
        app = MDApp.get_running_app()
        # Actualizar el producto en la pantalla existente
        detalle_screen = app.sm.get_screen('detalle_producto')
        detalle_screen.producto = producto
        detalle_screen.clear_widgets()
        detalle_screen.build_ui()
        app.change_screen('detalle_producto')

    def editar_producto(self, producto):
        """Editar producto"""
        app = MDApp.get_running_app()
        # Actualizar el producto en la pantalla existente
        editar_screen = app.sm.get_screen('editar_producto')
        editar_screen.producto = producto
        editar_screen.clear_widgets()
        editar_screen.build_ui()
        app.change_screen('editar_producto')

    def menu_callback(self, text_item):
        """Callback para opciones del menú"""
        self.menu.dismiss()
        if text_item == "Actualizar lista":
            self.actualizar_lista()
        elif text_item == "Ver estadísticas generales":
            self.ver_estadisticas()
        elif text_item == "Cerrar sesión":
            self.cerrar_sesion()

    def actualizar_lista(self):
        """Actualizar la lista de productos"""
        print("Lista actualizada")
        # Aquí se podría refrescar desde una base de datos

    def ver_estadisticas(self):
        """Mostrar estadísticas generales"""
        activos = len([p for p in self.mis_productos if p['estado'] == 'Activo'])
        vendidos = len([p for p in self.mis_productos if p['estado'] == 'Vendido'])
        total_vistas = sum(p['vistas'] for p in self.mis_productos)
        promedio_vistas = total_vistas / len(self.mis_productos) if self.mis_productos else 0

        dialog = MDDialog(
            title="Estadísticas Generales",
            text=f"Productos activos: {activos}\nProductos vendidos: {vendidos}\nVisualizaciones promedio: {promedio_vistas:.1f}",
            size_hint=(0.8, 0.4),
            buttons=[
                MDRaisedButton(
                    text="Cerrar",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def cerrar_sesion(self):
        """Cerrar sesión"""
        app = MDApp.get_running_app()
        app.change_screen('login')

