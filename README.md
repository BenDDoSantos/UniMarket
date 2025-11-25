📘 UniMarket — Marketplace Universitario

Aplicación móvil desarrollada con Python + KivyMD

<p align="left"> <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge"> <img src="https://img.shields.io/badge/Kivy-2.2-green?style=for-the-badge"> <img src="https://img.shields.io/badge/KivyMD-1.1.1-green?style=for-the-badge"> <img src="https://img.shields.io/badge/Estado-En%20Desarrollo-yellow?style=for-the-badge"> <img src="https://img.shields.io/badge/Licencia-MIT-orange?style=for-the-badge"> </p>
📌 Descripción General

UniMarket es una aplicación móvil diseñada para estudiantes universitarios, con el objetivo de ofrecer un marketplace interno donde puedan publicar, administrar y visualizar productos dentro de una comunidad cerrada.

El sistema está construido en Python, utilizando Kivy y KivyMD, con una arquitectura modular, escalable y mantenible.
El proyecto organiza su estructura en capas claras: interfaz, lógica, datos y persistencia en JSON.

👥 Equipo de Desarrollo
Integrante	Rol
Benjamin C. Dos Santos	Programador, Analista
Mauricio Mora	Programador, Arquitectura de Datos
Marco Sandoval	Diseño, QA
Instituto Tecnológico UCT	Asesoría académica
## 🗂️ Estructura del Proyecto

```
UniMarket-main/
│── main.py
│── README.md
│── LICENSE
│── TODO.md
│
├── assets/
│   ├── images/
│   │   └── uct_logo.png
│   └── products/
│       └── (imágenes autogeneradas)
│
├── components/
│   ├── custom_bottom_bar.py
│   ├── sidebar_modal.py
│   └── (otros componentes)
│
├── data/
│   ├── data_manager.py
│   ├── custom_file_manager.py
│   └── usuarios.json
│
├── database/
│   ├── products.json
│   └── categories.json
│
├── screens/
│   ├── agregar_producto/
│   ├── categorias/
│   ├── editar_producto/
│   ├── login/
│   ├── mis_productos/
│   ├── perfil/
│   ├── productos/
│   └── registro/
│
└── utils/
    ├── auth_utils.py
    ├── color_utils.py
    └── validators.py
```


🧠 Lógica General del Proyecto

## main.py

Archivo principal que inicializa la aplicación:

- Configura el tema global (MDTheme)
- Registra todas las pantallas del sistema
- Administra navegación entre vistas
- Carga inicial de datos

---

## 📁 Explicación de Carpetas

### 1. assets/

Recursos estáticos del sistema.

- `/images` → logos e íconos
- `/products` → imágenes de productos generadas automáticamente (nombres únicos generados por `data_manager.py` usando UUID + timestamp)

### 2. components/

Componentes reutilizables para la interfaz:

- `custom_bottom_bar.py` → barra inferior de navegación
- `sidebar_modal.py` → menú lateral tipo "hamburguesa"

Garantizan consistencia visual en todas las pantallas.

### 3. data/

Manejo de datos y persistencia en JSON.

- **data_manager.py**: CRUD de productos, copia automática de imágenes, IDs únicos, lectura/escritura JSON
- **custom_file_manager.py**: Explorador de archivos KivyMD
- **usuarios.json**: Usuarios registrados localmente

### 4. database/

Almacén principal del proyecto (modo local).

- **products.json**: Contiene id, nombre, precio, categoría, creador, imagen, descripción
- **categories.json**: Lista de categorías (Ropa, Tecnología, Comida, Servicios, etc.)

### 5. screens/

Cada pantalla del sistema en su propio módulo:

- `login/` → autenticación, recordatorio de usuario
- `registro/` → formulario con validaciones
- `productos/` → grid responsivo de productos
- `mis_productos/` → CRUD personal
- `categorias/` → filtrado dinámico
- `agregar_producto/` → formulario + carga de imagen
- `editar_producto/` → edición completa, reemplazo de imagen
- `perfil/` → información básica del usuario

### 6. utils/

Funciones auxiliares:

- `auth_utils.py` → validación de correos
- `color_utils.py` → colores por categoría
- `validators.py` → validaciones de texto, números y emails

---

🚀 Funcionalidades Principales

- Inicio de sesión y registro local
- Visualización de productos en grilla
- CRUD completo de productos
- Copia automática de imágenes al proyecto
- Persistencia en JSON
- Sidebar + barra inferior personalizada
- Filtrado por categorías
- IDs y rutas generadas automáticamente
- Interfaz responsiva hecha en KivyMD

🧩 Próximas Mejoras

- Migración a base de datos (MongoDB o SQLite)
- Chat comprador-vendedor
- Buscador avanzado
- Notificaciones push
- Sistema de favoritos
- Filtros avanzados (precio, categoría, zona)
- Métricas y estadísticas