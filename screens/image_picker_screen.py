from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivy.lang import Builder
from kivy.utils import platform
import os

# ButtonBehavior + AsyncImage to make images clickable
class ImageButton(ButtonBehavior, AsyncImage):
    pass

class ImagePickerScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_select = lambda path: None  # Placeholder callback, to be set by caller
        
        # Determine base pictures paths to try on Windows
        potential_paths = [
            os.path.expanduser("~/Pictures"),   # Prefer this first on Windows
            os.path.expanduser("~/Imágenes"),
            os.path.join(os.path.expanduser("~"), "OneDrive", "Imágenes"),
            os.path.join(os.path.expanduser("~"), "Pictures")
        ]

        self.base_path = None
        for path in potential_paths:
            if os.path.exists(path):
                self.base_path = path
                break

        if not self.base_path:
            self.base_path = os.path.expanduser("~")  # fallback
        
        print("SCAN PATH (init):", self.base_path)
        
        # Top app bar with back button
        self.toolbar = MDTopAppBar(
            title="Seleccionar imagen",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=10,
            pos_hint={"top": 1}
        )
        self.add_widget(self.toolbar)

        # ScrollView with GridLayout
        self.scroll = ScrollView(
            size_hint=(1, None),
            size=(self.width, self.height - dp(56)),  # 56dp is typical toolbar height
            pos_hint={"top": 0.95},
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=dp(8),
        )
        
        self.grid = GridLayout(
            cols=4,
            padding=dp(10),
            spacing=dp(10),
            size_hint_y=None,
        )
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)

        self.load_images(self.base_path)

    def load_images(self, path):
        print("SCAN PATH:", path)  # Debug
        self.current_path = path
        self.grid.clear_widgets()

        try:
            items = os.listdir(path)
            print("FILES FOUND:", items)  # Debug
        except Exception as e:
            print("Error reading directory:", e)
            items = []

        # Sort items: folders first, then files
        folders = []
        images = []
        allowed_exts = {".jpg", ".jpeg", ".png", ".webp"}

        for item in sorted(items, key=str.lower):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                folders.append(item)
            else:
                if os.path.splitext(item)[1].lower() in allowed_exts:
                    images.append(item)

        # Add folder thumbnails (placeholder icon must exist)
        for folder in folders:
            btn = ImageButton(
                source="assets/images/folder_icon.png",  # Folder icon placeholder, ensure exists
                size_hint=(None, None),
                size=(dp(110), dp(110)),
                allow_stretch=True,
                keep_ratio=True,
            )
            btn.bind(on_release=lambda btn, f=folder: self.load_images(os.path.join(self.current_path, f)))
            self.grid.add_widget(btn)

        # Add image thumbnails
        for image in images:
            full_image_path = os.path.join(path, image)
            btn = ImageButton(
                source=full_image_path,
                size_hint=(None, None),
                size=(dp(110), dp(110)),
                allow_stretch=True,
                keep_ratio=True,
            )
            btn.bind(on_release=lambda btn, p=full_image_path: self.select_image(p))
            self.grid.add_widget(btn)

    def select_image(self, path):
        # Call the callback with selected image path
        self.on_select(path)

    def go_back(self):
        # Default behavior: just go back to previous screen
        app = self.manager.app if hasattr(self.manager, 'app') else None
        if app:
            app.change_screen('agregar_producto')  # Or any fallback screen name
        else:
            if self.manager:
                self.manager.current = 'agregar_producto'
