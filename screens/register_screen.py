from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from data_manager import data_manager


class RegisterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        main_layout.add_widget(MDLabel(size_hint_y=0.1))

        # Título
        title = MDLabel(
            text="Registro",
            font_style="H3",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=0.15
        )
        main_layout.add_widget(title)

        subtitle = MDLabel(
            text="Crea tu cuenta en UniMarket",
            font_style="Body1",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=0.1
        )
        main_layout.add_widget(subtitle)

        # Espaciador
        main_layout.add_widget(MDLabel(size_hint_y=0.05))

        # Campo de email
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
        main_layout.add_widget(self.password_field)

        # Campo de confirmar contraseña
        self.confirm_password_field = MDTextField(
            hint_text="Confirmar contraseña",
            icon_right="eye-off",
            password=True,
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            mode="rectangle"
        )
        main_layout.add_widget(self.confirm_password_field)

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

        # Botón de registro
        register_btn = MDRaisedButton(
            text="REGISTRARSE",
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            on_release=self.do_register
        )
        main_layout.add_widget(register_btn)

        # Botón de volver al login
        back_btn = MDFlatButton(
            text="¿Ya tienes cuenta? Inicia sesión",
            size_hint=(0.9, None),
            height=dp(50),
            pos_hint={"center_x": 0.5},
            on_release=self.go_to_login
        )
        main_layout.add_widget(back_btn)

        # Espaciador inferior
        main_layout.add_widget(MDLabel(size_hint_y=0.1))

        self.add_widget(main_layout)

    def do_register(self, instance):
        """Realizar registro y guardar usuario"""
        email = self.email_field.text.strip()
        password = self.password_field.text
        confirm_password = self.confirm_password_field.text

        # Validar que el correo termine en @alu.uct.cl o @uct.cl
        if not (email.endswith("@alu.uct.cl") or email.endswith("@uct.cl")):
            self.error_label.text = "Correo no válido. Use un correo @alu.uct.cl o @uct.cl"
            return

        if password != confirm_password:
            self.error_label.text = "Las contraseñas no coinciden"
            return

        if len(password) < 6:
            self.error_label.text = "La contraseña debe tener al menos 6 caracteres"
            return

        # Intentar registrar usuario
        if data_manager.register_user(email, password, email.split('@')[0]):
            self.error_label.text = "Registro exitoso. Ahora inicia sesión."
            # Limpiar campos
            self.email_field.text = ""
            self.password_field.text = ""
            self.confirm_password_field.text = ""
        else:
            self.error_label.text = "El usuario ya existe"

    def go_to_login(self, instance):
        """Volver a la pantalla de login"""
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.change_screen('login')
