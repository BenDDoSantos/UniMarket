from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from data_manager import data_manager
import os


AZUL_UCT = (0 / 255, 94 / 255, 184 / 255, 1)  # #005EB8


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('login_data.json')
        self.build_ui()
    
    def build_ui(self):
        # Ruta del logo
        logo_path = os.path.join(os.getcwd(), "assets", "images", "uct_logo.png")
        print("WORKING DIR (LOGIN):", os.getcwd())
        print("UCT LOGO EXISTS (LOGIN)?", os.path.exists(logo_path))

        # Layout raíz
        root_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(1, 1, 1, 1)
        )

        # Espacio superior
        root_layout.add_widget(MDLabel(size_hint_y=0.05))

        # Logo institucional
        logo = Image(
            source=logo_path,
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            pos_hint={"center_x": 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        root_layout.add_widget(logo)

        # Pequeño espacio después del logo
        root_layout.add_widget(MDLabel(size_hint_y=0.02))

        # Tarjeta central
        card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(18),
            size_hint=(0.9, None),
            height=dp(420),
            pos_hint={"center_x": 0.5},
            elevation=1,
            radius=[20, 20, 20, 20],
        )

        card_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12)
        )

        # Título
        title = MDLabel(
            text="UniMarket",
            font_style="H4",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(40),
        )
        card_layout.add_widget(title)

        # Subtítulo
        subtitle = MDLabel(
            text="Marketplace Universitario",
            font_style="Body1",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20),
        )
        card_layout.add_widget(subtitle)

        # Espacio antes de inputs
        card_layout.add_widget(MDLabel(size_hint_y=None, height=dp(10)))

        # Campo de email
        self.email_field = MDTextField(
            hint_text="Correo universitario",
            icon_right="email",
            size_hint_x=1,
            mode="rectangle"
        )
        card_layout.add_widget(self.email_field)

        # Campo de contraseña
        self.password_field = MDTextField(
            hint_text="Contraseña",
            icon_right="eye-off",
            password=True,
            size_hint_x=1,
            mode="rectangle"
        )
        self.password_field.bind(on_touch_down=self.toggle_password_visibility)
        card_layout.add_widget(self.password_field)

        # Etiqueta de error
        self.error_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Error",
            size_hint_y=None,
            height=dp(20),
        )
        card_layout.add_widget(self.error_label)

        # Espacio antes de botones
        card_layout.add_widget(MDLabel(size_hint_y=None, height=dp(10)))

        # Botón de login (principal)
        login_btn = MDRaisedButton(
            text="INICIAR SESIÓN",
            size_hint=(1, None),
            height=dp(48),
            md_bg_color=AZUL_UCT,
            on_release=self.do_login
        )
        card_layout.add_widget(login_btn)

        # Botón de registro (secundario)
        register_btn = MDFlatButton(
            text="Crear cuenta en UniMarket",
            size_hint=(1, None),
            height=dp(40),
            text_color=AZUL_UCT,
            on_release=self.go_to_register
        )
        card_layout.add_widget(register_btn)

        card.add_widget(card_layout)
        root_layout.add_widget(card)

        # Espacio inferior
        root_layout.add_widget(MDLabel(size_hint_y=0.1))

        self.add_widget(root_layout)

    def on_enter(self):
        """Cargar el último correo usado al entrar a la pantalla"""
        if self.store.exists('last_email'):
            self.email_field.text = self.store.get('last_email')['email']

    def do_login(self, instance):
        """Realizar login y cambiar a pantalla de productos"""
        email = self.email_field.text.strip()
        password = self.password_field.text.strip()

        if not email or not password:
            self.error_label.text = "Completa los campos"
            return

        if not (email.endswith("@alu.uct.cl") or email.endswith("@uct.cl")):
            self.error_label.text = "Correo no válido. Utilice correo @alu.uct.cl o @uct.cl"
            return

        user = data_manager.authenticate_user(email, password)
        if user:
            data_manager.current_user = user
            data_manager.save_current_user()
            self.store.put('last_email', email=email)
            self.error_label.text = ""
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            app.change_screen('productos')
        else:
            self.error_label.text = "Credenciales incorrectas"

    def go_to_register(self, instance):
        """Ir a la pantalla de registro"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.change_screen('register')

    def toggle_password_visibility(self, instance, touch):
        """Alternar la visibilidad de la contraseña"""
        if touch.x > instance.x + instance.width - dp(48):
            self.password_field.password = not self.password_field.password
            self.password_field.icon_right = "eye" if not self.password_field.password else "eye-off"

