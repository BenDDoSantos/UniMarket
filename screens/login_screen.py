from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from data_manager import data_manager


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('login_data.json')
        self.build_ui()
    
    def build_ui(self):
        # Layout principal
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(20),
            md_bg_color=(1, 1, 1, 1)
        )
        
        # Espaciador superior
        main_layout.add_widget(MDLabel(size_hint_y=0.2))
        
        # Logo o título
        title = MDLabel(
            text="UniMarket",
            font_style="H3",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=0.15
        )
        main_layout.add_widget(title)
        
        subtitle = MDLabel(
            text="Marketplace Universitario",
            font_style="Body1",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=0.1
        )
        main_layout.add_widget(subtitle)
        
        # Espaciador
        main_layout.add_widget(MDLabel(size_hint_y=0.1))
        
        # Campo de usuario/email
        self.email_field = MDTextField(
            hint_text="Correo universitario",
            icon_right="email",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            mode="rectangle"
        )
        main_layout.add_widget(self.email_field)
        
        # Campo de contraseña
        self.password_field = MDTextField(
            hint_text="Contraseña",
            icon_right="eye-off",
            password=True,
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            mode="rectangle"
        )
        self.password_field.bind(on_touch_down=self.toggle_password_visibility)
        main_layout.add_widget(self.password_field)

        # Etiqueta de error
        self.error_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Error",
            size_hint_y=0.05
        )
        main_layout.add_widget(self.error_label)

        # Espaciador
        main_layout.add_widget(MDLabel(size_hint_y=0.05))
        
        # Botón de login
        login_btn = MDRaisedButton(
            text="INICIAR SESIÓN",
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            on_release=self.do_login
        )
        main_layout.add_widget(login_btn)
        
        # Botón de registro
        register_btn = MDRaisedButton(
            text="REGISTRARSE",
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.7, 0.7, 0.7, 1),
            on_release=self.go_to_register
        )
        main_layout.add_widget(register_btn)
        
        # Espaciador inferior
        main_layout.add_widget(MDLabel(size_hint_y=0.2))
        
        self.add_widget(main_layout)

    def on_enter(self):
        """Cargar el último correo usado al entrar a la pantalla"""
        if self.store.exists('last_email'):
            self.email_field.text = self.store.get('last_email')['email']

    def do_login(self, instance):
        """Realizar login y cambiar a pantalla de productos"""
        email = self.email_field.text.strip()
        password = self.password_field.text.strip()

        # Validar que los campos no estén vacíos
        if not email or not password:
            self.error_label.text = "Completa los campos"
            return

        # Validar que el correo termine en @alu.uct.cl o @uct.cl
        if not (email.endswith("@alu.uct.cl") or email.endswith("@uct.cl")):
            self.error_label.text = "Correo no válido. Utilice correo @alu.uct.cl o @uct.cl"
            return

        # Autenticar contra usuarios guardados
        user = data_manager.authenticate_user(email, password)
        if user:
            data_manager.current_user = user
            # Guardar el correo para recordar en futuras sesiones
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
        # Solo activar si se toca el área del ícono (últimos 48dp desde la derecha)
        if touch.x > instance.x + instance.width - dp(48):
            if self.password_field.password:
                self.password_field.password = False
                self.password_field.icon_right = "eye"
            else:
                self.password_field.password = True
                self.password_field.icon_right = "eye-off"

