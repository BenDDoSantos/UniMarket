from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivy.uix.image import AsyncImage
from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp


class ImageThumbnail(MDBoxLayout):
    def __init__(self, path, parent_screen, **kwargs):
        super().__init__(**kwargs)

        self.path = path
        self.parent_screen = parent_screen

        # Each thumbnail HAS a fixed size enforced
        self.size_hint = (None, None)
        w = self.size[0] if self.size[0] else dp(80)
        h = self.size[1] if self.size[1] else dp(80)
        self.size = (w, h)

        # Ensure vertical alignment and no weird expansion
        self.orientation = "vertical"
        self.padding = 0
        self.spacing = 0

        # --- FIX REAL: RelativeLayout MUST have fixed size ---
        container = RelativeLayout(
            size_hint=(None, None),
            size=(w, h)
        )

        # The image fits inside the thumbnail, no overflow
        img = AsyncImage(
            source=path,
            size_hint=(None, None),
            size=(w, h),
            allow_stretch=True,
            keep_ratio=True
        )
        container.add_widget(img)

        # Close button positioned inside the RelativeLayout
        close_btn = MDIconButton(
            icon="close",
            icon_size=dp(18),
            md_bg_color=(1, 0, 0, 0.8),
            pos_hint={"right": 1, "top": 1},
            on_release=lambda x: parent_screen.remove_image(path)
        )
        container.add_widget(close_btn)

        self.add_widget(container)
