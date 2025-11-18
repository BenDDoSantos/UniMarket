from kivy.config import Config

# Configurar la ventana para simular un dispositivo móvil
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'resizable', '0')

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivy.metrics import dp

# Importar data manager
from data_manager import data_manager

# Importar las pantallas
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.productos_screen import ProductosScreen
from screens.mis_productos_screen import MisProductosScreen
from screens.agregar_producto_screen import AgregarProductoScreen
from screens.categorias_screen import CategoriasScreen
from screens.perfil_screen import PerfilScreen
from screens.detalle_producto_screen import DetalleProductoScreen
from screens.editar_producto_screen import EditarProductoScreen
from screens.editar_perfil_screen import EditarPerfilScreen
from components.sidebar_modal import SidebarModal

class UniMarketApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Light"
        
        # Crear el screen manager directamente
        self.sm = MDScreenManager()
        
        # Agregar todas las pantallas
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(RegisterScreen(name='register'))
        self.sm.add_widget(ProductosScreen(name='productos'))
        self.sm.add_widget(MisProductosScreen(name='mis_productos'))
        self.sm.add_widget(AgregarProductoScreen(name='agregar_producto'))
        self.sm.add_widget(CategoriasScreen(name='categorias'))
        self.sm.add_widget(PerfilScreen(name='perfil'))
        self.sm.add_widget(DetalleProductoScreen(name='detalle_producto'))
        self.sm.add_widget(EditarProductoScreen(name='editar_producto'))
        self.sm.add_widget(EditarPerfilScreen(name='editar_perfil'))
        
        return self.sm
    
    def change_screen(self, screen_name):
        """Cambiar de pantalla"""
        self.sm.current = screen_name
    
    def toggle_nav_drawer(self):
        """Abrir/cerrar el sidebar"""
        if not hasattr(self, 'sidebar_modal') or self.sidebar_modal is None:
            self.sidebar_modal = SidebarModal()
        self.sidebar_modal.open()

    def logout(self):
        """Cerrar sesión: eliminar estado de sesión pero mantener último correo"""
        data_manager.current_user = None


if __name__ == '__main__':
    UniMarketApp().run()