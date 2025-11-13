from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivymd.app import MDApp


class CustomBottomBar(MDCard):
    def __init__(self, current_screen, navigation_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = dp(64)
        self.elevation = 4
        self.radius = [dp(0), dp(0), dp(0), dp(0)]  # No rounded corners for bottom bar
        self.padding = dp(10)
        self.spacing = dp(20)

        # Define the navigation items
        self.nav_items = [
            {"screen": "productos", "icon": "shopping", "text": "Productos"},
            {"screen": "categorias", "icon": "format-list-bulleted", "text": "Categorías"},
            {"screen": "mis_productos", "icon": "briefcase", "text": "Mis Productos"}
        ]

        # Create buttons
        for item in self.nav_items:
            btn_layout = MDBoxLayout(orientation='vertical', size_hint=(1, 1), spacing=dp(2))
            btn = MDIconButton(
                icon=item["icon"],
                size_hint=(None, None),
                size=(dp(24), dp(24)),
                pos_hint={'center_x': 0.5}
            )
            label = MDLabel(
                text=item["text"],
                font_style="Caption",
                halign="center",
                size_hint_y=None,
                height=dp(16),
                pos_hint={'center_x': 0.5}
            )

            # Set active state
            if item["screen"] == current_screen:
                btn.theme_icon_color = "Custom"
                btn.icon_color = MDApp.get_running_app().theme_cls.primary_color
                label.theme_text_color = "Custom"
                label.text_color = MDApp.get_running_app().theme_cls.primary_color
                # Optional: Add underline indicator
                label.underline = True
            else:
                btn.theme_icon_color = "Secondary"
                label.theme_text_color = "Secondary"

            # Bind navigation
            btn.bind(on_release=lambda x, s=item["screen"]: navigation_callback(s))

            btn_layout.add_widget(btn)
            btn_layout.add_widget(label)
            self.add_widget(btn_layout)
