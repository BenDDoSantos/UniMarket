from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp


class SidebarModal(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.85, 1)  # 85% del ancho de la pantalla
        self.pos_hint = {'x': 0, 'top': 1}  # Completamente pegado a la izquierda
        self.auto_dismiss = True  # Se cierra al tocar fuera
        self.background_color = (0, 0, 0, 0.3)  # Fondo semi-transparente
        # Eliminar padding por defecto del ModalView
        self.padding = [0, 0, 0, 0]
        self.build_ui()
    
    def build_ui(self):
        # Usar FloatLayout para control total de posición
        main_container = FloatLayout()
        
        # Layout principal del sidebar
        sidebar_layout = MDBoxLayout(
            orientation='vertical',
            size_hint=(0.85, 1),
            pos_hint={'x': 0, 'top': 1},
            md_bg_color=(0.2, 0.4, 0.8, 1),  # Fondo azul del sidebar
            padding=[0, 0, 0, 0]  # Sin padding
        )
        
        # Header del sidebar
        header = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),
            padding=dp(25),
            spacing=dp(15),
            md_bg_color=(0.2, 0.4, 0.8, 1)
        )
        
        # Avatar del usuario (usando un botón con ícono)
        avatar = MDIconButton(
            icon="account-circle",
            icon_size=dp(60),
            theme_icon_color="Custom",
            icon_color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(60), dp(60))
        )
        header.add_widget(avatar)
        
        # Nombre del usuario
        name_label = MDLabel(
            text="Juan Pérez",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="center"
        )
        header.add_widget(name_label)
        
        # Email del usuario
        email_label = MDLabel(
            text="juan.perez@alu.uct.cl",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0.9, 0.9, 0.9, 1),
            halign="center"
        )
        header.add_widget(email_label)
        
        sidebar_layout.add_widget(header)
        
        # Scroll view para el contenido del menú
        scroll_view = MDScrollView()
        
        # Lista de opciones del menú
        menu_list = MDList()
        
        # Opciones del menú
        opciones = [
            {"icon": "account", "text": "Mi Perfil", "screen": "perfil"},
            {"icon": "shopping", "text": "Productos", "screen": "productos"},
            {"icon": "briefcase", "text": "Mis Productos", "screen": "mis_productos"},
            {"icon": "format-list-bulleted", "text": "Categorías", "screen": "categorias"},
            {"icon": "heart", "text": "Favoritos", "screen": None},
            {"icon": "message", "text": "Mensajes", "screen": None},
            {"icon": "history", "text": "Historial", "screen": None},
            {"icon": "bell", "text": "Notificaciones", "screen": None},
            {"icon": "star", "text": "Reseñas", "screen": None},
            {"icon": "chart-line", "text": "Estadísticas", "screen": None},
            {"icon": "shield", "text": "Seguridad", "screen": None},
            {"icon": "cog", "text": "Configuración", "screen": None},
            {"icon": "help-circle", "text": "Ayuda", "screen": None},
            {"icon": "information", "text": "Acerca de", "screen": None},
            {"icon": "logout", "text": "Cerrar Sesión", "screen": "login"},
        ]
        
        for opcion in opciones:
            item = OneLineAvatarIconListItem(
                text=opcion['text'],
                on_release=lambda x, opcion=opcion: self.handle_menu_option(opcion)
            )
            item.add_widget(IconLeftWidget(icon=opcion['icon']))
            menu_list.add_widget(item)
        
        # Agregar la lista al scroll view
        scroll_view.add_widget(menu_list)
        
        # Agregar el scroll view al layout principal
        sidebar_layout.add_widget(scroll_view)
        
        # Agregar el sidebar al contenedor principal
        main_container.add_widget(sidebar_layout)
        
        # Agregar el contenedor al modal
        self.add_widget(main_container)
    
    def handle_menu_option(self, opcion):
        """Manejar selección de opción del menú"""
        if opcion['screen']:
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            if opcion['screen'] == 'login':
                # Cerrar sesión antes de ir a login
                app.logout()
            app.change_screen(opcion['screen'])
            # Cerrar el sidebar después de navegar
            self.dismiss()
        else:
            print(f"Opción '{opcion['text']}' no implementada aún")
            self.dismiss()
