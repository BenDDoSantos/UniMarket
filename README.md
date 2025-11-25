📘 README – UniMarket

Marketplace Universitario — Aplicación Móvil en KivyMD

📌 Descripción General

UniMarket es una aplicación móvil desarrollada en Python, utilizando Kivy y KivyMD, cuyo objetivo es ofrecer un marketplace universitario donde los estudiantes puedan publicar, administrar y visualizar productos dentro de una comunidad estudiantil.

El proyecto implementa una arquitectura modular, organizada y escalable que permite agregar nuevas funcionalidades sin comprometer la estructura base.

👥 Equipo de Desarrollo

Proyecto realizado por:

Benjamin C. Dos Santos — Programador, Analista

Mauricio Mora — Programador, Programador y Base de Datos

Marco Sandoval — Programador y Analista

En colaboración con el Instituto Tecnológico de la Universidad Católica de Temuco.

🗂️ Estructura del Proyecto

La siguiente estructura corresponde al contenido del proyecto ubicado dentro de UniMarket-main/:

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
│       └── (imágenes generadas de productos)
│
├── components/
│   ├── __init__.py
│   ├── custom_bottom_bar.py
│   ├── sidebar_modal.py
│   └── (otros componentes reutilizables)
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
│   │   └── agregar_producto_screen.py
│   ├── categorias/
│   │   └── categorias_screen.py
│   ├── editar_producto/
│   │   └── editar_producto_screen.py
│   ├── login/
│   │   └── login_screen.py
│   ├── mis_productos/
│   │   └── mis_productos_screen.py
│   ├── perfil/
│   │   └── perfil_screen.py
│   ├── productos/
│   │   └── productos_screen.py
│   └── registro/
│       └── register_screen.py
│
├── utils/
│   ├── auth_utils.py
│   ├── color_utils.py
│   └── validators.py
│
└── __pycache__/ (archivos compilados)

🧠 Lógica General del Proyecto
✔ main.py

Archivo principal del proyecto.
Registra todas las pantallas e inicializa la App.

Incluye:

Carga del tema global (MDTheme)

Manejo de navegación

Registro de pantallas mediante ScreenManager

📁 Explicación de Carpetas

1. assets/

Contiene todos los archivos estáticos del proyecto.

images/

Logos e íconos.

products/

Todas las imágenes de productos guardadas localmente.

Las imágenes se generan automáticamente con nombres únicos usando UUID + timestamp gracias a data_manager.py.

2. components/

Contiene elementos UI reutilizables.

custom_bottom_bar.py

Barra de navegación inferior personalizada con iconos.

Se utiliza en todas las pantallas principales.

sidebar_modal.py

Sidebar lateral (menú hamburguesa).

Acceso rápido al perfil, categorías, configuración, etc.

Permite UI consistente en todas las pantallas.

3. data/

Lógica de datos y manejo de archivos.

data_manager.py

CRUD de productos

Manejo de copias de imágenes

Actualización/lectura de archivos JSON

Generación de claves únicas

custom_file_manager.py

Administrador de archivos para escoger imágenes desde el explorador.

Integrado con KivyMD.

usuarios.json

Almacena temporalmente usuarios registrados (modo local).

4. database/

JSONs que actúan como base de datos local:

products.json

Lista de productos con:

id

nombre

precio

categoría

creador

imagen

descripción

categories.json

Categorías disponibles:

Ropa

Tecnología

Comida

Servicios

Etc.

5. screens/

Contiene todas las pantallas de la aplicación, cada una en su propia carpeta.

🔐 Login Screen

login/login_screen.py

Verificación de correo institucional

Recuerda último correo ingresado

Interfaz ordenada y responsiva

📝 Register Screen

registro/register_screen.py

Formulario extendido

Validaciones de campos

Colores institucionales

🛍️ Productos

productos/productos_screen.py

Muestra todos los productos

Vista tipo grid

Integración con data_manager

👜 Mis Productos

mis_productos/mis_productos_screen.py

CRUD completo local

Editar, ver y eliminar productos propios

🏷️ Categorías

categorias/categorias_screen.py

Filtrado por categoría

Colores distintivos

➕ Agregar Producto

agregar_producto/agregar_producto_screen.py

Formulario con:

Nombre

Precio

Categoría

Imagen

Descripción

Copia automática de la imagen a assets/products/

✏️ Editar Producto

editar_producto/editar_producto_screen.py

Permite reemplazar imagen

Cambiar datos del producto

Guarda cambios en JSON

👤 Perfil

perfil/perfil_screen.py

Información básica del usuario

Opciones adicionales (futuras)

6. utils/

Utilidades generales.

auth_utils.py

Validación de correos institucionales

Manejo básico de autenticación local

color_utils.py

Colores para categorías

Paleta institucional UCT

validators.py

Validaciones reutilizables de campos

Sanitización y verificación de entradas

🚀 Funcionalidades Principales

Sistema de login

Registro de usuarios

Visualización de productos en grilla

Gestión local de productos (CRUD)

Selección de imágenes desde el explorador

Sidebar y navegación inferior

Filtrado por categorías

Persistencia de datos mediante JSON

Asignación automática de colores por categoría

Generación automática de imágenes copiadas al proyecto

🧩 Próximas Mejoras

Base de datos real (MongoDB o SQLite)

Chat entre compradores y vendedores

Buscador avanzado

Notificaciones push

Sistema de favoritos

Filtros combinados (precio, categoría, zona)

Estadísticas de ventas

🎓 Licencia

Este proyecto se distribuye bajo la licencia incluida en LICENSE.