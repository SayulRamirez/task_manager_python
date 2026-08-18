# ⚙️ Backend - FastAPI API

Este directorio contiene la API RESTful del sistema, construida con **FastAPI** y **Python**. El proyecto nace como una migración de un backend legacy en Java (Spring Boot), adoptando una **Arquitectura Limpia (Clean Architecture)** y manteniendo los más altos estándares empresariales de seguridad y separación de responsabilidades.

## ✨ Arquitectura y Seguridad

*   **Multicapa:** Separación estricta entre Controladores (Routers), Servicios (Lógica de Negocio) y Repositorios (Acceso a Datos).
*   **Autenticación y Autorización:**
    *   **JWT Sin Estado:** Tokens firmados para validar sesiones sin saturar la memoria del servidor.
    *   **Hashing Seguro:** Encriptación de contraseñas utilizando **Bcrypt** (con resolución analítica del límite de 72 bytes).
    *   **RBAC (Role-Based Access Control):** Dependencias dinámicas (`required_user`, `required_admin`) para proteger endpoints según el rol del usuario mediante `Depends()`.
    *   **Seguridad contra IDOR (Insecure Direct Object Reference):** Por diseño, los IDs de los usuarios se extraen directamente del payload del token JWT validado, eliminando la confianza ciega en los parámetros enviados por el cliente.
*   **Persistencia de Datos:** Integración de **SQLAlchemy 2.0** como ORM moderno y tipado, configurado actualmente con SQLite.
*   **Gestión de Entorno:** Principio *fail-fast* para la carga de variables de entorno y soporte nativo para **CORS**.

---

## 🛠️ Entorno de Desarrollo Local

### 1. Requisitos Previos
*   Python 3.10 o superior
*   Gestor de paquetes `pip`

### 2. Configuración del Entorno Virtual (venv)
Es fundamental aislar las dependencias del proyecto. Ejecuta los siguientes comandos desde la raíz del proyecto backend:

**En Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**En Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalación de Dependencias
Con el entorno virtual activado, instala las librerías necesarias:
```bash
pip install -r requirements.txt
```

### 4. Variables de Entorno
El proyecto utiliza un sistema estricto de variables de entorno. Crea un archivo llamado `.env` en la raíz de la carpeta `backend/` con la siguiente estructura (ajusta los valores según sea necesario):
```env
SQLITE_PATH=sqlite:///./app.db
SECRET_KEY=ingresa_aqui_tu_clave_secreta_super_segura
ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=30
```

### 5. Ejecutar el Servidor
Para levantar la aplicación en modo desarrollo con recarga automática, ejecuta:
```bash
cd src
uvicorn main:app --reload --port 8000
```
*(Nota: Ajusta `main:app` dependiendo de la ubicación exacta de tu archivo principal y la instancia de FastAPI).*

---

## 📖 Documentación y Endpoints

Al iniciar el servidor, FastAPI autogenera la documentación interactiva OpenAPI. Puedes acceder a ella desde tu navegador:

*   **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)

Para probar los endpoints protegidos desde Swagger, utiliza la ruta `/auth/register` para crear un usuario, y luego haz clic en el botón verde **"Authorize"** en la parte superior para iniciar sesión. Esto guardará tu token JWT y lo inyectará automáticamente en todas las peticiones posteriores.

### Resumen de Rutas de la API:

*   **Auth Controller (`/auth`) - Público:**
    *   `POST /login`: Login de la app (Genera y devuelve el JWT).
    *   `POST /register`: Registrar nuevos usuarios.

*   **User Controller (`/user`) - Requiere Rol ADMIN:**
    *   `GET /{id}`: Obtener información del usuario por ID.
    *   `PATCH /{id}`: Cambiar información del usuario por ID.

*   **Project Controller (`/project`) - Requiere Rol USER/ADMIN:**
    *   `POST /`: Crear nuevo proyecto.
    *   `GET /`: Obtener todos los proyectos del líder (el ID se extrae del token, evadiendo IDOR).
    *   `GET /{id}`: Obtener proyecto por ID.
    *   `PATCH /{id}/changed/{changed}`: Cambiar estado del proyecto.
    *   `DELETE /{id}`: Eliminar proyecto.

*   **Task Controller (`/task`) - Requiere Rol USER/ADMIN:**
    *   `POST /`: Crear una nueva tarea.
    *   `GET /{id}`: Obtener tarea por ID.
    *   `GET /{id_responsible}/responsible`: Obtener todas las tareas asignadas a un responsable.
    *   `PATCH /{id}/change/{change}`: Cambiar estado de la tarea.
    *   `DELETE /{id}`: Eliminar tarea.