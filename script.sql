import sqlite3

DB_NAME = "unimarket.db"

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Crear tabla Campus
    cursor.execute('''CREATE TABLE IF NOT EXISTS Campus (
        campus_ID INTEGER PRIMARY KEY,
        nombre_campus TEXT
    );''')

    # Crear tabla PerfilUsuario
    cursor.execute('''CREATE TABLE IF NOT EXISTS PerfilUsuario (
        perfilUsuario_ID INTEGER PRIMARY KEY,
        foto_perfil TEXT,
        telefono TEXT,
        facultad TEXT,
        carrera TEXT,
        año_ingreso INTEGER,
        campus_ID INTEGER,
        FOREIGN KEY (campus_ID) REFERENCES Campus(campus_ID)
    );''')

    # Crear tabla Usuario
    cursor.execute('''CREATE TABLE IF NOT EXISTS Usuario (
        usuario_ID INTEGER PRIMARY KEY,
        nombre TEXT,
        apellido TEXT,
        correo_institucional TEXT,
        contraseña TEXT,
        rol TEXT,
        fecha_registro TEXT,
        estado_cuenta TEXT,
        campus_ID INTEGER,
        perfilUsuario_ID INTEGER,
        FOREIGN KEY (campus_ID) REFERENCES Campus(campus_ID),
        FOREIGN KEY (perfilUsuario_ID) REFERENCES PerfilUsuario(perfilUsuario_ID)
    );''')

    # Crear tabla Chat
    cursor.execute('''CREATE TABLE IF NOT EXISTS Chat (
        chat_ID INTEGER PRIMARY KEY,
        comprador_ID INTEGER,
        vendedor_ID INTEGER,
        publicacion_ID INTEGER,
        FOREIGN KEY (comprador_ID) REFERENCES Usuario(usuario_ID),
        FOREIGN KEY (vendedor_ID) REFERENCES Usuario(usuario_ID)
    );''')

    # Crear tabla Publicacion
    cursor.execute('''CREATE TABLE IF NOT EXISTS Publicacion (
        publicacion_ID INTEGER PRIMARY KEY,
        titulo TEXT,
        descripcion TEXT,
        categoria TEXT,
        precio REAL,
        fecha_creacion TEXT,
        usuario_ID INTEGER,
        chat_ID INTEGER,
        favorito_ID INTEGER,
        FOREIGN KEY (usuario_ID) REFERENCES Usuario(usuario_ID),
        FOREIGN KEY (chat_ID) REFERENCES Chat(chat_ID)
    );''')

    # Crear tabla ImagenPublicacion
    cursor.execute('''CREATE TABLE IF NOT EXISTS ImagenPublicacion (
        imagen_ID INTEGER PRIMARY KEY,
        url_imagen TEXT,
        publicacion_ID INTEGER,
        FOREIGN KEY (publicacion_ID) REFERENCES Publicacion(publicacion_ID)
    );''')

    # Crear tabla Mensaje
    cursor.execute('''CREATE TABLE IF NOT EXISTS Mensaje (
        mensaje_ID INTEGER PRIMARY KEY,
        chat_ID INTEGER,
        usuario_ID INTEGER,
        contenido TEXT,
        fecha_mensaje TEXT,
        hora_mensaje TEXT,
        FOREIGN KEY (chat_ID) REFERENCES Chat(chat_ID),
        FOREIGN KEY (usuario_ID) REFERENCES Usuario(usuario_ID)
    );''')

    # Crear tabla Reseña
    cursor.execute('''CREATE TABLE IF NOT EXISTS Reseña (
        reseña_ID INTEGER PRIMARY KEY,
        publicacion_ID INTEGER,
        usuario_ID INTEGER,
        contenido TEXT,
        fecha_comentario TEXT,
        FOREIGN KEY (publicacion_ID) REFERENCES Publicacion(publicacion_ID),
        FOREIGN KEY (usuario_ID) REFERENCES Usuario(usuario_ID)
    );''')

    # Crear tabla Favoritos
    cursor.execute('''CREATE TABLE IF NOT EXISTS Favoritos (
        favorito_ID INTEGER PRIMARY KEY,
        publicacion_ID INTEGER,
        usuario_ID INTEGER,
        FOREIGN KEY (publicacion_ID) REFERENCES Publicacion(publicacion_ID),
        FOREIGN KEY (usuario_ID) REFERENCES Usuario(usuario_ID)
    );''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
