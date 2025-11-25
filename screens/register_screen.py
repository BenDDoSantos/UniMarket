from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivy.uix.image import Image
from kivymd.toast import toast
from kivymd.app import MDApp
from data_manager import data_manager

AZUL_UCT = (0 / 255, 94 / 255, 184 / 255, 1)

class RegisterScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()

        # ROOT GENERAL
        root = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10),
            md_bg_color=(1, 1, 1, 1)
        )
        self.add_widget(root)

        # ----- ESPACIO SUPERIOR -----
        root.add_widget(MDLabel(size_hint_y=0.03))

        # ----- LOGO (reubicado) -----
        logo_container = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(130),
            padding=(0, dp(10), 0, dp(10))
        )
        logo = Image(
            source="assets/images/uct_logo.png",
            size_hint=(None, None),
            size=(dp(110), dp(110)),
            pos_hint={"center_x": 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        logo_container.add_widget(logo)
        root.add_widget(logo_container)

        # ----- MDCard (ajustado) -----
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint=(0.9, None),
            height=dp(390),
            pos_hint={"center_x": 0.5, "center_y": 0.45},
            elevation=1,
            radius=[16, 16, 16, 16]
        )

        card_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10)
        )

        # ----- TÍTULO -----
        title = MDLabel(
            text="Registro",
            font_style="H5",
            halign="center",
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(32),
        )
        card_layout.add_widget(title)

        # ----- SUBTÍTULO -----
        subtitle = MDLabel(
            text="Crea tu cuenta en UniMarket",
            font_style="Body2",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(18),
        )
        card_layout.add_widget(subtitle)

        # ----- Inputs (compactos) -----
        self.nombre_input = MDTextField(
            hint_text="Nombre completo",
            icon_right="account",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(40),
        )
        card_layout.add_widget(self.nombre_input)

        self.email_input = MDTextField(
            hint_text="Correo universitario (@alu.uct.cl)",
            icon_right="email",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(40),
        )
        card_layout.add_widget(self.email_input)

        self.password_input = MDTextField(
            hint_text="Contraseña",
            icon_right="eye-off",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(40),
            password=True
        )
        self.password_input.bind(on_touch_down=self.toggle_password)
        card_layout.add_widget(self.password_input)

        self.confirm_password_input = MDTextField(
            hint_text="Confirmar contraseña",
            icon_right="eye-off",
            mode="rectangle",
            size_hint=(1, None),
            height=dp(40),
            password=True
        )
        self.confirm_password_input.bind(on_touch_down=self.toggle_confirm_password)
        card_layout.add_widget(self.confirm_password_input)

        # ----- BOTÓN REGISTRARSE -----
        register_btn = MDRaisedButton(
            text="REGISTRARSE",
            size_hint=(1, None),
            height=dp(44),
            md_bg_color=AZUL_UCT,
            on_release=self.register_user
        )
        card_layout.add_widget(register_btn)

        card.add_widget(card_layout)
        root.add_widget(card)

        # ----- ENLACE INICIAR SESIÓN -----
        login_btn = MDFlatButton(
            text="¿Ya tienes cuenta? Inicia sesión",
            size_hint=(1, None),
            height=dp(40),
            text_color=AZUL_UCT,
            on_release=lambda x: MDApp.get_running_app().change_screen("login"),
        )
        root.add_widget(login_btn)

        # Espacio final inferior
        root.add_widget(MDLabel(size_hint_y=0.05))

    # ----- LÓGICA -----
    def toggle_password(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # Detectar si tocó el área del icono derecho (último 10% del ancho)
            if touch.x > instance.right - dp(40):
                instance.password = not instance.password
                instance.icon_right = "eye" if instance.password else "eye-off"
                return True
        return False

    def toggle_confirm_password(self, instance, touch):
        if instance.collide_point(*touch.pos):
            # Detectar si tocó el área del icono derecho (último 10% del ancho)
            if touch.x > instance.right - dp(40):
                instance.password = not instance.password
                instance.icon_right = "eye" if instance.password else "eye-off"
                return True
        return False

    def register_user(self, instance):
        nombre = self.nombre_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        confirm = self.confirm_password_input.text.strip()

        if not nombre or not email or not password or not confirm:
            toast("Completa todos los campos")
            return

        if " " not in nombre:
            toast("Escribe nombre y apellido")
            return

        if not email.endswith("@alu.uct.cl"):
            toast("Usa tu correo institucional @alu.uct.cl")
            return

        if password != confirm:
            toast("Las contraseñas no coinciden")
            return

        if data_manager.register_user(email, password, nombre):
            toast("Registro exitoso. Inicia sesión.")
            MDApp.get_running_app().change_screen("login")
        else:
            toast("El usuario ya existe")













