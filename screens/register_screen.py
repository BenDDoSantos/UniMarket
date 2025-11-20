from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.metrics import dp
from data_manager import data_manager
import os

AZUL_UCT = (0 / 255, 94 / 255, 184 / 255, 1)


class RegisterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):

        logo_path = os.path.join(os.getcwd(), "assets", "images", "uct_logo.png")

        # Layout raíz
        root = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(1, 1, 1, 1)
        )

        # Espacio superior suave igual a login
        root.add_widget(MDLabel(size_hint_y=0.03))

        # Logo institucional UCT
        logo = Image(
            source=logo_path,
            size_hint=(None, None),
            size=(dp(120), dp(120)),
            pos_hint={"center_x": 0.5},
            allow_stretch=True,
            keep_ratio=True,
        )
        root.add_widget(logo)

        # Espacio pequeño entre logo y card
        root.add_widget(MDLabel(size_hint_y=0.015))

        # ========= MDCard principal =========
        card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            size_hint=(0.9, None),
            height=dp(455),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            elevation=1,
            radius=[20, 20, 20, 20],
        )

        card_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12)
        )

        # 🌟 TÍTULO **DENTRO DEL CARD**
        title = MDLabel(
            text="Registro",
            font_style="H4",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(38),
        )
        card_layout.add_widget(title)

        # 🌟 SUBTÍTULO **DENTRO DEL CARD**
        subtitle = MDLabel(
            text="Crea tu cuenta en UniMarket",
            font_style="Body1",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(20),
        )
        card_layout.add_widget(subtitle)

        # Espacio antes de los campos
        card_layout.add_widget(MDLabel(size_hint_y=None, height=dp(4)))

        # ========= CAMPOS =========

        self.email_field = MDTextField(
            hint_text="Correo universitario",
            icon_right="email",
            size_hint_x=1,
            mode="rectangle",
        )
        card_layout.add_widget(self.email_field)

        self.password_field = MDTextField(
            hint_text="Contraseña",
            icon_right="eye-off",
            password=True,
            size_hint_x=1,
            mode="rectangle",
        )
        card_layout.add_widget(self.password_field)

        self.confirm_password_field = MDTextField(
            hint_text="Confirmar contraseña",
            icon_right="eye-off",
            password=True,
            size_hint_x=1,
            mode="rectangle",
        )
        card_layout.add_widget(self.confirm_password_field)

        # ERROR MESSAGE
        self.error_label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Error",
            size_hint_y=None,
            height=dp(20),
        )
        card_layout.add_widget(self.error_label)

        # ========= BOTÓN REGISTRARSE =========
        register_btn = MDRaisedButton(
            text="REGISTRARSE",
            size_hint=(1, None),
            height=dp(48),
            md_bg_color=AZUL_UCT,
            on_release=self.do_register,
        )
        card_layout.add_widget(register_btn)

        # ========= BOTÓN VOLVER =========
        back_btn = MDFlatButton(
            text="¿Ya tienes cuenta? Inicia sesión",
            size_hint=(1, None),
            height=dp(40),
            text_color=AZUL_UCT,
            on_release=self.go_to_login,
        )
        card_layout.add_widget(back_btn)

        card.add_widget(card_layout)
        root.add_widget(card)

        # Espacio final inferior
        root.add_widget(MDLabel(size_hint_y=0.1))

        self.add_widget(root)

    # ============================
    #        LÓGICA
    # ============================

    def do_register(self, instance):
        email = self.email_field.text.strip()
        password = self.password_field.text
        confirm_password = self.confirm_password_field.text

        if not (email.endswith("@alu.uct.cl") or email.endswith("@uct.cl")):
            self.error_label.text = "Correo no válido. Use un correo @alu.uct.cl o @uct.cl"
            return

        if password != confirm_password:
            self.error_label.text = "Las contraseñas no coinciden"
            return

        if len(password) < 6:
            self.error_label.text = "La contraseña debe tener al menos 6 caracteres"
            return

        if data_manager.register_user(email, password, email.split('@')[0]):
            self.error_label.text = "Registro exitoso. Ahora inicia sesión."
            self.email_field.text = ""
            self.password_field.text = ""
            self.confirm_password_field.text = ""
        else:
            self.error_label.text = "El usuario ya existe"

    def go_to_login(self, instance):
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.change_screen("login")


