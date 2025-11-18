from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
from kivymd.uix.button import MDIconButton
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from data_manager import data_manager


class MisProductosScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def on_enter(self):
        """Refrescar la lista cuando se entra a la pantalla"""
        self.clear_widgets()
        self.build_ui()

    def build_ui(self):
        # === ROOT ===
        root_layout = FloatLayout()

        # === MAIN LAYOUT VERTICAL ===
        main_layout = MDBoxLayout(orientation='vertical', size_hint=(1, 1))

        # Toolbar superior
        toolbar = MDTopAppBar(
            title="Mis Productos",
            left_action_items=[["menu", lambda x: self.toggle_nav_drawer()]],
            right_action_items=[["dots-vertical", lambda x: self.show_options()]],
            id="toolbar",
            elevation=0,
        )
        main_layout.add_widget(toolbar)

        # Scroll con los productos
        scroll = MDScrollView(size_hint_y=1)

        products_list = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=(dp(10), dp(10), dp(10), dp(10)),
            size_hint_y=None
        )
        products_list.bind(minimum_height=products_list.setter("height"))

        # Cargar productos del usuario actual
        if data_manager.current_user:
            self.mis_productos = data_manager.get_products_by_user(data_manager.current_user["email"])
        else:
            self.mis_productos = []

        for producto in self.mis_productos:
            card = MDCard(
                size_hint=(1, None),
                height=dp(80),
                elevation=0,
                radius=[dp(10)],
                on_release=lambda x, p=producto: self.ver_detalle(p),
            )

            card_layout = MDBoxLayout(orientation="horizontal", padding=dp(10), spacing=dp(10))

            # Imagen del producto o icono por defecto
            if producto.get("imagen") and producto["imagen"]:
                from kivy.uix.image import Image
                img = Image(
                    source=producto["imagen"],
                    size_hint=(None, None),
                    size=(dp(60), dp(60)),
                    allow_stretch=True,
                    keep_ratio=False
                )
                card_layout.add_widget(img)
            else:
                icon = MDIconButton(icon="package-variant", size_hint=(None, None), size=(dp(60), dp(60)), disabled=True)
                card_layout.add_widget(icon)

            # Texto
            text_layout = MDBoxLayout(orientation="vertical", size_hint=(1, 1))
            name_label = MDLabel(text=producto["nombre"], font_style="Body1", halign="left")
            status_label = MDLabel(
                text=f"{producto['estado']} - ${producto['precio']:,}",
                font_style="Caption",
                halign="left"
            )
            text_layout.add_widget(name_label)
            text_layout.add_widget(status_label)
            card_layout.add_widget(text_layout)

            # Botones derecha
            buttons_layout = MDBoxLayout(orientation="horizontal", size_hint=(None, None), size=(dp(100), dp(40)), spacing=dp(10))

            edit_btn = MDIconButton(
                icon="pencil", size_hint=(None, None), size=(dp(35), dp(35)),
                icon_color=(0.3, 0.3, 0.3, 1)
            )
            edit_btn.bind(on_release=lambda x, p=producto: self.editar_producto(p))
            buttons_layout.add_widget(edit_btn)

            delete_btn = MDIconButton(
                icon="delete", size_hint=(None, None), size=(dp(35), dp(35)),
                icon_color=(0.8, 0.2, 0.2, 1)
            )
            delete_btn.bind(on_release=lambda x, p=producto: self.eliminar_producto(p))
            buttons_layout.add_widget(delete_btn)

            card_layout.add_widget(buttons_layout)

            card.add_widget(card_layout)
            products_list.add_widget(card)

        scroll.add_widget(products_list)
        main_layout.add_widget(scroll)

        # === Bottom Bar ===
        from components.custom_bottom_bar import CustomBottomBar

        bottom_bar = CustomBottomBar(
            current_screen="mis_productos",
            navigation_callback=self.navigate_to_screen
        )
        main_layout.add_widget(bottom_bar)

        # Agregar main layout
        root_layout.add_widget(main_layout)

        # === FAB flotante (corregido) ===
        fab = MDFloatingActionButton(
            icon="plus",
            size_hint=(None, None),
            size=(dp(56), dp(56)),
            elevation=3,
            on_release=self.add_producto,

            # ⭐ CORRECTA POSICIÓN:
            pos_hint={"right": 0.95},
            y=dp(90),     # 64dp bottom bar + 16dp separación + altura FAB
        )
        root_layout.add_widget(fab)

        self.add_widget(root_layout)

    # ========= FUNCIONES =========

    def toggle_nav_drawer(self):
        MDApp.get_running_app().toggle_nav_drawer()

    def show_options(self):
        menu_items = [
            {"text": "Actualizar lista", "viewclass": "OneLineListItem", "on_release": lambda x="Actualizar lista": self.menu_callback(x)},
            {"text": "Ver estadísticas generales", "viewclass": "OneLineListItem", "on_release": lambda x="Ver estadísticas generales": self.menu_callback(x)},
            {"text": "Cerrar sesión", "viewclass": "OneLineListItem", "on_release": lambda x="Cerrar sesión": self.menu_callback(x)},
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.toolbar.right_action_items[0][1],
            items=menu_items,
            width_mult=4,
        )
        self.menu.open()

    def add_producto(self, instance):
        app = MDApp.get_running_app()
        app.change_screen("agregar_producto")

    def navigate_to_screen(self, screen_name):
        if screen_name != "mis_productos":
            MDApp.get_running_app().change_screen(screen_name)

    def ver_detalle(self, producto):
        app = MDApp.get_running_app()
        screen = app.sm.get_screen("detalle_producto")
        screen.producto = producto
        screen.clear_widgets()
        screen.build_ui()
        app.change_screen("detalle_producto")

    def editar_producto(self, producto):
        app = MDApp.get_running_app()
        screen = app.sm.get_screen("editar_producto")
        screen.producto = producto
        screen.clear_widgets()
        screen.build_ui()
        app.change_screen("editar_producto")

    def eliminar_producto(self, producto):
        dialog = MDDialog(
            title="Eliminar Producto",
            text=f"¿Estás seguro de eliminar '{producto['nombre']}'?",
            buttons=[
                MDRaisedButton(text="Cancelar", on_release=lambda x: dialog.dismiss()),
                MDRaisedButton(text="Eliminar", md_bg_color=(1, 0, 0, 1),
                               on_release=lambda x: self.confirmar_eliminar(producto, dialog))
            ]
        )
        dialog.open()

    def confirmar_eliminar(self, producto, dialog):
        dialog.dismiss()
        data_manager.products = [p for p in data_manager.products if p["id"] != producto["id"]]
        data_manager.save_all_data()
        self.clear_widgets()
        self.build_ui()

    def menu_callback(self, text):
        self.menu.dismiss()
        if text == "Actualizar lista":
            self.clear_widgets()
            self.build_ui()
        elif text == "Ver estadísticas generales":
            self.ver_estadisticas()
        elif text == "Cerrar sesión":
            MDApp.get_running_app().change_screen("login")

    def ver_estadisticas(self):
        activos = len([p for p in self.mis_productos if p["estado"] == "Activo"])
        vendidos = len([p for p in self.mis_productos if p["estado"] == "Vendido"])
        total_vistas = sum(p["vistas"] for p in self.mis_productos)
        promedio = total_vistas / len(self.mis_productos) if self.mis_productos else 0

        dialog = MDDialog(
            title="Estadísticas",
            text=f"Activos: {activos}\nVendidos: {vendidos}\nPromedio vistas: {promedio:.1f}",
            buttons=[MDRaisedButton(text="Cerrar", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()
