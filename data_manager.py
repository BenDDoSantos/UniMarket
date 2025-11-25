import json
import os
from pathlib import Path
from datetime import datetime
import uuid
import shutil


class DataManager:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self.products_file = self.data_dir / "products.json"
        self.categories_file = self.data_dir / "categories.json"
        self.current_user_file = self.data_dir / "current_user.json"
        self.current_user = None
        self.initialize_default_data()
        self.load_current_user_from_file()

    def save_current_user(self):
        if self.current_user:
            with open(self.current_user_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_user, f, indent=4, ensure_ascii=False)
        else:
            if self.current_user_file.exists():
                self.current_user_file.unlink()

    def load_current_user_from_file(self):
        if self.current_user_file.exists():
            with open(self.current_user_file, 'r', encoding='utf-8') as f:
                self.current_user = json.load(f)
        else:
            self.current_user = None

    def initialize_default_data(self):
        if not self.users_file.exists():
            default_users = [
                {"email": "mauricio@alu.uct.cl", "password": "123456", "name": "Mauricio"},
                {"email": "juan@alu.uct.cl", "password": "123456", "name": "Juan"},
                {"email": "ana@uct.cl", "password": "123456", "name": "Ana"}
            ]
            self.save_data(self.users_file, default_users)

        if not self.products_file.exists():
            default_products = [
                {"id": 1, "nombre": "Calculadora Científica", "precio": 15000, "descripcion": "Calculadora científica con funciones avanzadas para estudiantes de ingeniería", "imagen": "", "vistas": 45, "vendedor": "mauricio@alu.uct.cl", "estado": "Activo"},
                {"id": 2, "nombre": "Libro de Cálculo I", "precio": 25000, "descripcion": "Libro de cálculo integral usado en primer semestre", "imagen": "", "vistas": 78, "vendedor": "mauricio@alu.uct.cl", "estado": "Vendido"},
                {"id": 3, "nombre": "Mouse Inalámbrico", "precio": 12000, "descripcion": "Mouse óptico inalámbrico, batería incluida", "imagen": "", "vistas": 23, "vendedor": "mauricio@alu.uct.cl", "estado": "Activo"},
                {"id": 4, "nombre": "Cuadernos", "precio": 3000, "descripcion": "Paquete de 5 cuadernos universitarios", "imagen": "", "vistas": 12, "vendedor": "mauricio@alu.uct.cl", "estado": "Activo"},
                {"id": 5, "nombre": "Laptop HP", "precio": 500000, "descripcion": "Laptop HP i5, 8GB RAM, 256GB SSD", "imagen": "", "vistas": 100, "vendedor": "juan@alu.uct.cl", "estado": "Activo"},
                {"id": 6, "nombre": "Audífonos Sony", "precio": 25000, "descripcion": "Audífonos inalámbricos con cancelación de ruido", "imagen": "", "vistas": 50, "vendedor": "ana@uct.cl", "estado": "Activo"},
                {"id": 7, "nombre": "Teclado Mecánico", "precio": 35000, "descripcion": "Teclado mecánico RGB para gaming", "imagen": "", "vistas": 30, "vendedor": "juan@alu.uct.cl", "estado": "Activo"}
            ]
            self.save_data(self.products_file, default_products)

        if not self.categories_file.exists():
            default_categories = [
                {"id": 1, "nombre": "Electrónica"},
                {"id": 2, "nombre": "Libros"},
                {"id": 3, "nombre": "Ropa"},
                {"id": 4, "nombre": "Hogar"},
                {"id": 5, "nombre": "Deportes"},
                {"id": 6, "nombre": "Vehículos"},
                {"id": 7, "nombre": "Servicios"},
                {"id": 8, "nombre": "Otros"}
            ]
            self.save_data(self.categories_file, default_categories)

    def load_data(self, file_path):
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_data(self, file_path, data):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_all_data(self):
        self.users = self.load_data(self.users_file)
        self.products = self.load_data(self.products_file)
        self.categories = self.load_data(self.categories_file)

    def save_all_data(self):
        self.save_data(self.users_file, self.users)
        self.save_data(self.products_file, self.products)
        self.save_data(self.categories_file, self.categories)

    def authenticate_user(self, email, password):
        for user in self.users:
            if user['email'] == email and user['password'] == password:
                return user
        return None

    def register_user(self, email, password, name, telefono='', carrera='', direccion=''):
        # Check if user already exists
        for user in self.users:
            if user['email'] == email:
                return False
        # Generate new id
        max_id = max([u.get('id', 0) for u in self.users], default=0)
        new_user = {
            "id": max_id + 1,
            "email": email,
            "password": password,
            "name": name,
            "telefono": telefono,
            "carrera": carrera,
            "direccion": direccion,
            "created_at": datetime.now().isoformat()
        }
        self.users.append(new_user)
        self.save_all_data()
        return True

    def update_user(self, user_email, updated_data):
        """Update user data and save to JSON"""
        for i, user in enumerate(self.users):
            if user['email'] == user_email:
                self.users[i].update(updated_data)
                self.save_all_data()
                # Update current_user if it's the same user
                if self.current_user and self.current_user['email'] == user_email:
                    self.current_user.update(updated_data)
                return True
        return False

    def get_all_products(self):
        return self.products

    def add_product(self, product):
        # Generate new id
        max_id = max([p.get('id', 0) for p in self.products], default=0)
        product['id'] = max_id + 1
        self.products.append(product)
        self.save_all_data()

    def update_product(self, product_id, updated_product):
        # Si hay nueva imagen y es ruta absoluta, copiar a assets
        if updated_product.get('imagen') and not updated_product['imagen'].startswith('assets/'):
            updated_product['imagen'] = self.copy_image_to_assets(updated_product['imagen'])

        for i, product in enumerate(self.products):
            if product['id'] == product_id:
                self.products[i].update(updated_product)
                self.save_all_data()
                return True
        return False

    def increment_product_views(self, product_id):
        for product in self.products:
            if product['id'] == product_id:
                product['vistas'] += 1
                self.save_all_data()
                return

    def get_products_by_user(self, user_email):
        return [p for p in self.products if p['vendedor'] == user_email]

    def get_categories(self):
        return self.categories

    def get_all_categories(self):
        return self.categories

    def copy_image_to_assets(self, src_path):
        """Copiar imagen a assets/products/ y retornar ruta relativa"""
        if not src_path or not os.path.exists(src_path):
            return ""

        # Crear directorio si no existe
        assets_products_dir = Path("assets/products")
        assets_products_dir.mkdir(parents=True, exist_ok=True)

        # Generar nombre único basado en timestamp y UUID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        file_extension = Path(src_path).suffix.lower()

        # Nombre único para evitar conflictos
        new_filename = f"product_{timestamp}_{unique_id}{file_extension}"
        dest_path = assets_products_dir / new_filename

        try:
            # Copiar archivo
            shutil.copy2(src_path, dest_path)
            # Retornar ruta relativa
            return f"assets/products/{new_filename}"
        except Exception as e:
            print(f"Error copiando imagen: {e}")
            return ""

# Global instance
data_manager = DataManager()
data_manager.load_all_data()
