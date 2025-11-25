📘 UniMarket — Marketplace Universitario

Aplicación móvil desarrollada en Python + KivyMD
Repositorio oficial del proyecto.

📌 Descripción General

UniMarket es una aplicación móvil diseñada para estudiantes universitarios, permitiendo publicar, administrar y visualizar productos dentro de una comunidad cerrada. El sistema está desarrollado en Python, utilizando Kivy y KivyMD, siguiendo una arquitectura modular, escalable y fácil de mantener.

El proyecto permite agregar nuevas funcionalidades sin afectar la estructura base, gracias a su organización por pantallas, componentes reutilizables y capas separadas para datos y lógica.

👥 Equipo de Desarrollo

Proyecto desarrollado por:

Integrante	Rol
Benjamin C. Dos Santos	Programador, Analista
Mauricio Mora	Programador, Arquitectura de Datos
Marco Sandoval	Programador, Analista
Instituto Tecnológico UCT	Asesoría académica
🗂️ Estructura del Proyecto

Estructura contenida en el directorio principal UniMarket-main/:

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
├── utils/
│   ├── auth_utils.py
│   ├── color_utils.py
│   └── validators.py
│
└── __pycache__/

🧠 Lógica General del Proyecto
main.py

Archivo principal que inicializa la aplicación:

Configuración del tema global (MDTheme)

Registro de pantallas

Manejo de navegación

Carga inicial del sistema

📁 Explicación de Carpetas
1. assets/

Archivos estáticos:

images/ → logos e íconos

products/ → imágenes de productos generadas automáticamente

Nombres únicos con UUID + timestamp (manejados por data_manager.py)

2. components/

Componentes UI reutilizables:

custom_bottom_bar.py
Barra inferior personalizada presente en las pantallas principales.

sidebar_modal.py
Menú lateral (hamburguesa) para navegación rápida (perfil, categorías, configuración, etc.).

3. data/

Manejo interno de datos y archivos JSON.

data_manager.py

CRUD de productos

Copiado automático de imágenes

Generación de IDs únicos

Lectura/escritura de JSON

custom_file_manager.py
File manager integrado con KivyMD para seleccionar imágenes.

usuarios.json
Almacenamiento local de usuarios registrados.

4. database/

Archivos JSON utilizados como base de datos local.

products.json
Contiene:

id

nombre

precio

categoría

creador

imagen

descripción

categories.json
Listado de categorías (Ropa, Tecnología, Comida, Servicios, etc.).

5. screens/

Todas las pantallas de la aplicación, cada una con su propia carpeta.

• Login

Autenticación de correo institucional, recordatorio de sesión.

• Register

Formulario extendido, validaciones y paleta institucional.

• Productos

Grid responsivo mostrando todos los productos.

• Mis Productos

CRUD completo: ver, editar, eliminar productos propios.

• Categorías

Filtro dinámico por categoría con colores temáticos.

• Agregar Producto

Formulario con carga de imagen (copiada automáticamente a /assets/products/).

• Editar Producto

Actualización de datos e imagen del producto.

• Perfil

Información básica del usuario y futuras opciones.

6. utils/

Funciones auxiliares reutilizables.

auth_utils.py
Validación de correos institucionales.

color_utils.py
Color asignado según categoría + paleta UCT.

validators.py
Validación de campos (texto, precio, email, etc.).

🚀 Funcionalidades Principales

Inicio de sesión y registro local

Vista general de productos en grilla

CRUD de productos

Selección de imágenes desde explorador

Persistencia mediante JSON

Sidebar y bottom bar personalizadas

Filtrado por categorías

Gestión automática de imágenes y rutas

Colores automáticos según categoría

🧩 Próximas Mejoras

Integración con base de datos real (MongoDB/SQLite)

Sistema de chat vendedor–comprador

Búsqueda avanzada

Notificaciones Push

Favoritos

Filtros combinados (precio, categoría, zona)

Estadísticas de ventas y actividad

🎓 Licencia

Este proyecto se distribuye bajo la licencia incluida en el archivo LICENSE.