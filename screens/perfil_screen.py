from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.metrics import dp


class PerfilScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        # Layout principal
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Toolbar superior
        toolbar = MDTopAppBar(
            title="Mi Perfil",
            left_action_items=[["menu", lambda x: self.toggle_nav_drawer()]],
            right_action_items=[["cog", lambda x: self.show_settings()]]
        )
        main_layout.add_widget(toolbar)
        
        # Scroll para el contenido
        scroll = MDScrollView()
        
        # Layout del contenido
        content_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(20),
            size_hint_y=None,
            adaptive_height=True
        )
        
        # Card de información del usuario
        user_card = MDCard(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(15),
            size_hint_y=None,
            height=dp(200),
            elevation=1,
            radius=[dp(10)]
        )
        
        # Avatar del usuario
        avatar_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=0.4
        )
        
        avatar = MDIconButton(
            icon="account-circle",
            icon_size=dp(80),
            theme_icon_color="Primary",
            size_hint=(None, None),
            size=(dp(80), dp(80))
        )
        avatar_layout.add_widget(avatar)
        
        # Información del usuario
        user_info = MDBoxLayout(
            orientation='vertical',
            spacing=dp(5)
        )
        
        name_label = MDLabel(
            text="Juan Pérez",
            font_style="H5",
            theme_text_color="Primary"
        )
        user_info.add_widget(name_label)
        
        email_label = MDLabel(
            text="juan.perez@alu.uct.cl",
            font_style="Body2",
            theme_text_color="Secondary"
        )
        user_info.add_widget(email_label)
        
        carrera_label = MDLabel(
            text="Ingeniería en Sistemas",
            font_style="Body2",
            theme_text_color="Secondary"
        )
        user_info.add_widget(carrera_label)
        
        avatar_layout.add_widget(user_info)
        user_card.add_widget(avatar_layout)
        
        # Estadísticas del usuario
        stats_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(20),
            size_hint_y=0.3
        )
        
        # Productos vendidos
        vendidos_card = MDCard(
            orientation='vertical',
            padding=dp(10),
            size_hint_x=0.3,
            elevation=0,
            radius=[dp(8)]
        )
        vendidos_label = MDLabel(
            text="12",
            font_style="H4",
            halign="center",
            theme_text_color="Primary"
        )
        vendidos_card.add_widget(vendidos_label)
        vendidos_text = MDLabel(
            text="Vendidos",
            font_style="Caption",
            halign="center",
            theme_text_color="Secondary"
        )
        vendidos_card.add_widget(vendidos_text)
        stats_layout.add_widget(vendidos_card)

        # Productos activos
        activos_card = MDCard(
            orientation='vertical',
            padding=dp(10),
            size_hint_x=0.3,
            elevation=0,
            radius=[dp(8)]
        )
        activos_label = MDLabel(
            text="5",
            font_style="H4",
            halign="center",
            theme_text_color="Primary"
        )
        activos_card.add_widget(activos_label)
        activos_text = MDLabel(
            text="Activos",
            font_style="Caption",
            halign="center",
            theme_text_color="Secondary"
        )
        activos_card.add_widget(activos_text)
        stats_layout.add_widget(activos_card)

        # Calificación
        rating_card = MDCard(
            orientation='vertical',
            padding=dp(10),
            size_hint_x=0.3,
            elevation=0,
            radius=[dp(8)]
        )
        rating_label = MDLabel(
            text="4.8",
            font_style="H4",
            halign="center",
            theme_text_color="Primary"
        )
        rating_card.add_widget(rating_label)
        rating_text = MDLabel(
            text="⭐ Rating",
            font_style="Caption",
            halign="center",
            theme_text_color="Secondary"
        )
        rating_card.add_widget(rating_text)
        stats_layout.add_widget(rating_card)
        
        user_card.add_widget(stats_layout)
        content_layout.add_widget(user_card)
        
        # Lista de opciones del perfil
        options_list = MDList()
        
        # Opciones del perfil
        opciones = [
            {"icon": "pencil", "text": "Editar Perfil"},
            {"icon": "history", "text": "Historial de Compras"},
            {"icon": "heart", "text": "Favoritos"},
            {"icon": "message", "text": "Mensajes"},
            {"icon": "cog", "text": "Configuración"},
            {"icon": "help-circle", "text": "Ayuda"},
            {"icon": "logout", "text": "Cerrar Sesión"},
        ]
        
        for opcion in opciones:
            item = OneLineAvatarIconListItem(
                text=opcion['text'],
                on_release=lambda x, opcion=opcion: self.handle_option(opcion)
            )
            item.add_widget(IconLeftWidget(icon=opcion['icon']))
            options_list.add_widget(item)
        
        content_layout.add_widget(options_list)
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def toggle_nav_drawer(self):
        """Abrir/cerrar el sidebar"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.toggle_nav_drawer()
    
    def show_settings(self):
        """Mostrar configuración"""
        pass
    
    def handle_option(self, opcion):
        """Manejar selección de opción"""
        print(f"Opción seleccionada: {opcion['text']}")
        if opcion['text'] == "Cerrar Sesión":
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            app.change_screen('login')
