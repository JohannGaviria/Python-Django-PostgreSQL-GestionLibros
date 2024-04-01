# Python-Django-PostgreSQL-GestionLibros

API REST que permite a los usuarios gestionar una biblioteca personal de libros. Los usuarios pueden realizar operaciones básicas como agregar, eliminar, actualizar y ver libros en su biblioteca. Además, la API proporciona funcionalidades para buscar libros por título, autor o género.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)

## Instalación

### Prerrequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

- Python (versión 3.12.2)
- PostgreSQL (versión 16)
- pip (administrador de paquetes de Python)

### Pasos de Instalación

1. **Clona este repositorio:**

```
git clone https://github.com/JohannGaviria/Python-Django-PostgreSQL-GestionLibros.git
```

2. **Crear el entorno virtual:**

Utiliza `virtualenv` o otro gestor de entornos virtuales

```
pip install virtualenv
python -m virtualenv nombre_del_entorno
```

3. **Instalar las dependencias:**

```
cd tu_proyecto
pip install -r requirements.txt
```

4. **Configurar la base de datos:**

- Crea una base de datos PostgreSQL en tu entorno.
- Crea un archivo `.env` en la ruta raiz de tu proyecto y crea las variables de entorno con los datos correpodientes:
    - SECRET_KEY=tu_clave_secreta
    - ENGINE=tu_base_de_datos
    - NAME=tu_nombre_de_la_base_de_datos
    - USER=tu_usuario_de_la_base_de_datos
    - PASSWORD=tu_contraseña_de_la_base_de_datos
    - HOST=tu_host
    - PORT=tu_port

5. **Ejecutar el servidor:**

```
python manage.py runserver
```

¡Listo! El proyecto ahora debería estar en funcionamiento en tu entorno local. Puedes acceder a él desde tu navegador web visitando `http://localhost:8000`.

## Uso

1. Ejecuta el servidor de desarrollo: 

```
python manage.py runserver
```

2. Accede a la API a través de las URL definidas.

## API Endpoints

### Autenticación y Autorización

La API utiliza un sistema de autenticación basado en tokens para proteger los endpoints y garantizar que solo los usuarios autenticados puedan acceder a ciertos recursos.

#### Obtener Token de Autenticación

Para obtener un token de autenticación, los usuarios deben registrarse y luego iniciar sesión. Una vez autenticados con éxito, recibirán un token que deben incluir en las solicitudes posteriores como encabezado de autorización.

```http
Authorization: Token xxxxxxxxxxxxxxxxxxxxxxxx
```

#### Solicitud para obtener un token de autenticación

```http
POST /api/user/signIn
Content-Type: application/json

{
  "username": "ejemplo_usuario",
  "password": "ejemplo_contraseña"
}
```

#### Respuesta exitosa con el token de autenticación

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "User": {
    "user_id": 1,
    "username": "ejemplo_usuario",
    "email": "ejemplo@usuario.com"
  }
}
```

### Crear nuevo usuario

```http
POST /api/user/signUp
```

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Requerido**. Nombre de usuario |
| `email` | `string` | **Requerido**. Correo electrónico |
| `password` | `string` | **Requerido**. Contraseña |

#### Registro de un nuevo usuario

```http
POST /api/user/signUp
Content-Type: application/json

{
  "username": "nuevo_usuario",
  "email": "correo@example.com",
  "password": "contraseña"
}
```

#### Respuesta exitosa al registro

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "User": {
    "user_id": 1,
    "username": "nuevo_usuario",
    "email": "correo@example.com"
  }
}
```

### Inciar sesión de usuario

```http
POST /api/user/signIn
```

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Requerido**. Nombre de usuario |
| `password` | `string` | **Requerido**. Contraseña |

#### Inicio de sesión de un usuario

```http
POST /api/user/signIn
Content-Type: application/json

{
  "username": "nuevo_usuario",
  "password": "contraseña"
}
```

#### Respuesta exitosa al inicio de sesión

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "User": {
    "user_id": 1,
    "username": "nuevo_usuario",
    "email": "correo@example.com"
  }
}
```

### Cerrar sesión de usuario

```http
GET /api/user/signOut
```

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Requerido**. Token de autentocación |

#### Cierre de sesión de un usuario

```http
GET /api/user/signOut
Authorization: Token xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Respuesta exitosa al cierre de sesión

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "User signed out successfully"
}
```

### Crear un nuevo libro

```http
POST /api/books/create
```

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `title`     |	`string`   |	**Requerido**. Título del libro |
| `author`    |	`string`	 | **Requerido**. Autor del libro |
| `genre`     |	`string`	 | **Requerido**. Género del libro |
| `publication_year` |	`string` | **Requerido**. Año de publicación del libro |

#### Crear un nuevo libro

```http
POST /api/books/create
Content-Type: application/json
Authorization: Token xxxxxxxxxxxxxxxxxxxxxxxxxxxx

{
  "title": "Nuevo libro",
  "user": 1,
  "author": {
    "full_name": "Nombre del autor",
    "email": "autor@email.com"
  },
  "genre": [
      {"genre": "Genero 1"},
      {"genre": "Genero 2"}
  ],
  "publication_year": 2024
}
```

#### Respuesta exitosa al crear un nuevo libro

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "message": "Successfully created book",
  "Book": {
    "id": 1,
    "user": 1,
    "title": "Nuevo libro",
    "author": {
      "id": 1,
      "full_name": "Nombre del autor",
      "email": "autor@email.com"
    },
    "genre": [
      {
        "id": 6,
        "genre": "Genero 1"
      },
      {
        "id": 7,
        "genre": "Genero 2"
      }
    ],
    "publication_year": 2024
  }
}
```

### Obtener todos los libros

```http
GET /api/books/all
```

#### Obtener todos los libros

```http
GET /api/books/all
Authorization: Token xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Respuesta exitosa al obtener todos los libros

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Correctly obtained books for the current user",
  "Books": [
    {
      "id": 1,
      "user": 1,
      "title": "Nuevo libro",
      "author": {
        "id": 1,
        "full_name": "Nombre del autor",
        "email": "autor@email.com"
      },
      "genre": [
        {
          "id": 1,
          "genre": "Genero 1"
        },
        {
          "id": 2,
          "genre": "Genero 2"
        }
      ],
      "publication_year": 2024
    },
    {
      "id": 2,
      "user": 2,
      "title": "Nuevo libro",
      "author": {
        "id": 2,
        "full_name": "Nombre del autor",
        "email": "autor@email.com"
      },
      "genre": [
        {
          "id": 3,
          "genre": "Genero 3"
        },
        {
          "id": 4,
          "genre": "Genero 4"
        }
      ],
      "publication_year": 2024
    }
  ]
}
```

### Obtener un libro por su ID

```http
GET /api/books/<id>
```

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `id`        |	`integer`  |	**Requerido**. ID del libro a obtener |

#### Obtener un libro por su ID

```http
GET /api/books/<id>
Authorization: Token xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Respuesta exitosa al obtener un libro por su ID

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Correctly obtained book",
  "Book": {
    "id": 1,
    "user": 1,
    "title": "Nuevo libro",
    "author": {
      "id": 1,
      "full_name": "Nombre del autor",
      "email": "autor@email.com"
    },
    "genre": [
      {
        "id": 1,
        "genre": "Genero 1"
      },
      {
        "id": 2,
        "genre": "Genero 2"
      }
    ],
    "publication_year": 2024
  }
}
```

### Actualizar un libro existente

```http
PUT /api/books/update/<id>
```

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `id`        |	`integer`  |	**Requerido**. ID del libro a actualizar |
| `title`     |	`string`   |	**Requerido**. Título actualizado del libro |
| `author`    |	`string`	 | **Requerido**. Autor actualizado del libro |
| `genre`     |	`string`	 | **Requerido**. Género actualizado del libro |
| `publication_year` |	`string` | **Requerido**. Año de publicación actualizado del libro |

#### Actualizar un libro existente

```http
PUT /api/books/update/<id>
Content-Type: application/json
Authorization: Token xxxxxxxxxxxxxxxxxxxxxxxxxxxx

{
  "title": "Nuevo libro",
  "user": 1,
  "author": {
    "full_name": "Nuevo Nombre del autor",
    "email": "nuevo_autor@email.com"
  },
  "genre": [
      {"genre": "Nuevo Genero 1"},
      {"genre": "Nuevo Genero 2"}
  ],
  "publication_year": 2024
}
```

#### Respuesta exitosa al actualizar un libro existente

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Book updated successfully",
  "Book": {
    "id": 1,
    "user": 1,
    "title": "Nuevo libro",
    "author": {
      "id": 1,
      "full_name": "Nuevo Nombre del autor",
      "email": "nuevo_autor@email.com"
    },
    "genre": [
      {
        "id": 1,
        "genre": "Nuevo Genero 1"
      },
      {
        "id": 2,
        "genre": "Nuevo Genero 2"
      }
    ],
    "publication_year": 2024
  }
}
```

### Eliminar un libro existente

```http
DELETE /api/books/<id>
```

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `id`        |	`integer`  |	**Requerido**. ID del libro a eliminar |

#### Eliminar un libro existente
```http
DELETE /api/books/<id>
Authorization: Token xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Respuesta exitosa al eliminar un libro existente
```http
HTTP/1.1 204 No Content

{
  "message": "Book deleted successfully"
}
```

### Busqueda de libros

```http
GET /api/books/searchs/?query=
```

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `query`     |	`string`   |	**Requerido**. Consulta de búsqueda |

**tipos de busquedas:**
  - Titulo del libro
  - Genero del libro
  - Nombre del autor

#### Búsqueda de libros

```http
GET /api/books/searchs/?query=consulta_de_búsqueda
Authorization: Token xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Respuesta exitosa a la búsqueda de libros

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Correctly obtained books",
  "Books": [
    {
      "id": 1,
      "user": 1,
      "title": "libro encontrado 1",
      "author": {
        "id": 1,
        "full_name": "Nombre del autor",
        "email": "autor@email.com"
      },
      "genre": [
        {
          "id": 1,
          "genre": "Genero 1"
        },
        {
          "id": 2,
          "genre": "Genero 2"
        }
      ],
      "publication_year": 2024
    },
    {
      "id": 2,
      "user": 2,
      "title": "libro encontrado 2",
      "author": {
        "id": 2,
        "full_name": "Nombre del autor",
        "email": "autor@email.com"
      },
      "genre": [
        {
          "id": 3,
          "genre": "Genero 3"
        },
        {
          "id": 4,
          "genre": "Genero 4"
        }
      ],
      "publication_year": 2024
    }
  ]
}
```
