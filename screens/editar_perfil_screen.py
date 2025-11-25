from kivymd.uix.screen import MDScreen 
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivymd.uix.scrollview import MDScrollView
from data_manager import data_manager


class EditarPerfilScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    # ================================================================
    # UI PRINCIPAL
    # ================================================================
    def build_ui(self):
        main_layout = MDBoxLayout(
            orientation='vertical',
            md_bg_color=(0.96, 0.96, 0.96, 1)
        )

        # ------------------------------------------------------------
        # BARRA SUPERIOR
        # ------------------------------------------------------------
        toolbar = MDTopAppBar(
            title="Editar Perfil",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=2
        )
        main_layout.add_widget(toolbar)

        # ------------------------------------------------------------
        # SCROLLVIEW
        # ------------------------------------------------------------
        scroll = MDScrollView()
        content = MDBoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(20),
            size_hint_y=None,
            adaptive_height=True
        )

        # ============================================================
        # TITULO
        # ============================================================
        title_card = MDCard(
            orientation='vertical',
            adaptive_height=True,
            padding=dp(18),
            elevation=0,
            radius=[dp(16)],
            md_bg_color=(0.3, 0.5, 0.9, 0.15)
        )

        title_card.add_widget(
            MDLabel(
                text="Editar Información del Perfil",
                font_style="H5",
                halign="center",
                bold=True
            )
        )
        content.add_widget(title_card)

        # ============================================================
        # INFORMACIÓN PERSONAL (NO EDITABLE)
        # ============================================================
        info_card = MDCard(
            orientation='vertical',
            adaptive_height=True,
            padding=dp(20),
            spacing=dp(15),
            elevation=1,
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1)
        )

        info_card.add_widget(
            MDLabel(
                text="Información Personal",
                font_style="H6",
                bold=True
            )
        )

        self.nombre_field = MDTextField(
            hint_text="Nombre completo",
            text="Juan Pérez",
            disabled=True,
            mode="rectangle"
        )
        info_card.add_widget(self.nombre_field)

        self.email_field = MDTextField(
            hint_text="Correo electrónico",
            text="juan.perez@alu.uct.cl",
            disabled=True,
            mode="rectangle"
        )
        info_card.add_widget(self.email_field)

        content.add_widget(info_card)

        # ============================================================
        # INFORMACIÓN ADICIONAL
        # ============================================================
        editable_card = MDCard(
            orientation='vertical',
            adaptive_height=True,
            padding=dp(20),
            spacing=dp(15),
            elevation=1,
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1)
        )

        editable_card.add_widget(
            MDLabel(
                text="Información Adicional",
                font_style="H6",
                bold=True
            )
        )

        self.carrera_field = MDTextField(
            hint_text="Carrera",
            text="Ingeniería en Sistemas",
            mode="rectangle",
            icon_left="school"
        )
        editable_card.add_widget(self.carrera_field)

        self.telefono_field = MDTextField(
            hint_text="Teléfono",
            mode="rectangle",
            icon_left="phone",
            input_type="number"
        )
        editable_card.add_widget(self.telefono_field)

        self.direccion_field = MDTextField(
            hint_text="Dirección (opcional)",
            mode="rectangle",
            icon_left="map-marker"
        )
        editable_card.add_widget(self.direccion_field)

        content.add_widget(editable_card)

        # ============================================================
        # BOTONES
        # ============================================================
        buttons = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(15),
            size_hint_y=None,
            height=dp(60)
        )

        cancel_btn = MDFlatButton(
            text="Cancelar",
            text_color=(0.4, 0.4, 0.4, 1),
            on_release=self.go_back
        )
        save_btn = MDRaisedButton(
            text="Guardar Cambios",
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.guardar_cambios
        )

        buttons.add_widget(cancel_btn)
        buttons.add_widget(save_btn)

        content.add_widget(buttons)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

        # Carga los datos
        self.load_user_data()

    # ================================================================
    # Cargar datos del usuario
    # ================================================================
    def load_user_data(self):
        if data_manager.current_user:
            user = data_manager.current_user
            self.nombre_field.text = user.get('nombre', 'Usuario')
            self.email_field.text = user.get('email', '')
            self.carrera_field.text = user.get('carrera', '')
            self.telefono_field.text = user.get('telefono', '')
            self.direccion_field.text = user.get('direccion', '')

    # ================================================================
    # Volver
    # ================================================================
    def go_back(self, instance=None):
        from kivymd.app import MDApp
        MDApp.get_running_app().change_screen('perfil')

    # ================================================================
    # Guardar cambios
    # ================================================================
    def guardar_cambios(self, instance):
        email = self.email_field.text.strip()
        carrera = self.carrera_field.text.strip()
        telefono = self.telefono_field.text.strip()

        # Validación simple
        if not email or '@' not in email or '.' not in email:
            dialog = MDDialog(
                title="Error",
                text="Ingrese un correo electrónico válido.",
                buttons=[MDRaisedButton(text="OK", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
            return

        if data_manager.current_user:
            updated_data = {
                'email': email,
                'carrera': carrera,
                'telefono': telefono,
                'direccion': self.direccion_field.text.strip()
            }
            success = data_manager.update_user(data_manager.current_user['email'], updated_data)
            if success:
                # Update current_user object and save persistently
                data_manager.current_user.update(updated_data)
                data_manager.save_current_user()

        dialog = MDDialog(
            title="Éxito",
            text="Perfil actualizado correctamente.",
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.success(dialog))]
        )
        dialog.open()

    # ================================================================
    def success(self, dialog):
        dialog.dismiss()
        from kivymd.app import MDApp
        app = MDApp.get_running_app()
        app.sm.get_screen('perfil').update_user_info()
        self.go_back()
