from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton, MDIconButton
from kivy.metrics import dp
from kivy.uix.image import AsyncImage
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from data_manager import data_manager


class MisProductosScreen(MDScreen):

    def on_pre_enter(self):
        self.clear_widgets()
        self.build_ui()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):

        root = FloatLayout()
        main = MDBoxLayout(orientation="vertical")

        # ========== TOOLBAR ==========
        toolbar = MDTopAppBar(
            title="Mis Productos",
            elevation=2,
            left_action_items=[["menu", lambda x: self.toggle_nav_drawer()]],
        )
        main.add_widget(toolbar)

        # ========== SCROLL ==========
        scroll = MDScrollView(size_hint_y=1)
        lista = MDBoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10),
            size_hint_y=None
        )
        lista.bind(minimum_height=lista.setter("height"))

        productos = data_manager.get_products_by_user(
            data_manager.current_user["email"]
        ) if data_manager.current_user else []

        for producto in productos:

            card = MDCard(
                size_hint=(1, None),
                height=dp(90),
                elevation=1,
                radius=[dp(10)]
            )
            fila = MDBoxLayout(
                orientation="horizontal",
                padding=dp(10),
                spacing=dp(10)
            )

            # ========== MINIATURA ==========
            imagenes = producto.get("imagenes", [])
            imagen_principal = imagenes[0] if imagenes else "assets/no_image.png"

            mini = AsyncImage(
                source=imagen_principal,
                size_hint=(None, None),
                size=(dp(60), dp(60)),
                allow_stretch=True,
                keep_ratio=True
            )
            fila.add_widget(mini)

            # ========== TEXTO ==========
            textos = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, 1)
            )
            textos.add_widget(MDLabel(
                text=producto["nombre"],
                font_style="Body1",
                halign="left"
            ))
            textos.add_widget(MDLabel(
                text=f"{producto['estado']} - ${producto['precio']:,}",
                font_style="Caption",
                halign="left"
            ))
            fila.add_widget(textos)

            # ========== BOTONES ==========
            botones = MDBoxLayout(
                orientation="horizontal",
                size_hint=(None, None),
                size=(dp(100), dp(40)),
                spacing=dp(10)
            )

            edit = MDIconButton(
                icon="pencil",
                size_hint=(None, None),
                size=(dp(35), dp(35)),
                icon_color=(0.3, 0.3, 0.3, 1)
            )
            edit.bind(
                on_release=lambda x, p=producto: self.editar_producto(p)
            )
            botones.add_widget(edit)

            delete = MDIconButton(
                icon="delete",
                size_hint=(None, None),
                size=(dp(35), dp(35)),
                icon_color=(0.8, 0.2, 0.2, 1)
            )
            delete.bind(
                on_release=lambda x, p=producto: self.eliminar_producto(p)
            )
            botones.add_widget(delete)

            fila.add_widget(botones)
            card.add_widget(fila)
            lista.add_widget(card)

        scroll.add_widget(lista)
        main.add_widget(scroll)

        # ========== FAB ==========
        fab = MDFloatingActionButton(
            icon="plus",
            elevation=3,
            size_hint=(None, None),
            size=(dp(56), dp(56)),
            pos_hint={"right": 0.95},
            y=dp(90),
            on_release=lambda x: MDApp.get_running_app().change_screen("agregar_producto")
        )

        main.add_widget(fab)

        from components.custom_bottom_bar import CustomBottomBar
        bottom = CustomBottomBar(
            current_screen="mis_productos",
            navigation_callback=self.navigate
        )
        main.add_widget(bottom)

        root.add_widget(main)
        self.add_widget(root)

    # ===========================
    #  FUNCIONES
    # ===========================
    def navigate(self, screen):
        if screen != "mis_productos":
            MDApp.get_running_app().change_screen(screen)

    def toggle_nav_drawer(self):
        MDApp.get_running_app().toggle_nav_drawer()

    def editar_producto(self, producto):
        app = MDApp.get_running_app()
        screen = app.sm.get_screen("editar_producto")
        screen.cargar_producto(producto)
        app.change_screen("editar_producto")

    def eliminar_producto(self, producto):
        dialog = MDDialog(
            title="Eliminar Producto",
            text=f"¿Seguro que deseas eliminar '{producto['nombre']}'?",
            buttons=[
                MDRaisedButton(text="Cancelar", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(
                    text="Eliminar",
                    md_bg_color=(1, 0, 0, 1),
                    on_release=lambda x: self.confirmar_eliminar(producto, dialog)
                ),
            ],
        )
        dialog.open()

    def confirmar_eliminar(self, producto, dialog):
        """Confirma la eliminación del producto"""
        # Cambiar esta línea:
        # data_manager.products = [p for p in data_manager.products if p["id"] != producto["id"]]
        
        # Por esto:
        data_manager.delete_product(producto["id"])
        
        # Cerrar diálogo y actualizar UI
        dialog.dismiss()
        self.build_ui()
        
        # Mostrar confirmación
        from kivymd.toast import toast
        toast("Producto eliminado")
