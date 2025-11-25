import json
import os
import shutil
from pathlib import Path
from datetime import datetime

class DataManager:
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self.users_file = self.data_dir / "users.json"
        self.products_file = self.data_dir / "products.json"
        self.categories_file = self.data_dir / "categories.json"
        self.assets_dir = Path(__file__).parent / "assets" / "products"
        self.current_user = None
        self.ensure_files_exist()

    def ensure_files_exist(self):
        self.data_dir.mkdir(exist_ok=True)
        self.assets_dir.mkdir(exist_ok=True, parents=True)
        if not self.users_file.exists():
            self.save_json(self.users_file, [])
        if not self.products_file.exists():
            self.save_json(self.products_file, [])
        if not self.categories_file.exists():
            self.save_json(self.categories_file, [])

    def save_json(self, filepath, data):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando {filepath}: {e}")
            return False

    def load_json(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando {filepath}: {e}")
            return []

    # ===== ACTUALIZAR CATEGORÍAS =====
    def update_categories_count(self):
        """Actualiza la cantidad de productos en cada categoría"""
        try:
            products = self.load_json(self.products_file)
            categories = self.load_json(self.categories_file)

            # Contar productos por categoría
            category_counts = {}
            for product in products:
                categoria = product.get("categoria", "Otros")
                category_counts[categoria] = category_counts.get(categoria, 0) + 1

            # Actualizar cantidades en categorías
            for category in categories:
                nombre = category.get("nombre")
                category["cantidad"] = category_counts.get(nombre, 0)

            # Guardar categorías actualizadas
            self.save_json(self.categories_file, categories)
            return True
        except Exception as e:
            print(f"Error actualizando categorías: {e}")
            return False

    # ===== USUARIOS =====
    def register_user(self, email, password, nombre):
        users = self.load_json(self.users_file)
        
        if any(user["email"] == email for user in users):
            return False
        
        new_user = {
            "email": email,
            "password": password,
            "nombre": nombre
        }
        users.append(new_user)
        return self.save_json(self.users_file, users)

    def login_user(self, email, password):
        users = self.load_json(self.users_file)
        for user in users:
            if user["email"] == email and user["password"] == password:
                return True
        return False

    def authenticate_user(self, email, password):
        """Autentica un usuario y retorna sus datos si es válido"""
        users = self.load_json(self.users_file)
        for user in users:
            if user["email"] == email and user["password"] == password:
                self.current_user = email  # Guardar el usuario actual
                return user
        return None
    
    def save_current_user(self):
        """Guarda el usuario actual en un archivo de sesión (opcional)"""
        try:
            session_file = self.data_dir / "session.json"
            session_data = {
                "current_user": self.current_user
            }
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando sesión: {e}")
            return False
    
    def load_current_user(self):
        """Carga el usuario guardado en sesión"""
        try:
            session_file = self.data_dir / "session.json"
            if session_file.exists():
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    self.current_user = session_data.get("current_user")
                    return self.current_user
        except Exception as e:
            print(f"Error cargando sesión: {e}")
        return None

    # ===== PRODUCTOS =====
    def add_product(self, product_data):
        """Agrega un producto y actualiza las categorías"""
        products = self.load_json(self.products_file)
        
        # Generar nuevo ID
        product_data["id"] = max([p.get("id", 0) for p in products], default=0) + 1
        products.append(product_data)
        
        result = self.save_json(self.products_file, products)
        
        # Actualizar categorías después de agregar
        if result:
            self.update_categories_count()
        
        return result

    def delete_product(self, product_id):
        """Elimina un producto y actualiza las categorías"""
        products = self.load_json(self.products_file)
        products = [p for p in products if p.get("id") != product_id]
        
        result = self.save_json(self.products_file, products)
        
        # Actualizar categorías después de eliminar
        if result:
            self.update_categories_count()
        
        return result

    def update_product(self, product_id, updated_data):
        """Actualiza un producto existente y actualiza las categorías"""
        try:
            products = self.load_json(self.products_file)
            
            for product in products:
                if product.get("id") == product_id:
                    product.update(updated_data)
                    break
            
            result = self.save_json(self.products_file, products)
            
            # Actualizar categorías después de modificar
            if result:
                self.update_categories_count()
            
            return result
        except Exception as e:
            print(f"Error actualizando producto: {e}")
            return False

    def save_all_data(self):
        """Guarda todos los datos (puede ser útil para sincronización)"""
        try:
            # Actualizar categorías basadas en productos
            self.update_categories_count()
            return True
        except Exception as e:
            print(f"Error guardando todos los datos: {e}")
            return False

    def get_products(self):
        return self.load_json(self.products_file)
    
    # Alias para compatibilidad
    def get_all_products(self):
        return self.get_products()
    
    def get_products_by_category(self, categoria):
        products = self.load_json(self.products_file)
        return [p for p in products if p.get("categoria") == categoria]
    
    def get_products_by_user(self, email):
        """Obtiene los productos de un usuario específico"""
        products = self.load_json(self.products_file)
        return [p for p in products if p.get("vendedor") == email]
    
    def get_categories(self):
        """Obtiene todas las categorías"""
        return self.load_json(self.categories_file)
    
    def increment_product_views(self, product_id):
        """Incrementa las vistas de un producto"""
        try:
            products = self.load_json(self.products_file)
            
            for product in products:
                if product.get("id") == product_id:
                    product["vistas"] = product.get("vistas", 0) + 1
                    break
            
            self.save_json(self.products_file, products)
            return True
        except Exception as e:
            print(f"Error incrementando vistas: {e}")
            return False

# Instancia global
data_manager = DataManager()
