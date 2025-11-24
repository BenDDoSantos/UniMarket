from kivymd.uix.filemanager import MDFileManager
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from kivy.lang import Builder
import os


class CustomFileManager(MDFileManager):
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}

    def generate_file_list(self, *args):
        """
        Override to show thumbnails for image files using AsyncImage
        while keeping folder icons unchanged.
        """
        files = []
        current_path = self.current_path
        files_and_dirs = self.get_files_and_directories(current_path)

        # Build files list for display
        for filename, ftype in sorted(files_and_dirs, key=lambda x: (x[1] != "dir", x[0].lower())):
            file_path = os.path.join(current_path, filename)
            # Folder entry
            if ftype == "dir":
                files.append(
                    self.get_file_manager_entry(
                        filename,
                        file_path,
                        is_dir=True,
                    )
                )
            else:
                ext = os.path.splitext(filename)[1].lower()
                if ext in self.IMAGE_EXTENSIONS:
                    # Create AsyncImage thumbnail instead of default icon
                    thumbnail = AsyncImage(
                        source=file_path,
                        size_hint=(None, None),
                        size=(dp(80), dp(80)),
                        allow_stretch=True,
                        keep_ratio=True,
                    )
                    files.append(
                        self.get_file_manager_entry(
                            filename,
                            file_path,
                            custom_icon=thumbnail,
                            is_dir=False,
                        )
                    )
                else:
                    # Default file entry
                    files.append(
                        self.get_file_manager_entry(
                            filename,
                            file_path,
                            is_dir=False,
                        )
                    )
        return files
