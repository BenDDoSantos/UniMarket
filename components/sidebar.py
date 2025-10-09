from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp


class Sidebar(MDNavigationDrawer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Configuración para que el sidebar se superponga
        self.type = "standard"
        self.anchor = "left"
        self.state = "close"
        self.build_ui()
    
    def build_ui(self):
        # Header del sidebar
        header = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(150),
            padding=dp(20),
            spacing=dp(10),
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
        
        self.add_widget(header)
        
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
            {"icon": "cog", "text": "Configuración", "screen": None},
            {"icon": "help-circle", "text": "Ayuda", "screen": None},
            {"icon": "logout", "text": "Cerrar Sesión", "screen": "login"},
        ]
        
        for opcion in opciones:
            item = OneLineAvatarIconListItem(
                text=opcion['text'],
                on_release=lambda x, opcion=opcion: self.handle_menu_option(opcion)
            )
            item.add_widget(IconLeftWidget(icon=opcion['icon']))
            menu_list.add_widget(item)
        
        self.add_widget(menu_list)
    
    def handle_menu_option(self, opcion):
        """Manejar selección de opción del menú"""
        if opcion['screen']:
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            app.change_screen(opcion['screen'])
            # Cerrar el sidebar después de navegar
            self.set_state("close")
        else:
            print(f"Opción '{opcion['text']}' no implementada aún")
