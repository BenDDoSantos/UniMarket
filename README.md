# Proyecto hecho posible por:

- Benjamin C. Dos Santos - Programador, Analista y Diseño
- Mauricio Mora - Programador, Analista y Base de Datos
- Marco Sandoval - Programador y Analista

En colaboración con el Instituto Tecnológico de la Universidad Católica de Temuco.

## UniMarket - Marketplace Universitario

Es una aplicación móvil desarrollada con Python, Kivy y KivyMD que pretende llegar a ser un "Marketplace universitario".

## Características

- **Pantalla de Login**: Autenticación de usuarios con correo universitario
- **Productos**: Visualización de todos los productos disponibles en formato de grilla
- **Mis Productos**: Gestión de productos del usuario (agregar, editar, ver estado)
- **Categorías**: Exploración de productos por categorías
- **Perfil de usuario**: Pantalla para visualizar al usuario
- **Navegación**: Barra de navegación inferior para fácil acceso entre pantallas
- **Sidebar**: Menú lateral de navegación

## Estructura del Proyecto

```
UniMarket/
├── main.py                 # Archivo principal de la aplicación
├── script.sql              # Archivo donde se muestran las tablas a implementar
├── repo_url.txt            # Archivo de texto que incluye el link hacia el repositorio en GitHub
├── requirements.txt        # Archivo de texto donde se encuentran las dependencias requeridas
├── components/             # Carpeta donde contiene los archivos que hacen posible un sidebar o menu hamburguesa en la aplicación
│   ├── sidebar.py
│   └── sidebar_modal.py
├── diagramas/              # Imágenes y archivos .drawio (Estos podrian no ser exactos en el producto final)
│   ├── Diagrama_entidad-relacion.drawio
│   ├── Diagrama_entidad-relacion.png
│   ├── Modelo_relacional.drawio
│   ├── Modelo_relacional.png
│   └── relational_model.md # Archivo .md con las tablas a utilizar
├── screens/                # Carpeta con todas las pantallas
│   ├── __init__.py
│   ├── perfil_screen.py    # Pantalla del perfil del usuario
│   ├── login_screen.py     # Pantalla de inicio de sesión
│   ├── productos_screen.py    # Pantalla de productos
│   ├── mis_productos_screen.py # Pantalla de mis productos
│   └── categorias_screen.py   # Pantalla de categorías
└── slides/                 # Carpeta que contiene la presentación de la persistencia de datos
    └── presentation.pdf
 
```

## Requisitos

- Python 3.x - Lenguaje de programación principal
- Kivy 2.3.1 - Framework para aplicaciones multiplataforma
- KivyMD 1.2.0 - Componentes Material Design para Kivy
- Pillow 10.4.0 - Biblioteca para procesamiento de imágenes en Python

Introducir este comando para descargar las dependencias requeridas anteriormente mencionadas
```bash
- pip install -r requirements.txt
```

## Instalación

1. Activar el entorno virtual:
```bash
# Windows
UniMarket\Scripts\activate

# Linux/Mac
source UniMarket/bin/activate
```

2. Ejecutar la aplicación:
```bash
python main.py
```

## Pantallas

### 1. Login (login_screen.py)
- Campo de correo universitario
- Campo de contraseña
- Botones de inicio de sesión y registro

### 2. Productos (productos_screen.py)
- Grilla de productos con imágenes
- Barra de búsqueda
- Navegación inferior

### 3. Mis Productos (mis_productos_screen.py)
- Lista de productos del usuario
- Estado de cada producto (Activo/Vendido)
- Botón flotante para agregar nuevos productos
- Opciones de edición

### 4. Categorías (categorias_screen.py)
- Grilla de categorías con iconos
- Contador de productos por categoría
- Colores distintivos por categoría

### 5. Perfil (perfil_screen.py)
- Pantalla simple para visualizar el usuario
- Datos del usuario como: Nombre, Carrera, Activos, etc.
- Botones adicionales para ingresar a mas funcionalidades (Proximamente por implementar)

## Próximas Funcionalidades

- Agregar funcionalidad de búsqueda
- Crear formulario para agregar/editar productos
- Implementar detalle de producto
- Agregar sistema de chat entre usuarios
- Implementar filtros por categoría
- Integrar con base de datos