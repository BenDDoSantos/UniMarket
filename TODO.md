# TODO - Fix image display in editar_producto_screen.py

- [ ] Update the method cargar_producto to ensure correct assignments (already okay).
- [ ] Modify build_ui to call refresh_thumbnails only when self.selected_images is not empty.
- [ ] Modify refresh_thumbnails:
    - Add early return if self.selected_images is empty, set thumbnail_container.width=0
    - Import os
    - Join image paths with the assets/products folder for correct absolute path resolution
- [ ] Ensure ImageThumbnail import remains correct.
- [ ] Keep compatibility with agregar_producto_screen.py and ImageThumbnail class.

After applying the above steps, test editar_producto_screen loading products with existing images to verify that thumbnails display properly.
