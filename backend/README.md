# 🚀 FastAPI Enterprise Backend: Clean Architecture & 99% Test Coverage

Este repositorio es una prueba de concepto de grado corporativo que demuestra la migración de una arquitectura legacy en Java (Spring Boot) hacia un ecosistema moderno, ágil y escalable utilizando **Python 3.12, FastAPI y PostgreSQL**. 

El objetivo principal de este proyecto es demostrar cómo aplicar **verdadera Ingeniería de Software** en ecosistemas de Inteligencia Artificial: separando responsabilidades, mitigando vulnerabilidades criptográficas y construyendo una red de pruebas automatizadas que garantiza cero regresiones en producción.

> 🖼️ *[Nota: Inserta aquí la imagen de tu diagrama de Clean Architecture]*  
> `![Arquitectura del Sistema](ruta-a-tu-imagen.png)`

---

## 📊 Resumen Ejecutivo (Impacto de Negocio)

* **Protección Anti-Fallas (99% de Cobertura):** Toda la lógica crítica de negocio está blindada contra errores inesperados.
* **Seguridad Empresarial Criptográfica:** Resolución analítica del límite de truncamiento de Bcrypt (72 bytes) y control de acceso robusto (RBAC).
* **Cero Confianza (Zero Trust):** Mitigación total de ataques IDOR. Los identificadores se extraen de la firma del token, nunca de los parámetros del cliente.
* **Escalabilidad y Persistencia Contenerizada:** El sistema opera sobre PostgreSQL aislado en contenedor Docker, administrado mediante migraciones automáticas con Alembic.

---

## 🏗️ Arquitectura y Seguridad en Detalle

El proyecto adopta un diseño **Multicapa**, asegurando que los Controladores (Routers), Servicios (Lógica de Negocio) y Repositorios (Acceso a Datos) operen de forma independiente.

* **Framework Core:** FastAPI, Pydantic v2, Python 3.12 (Debian Bookworm)
* **Persistencia y Migraciones:** PostgreSQL 14 (Alpine), SQLAlchemy 2.0 (ORM) y Alembic para el control de versiones de la base de datos.
* **Seguridad y Autenticación:**
  * **JWT Sin Estado:** Tokens firmados para validar sesiones en alta concurrencia sin saturar la memoria del servidor.
  * **Custom Bcrypt Pre-Hashing:** Un `Hasher` personalizado que aplica un hash SHA-256 antes de encriptar con Bcrypt, manteniendo intacta la entropía de las contraseñas que superan los 72 caracteres.
  * **RBAC Dinámico:** Dependencias inyectadas (`required_user`, `required_admin`) en las rutas para proteger los endpoints según los privilegios del payload del JWT.
* **Gestión de Entorno:** Principio *fail-fast* para validación de variables de entorno al arranque y soporte nativo CORS.

---

## 🧪 Testing y Métricas de Calidad

La estabilidad del sistema se garantiza mediante una suite integral utilizando **pytest**, **pytest-cov** y **TestClient**, conectada a una base de datos PostgreSQL aislada de pruebas para simular entornos reales sin contaminar los datos de desarrollo.

* **Total de Pruebas:** 96 tests automatizados (100% exitosos).
* **Líneas Auditadas:** 1,485 líneas de código.
* **Cobertura General:** 99% de líneas cubiertas.
* **Cobertura de Negocio:** 100% en Controllers, Services, Repositories, DTOs, Models y Exceptions.

> 🖼️ *[Nota: Inserta aquí la captura de pantalla estética de tu terminal mostrando el 100% pass de pytest]*  
> `![Reporte de Pytest](ruta-a-tu-captura-de-terminal.png)`

### Ejecución de la Suite de Pruebas

```bash
# 1. Ejecutar todas las pruebas
pytest -v

# 2. Ver reporte de cobertura en consola (mostrando líneas faltantes)
pytest --cov=src --cov-report=term-missing

# 3. Generar reporte HTML interactivo
pytest --cov=src --cov-report=html
```
*(Para el reporte HTML, abre `htmlcov/index.html` en el navegador).*

---

## 🛠️ Manual de Operación y Onboarding

### 1. Requisitos Previos
* Docker y Docker Compose instalados.
* Python 3.12 (opcional, solo si deseas ejecutar el backend o pytest directamente en tu máquina host).

### 2. Configuración de Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto con la siguiente estructura base:

```env
PYTHONPATH=./backend/src

# Base de Datos de Desarrollo
DB_HOST=host
DB_PORT=puerto
DB_USER=usuario_desarrollo
DB_PASS=contraseña_desarrollo
DB_NAME=nombre_base_desarrollo

# Base de Datos de Pruebas Local (Pytest)
TEST_DB_URL=postgresql://usuario_desarrollo:contraseña_desarrollo@host:puerto/nombre_base_pruebas

# Configuración Criptográfica
ALGORITHM=HS256
SECRET_KEY=secret_seguro
TOKEN_EXPIRE_MINUTES=30
```

---

### 3. Puesta en Marcha del Entorno

#### Opción A: Entorno Completo con Docker (Recomendado)
Levanta tanto PostgreSQL como el backend con FastAPI en contenedores aislados. Alembic ejecutará automáticamente las migraciones al iniciar el contenedor.

```bash
# 1. Levantar contenedores y construir imagen del backend
docker compose -f docker-compose.test.yml up --build -d

# 2. Crear la base de datos de pruebas (requerido solo la primera vez para pytest)
docker exec -it taskmanager_db psql -U dev -d taskmanager_dev -c "CREATE DATABASE taskmanager_test;"
```

#### Opción B: Modo Híbrido (PostgreSQL en Docker + Backend en Terminal Local)
Si prefieres correr FastAPI y debuggear directamente en tu entorno virtual local:

```bash
# 1. Levantar únicamente el contenedor de PostgreSQL
docker compose -f docker-compose.test.yml up postgres -d

# 2. Crear la base de datos de pruebas (requerido solo la primera vez)
docker exec -it taskmanager_db psql -U dev -d taskmanager_dev -c "CREATE DATABASE taskmanager_test;"

# 3. Crear y activar entorno virtual local
cd backend/src
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar migraciones de Alembic manualmente
alembic upgrade head

# 6. Levantar servidor FastAPI con hot-reload
uvicorn main:app --reload --port 8000
```

---

## 📖 Documentación y Endpoints (OpenAPI)

Al iniciar el servidor, FastAPI autogenera la documentación interactiva. Accede vía Swagger UI en: `http://localhost:8000/docs`

> **Pro Tip para Pruebas:** Usa la ruta `/auth/register` para crear un usuario, y luego haz clic en el botón verde **"Authorize"** en la parte superior. Esto inyectará el JWT en todas tus peticiones posteriores automáticamente.

### Resumen del Contrato de la API:
* **Auth (`/auth`) - Público:** Login (Generación de JWT) y Registro.
* **Users (`/user`) - Solo ADMIN:** Gestión y modificación de perfiles.
* **Projects (`/project`) - USER/ADMIN:** CRUD de proyectos. Los IDs de pertenencia se extraen del token (Anti-IDOR).
* **Tasks (`/task`) - USER/ADMIN:** CRUD y asignación de tareas por responsables.

### Endpoints detallados de la API:

* **Auth Controller (`/auth`) - Público:**
  * `POST /login`: Login de la app (Genera y devuelve el JWT).
  * `POST /register`: Registrar nuevos usuarios.

* **User Controller (`/user`) - Requiere Rol ADMIN:**
  * `GET /{id}`: Obtener información del usuario por ID.
  * `PATCH /{id}`: Cambiar información del usuario por ID.

* **Project Controller (`/project`) - Requiere Rol USER/ADMIN:**
  * `POST /`: Crear nuevo proyecto.
  * `GET /`: Obtener todos los proyectos del líder (el ID se extrae del token, evadiendo IDOR).
  * `GET /{id}`: Obtener proyecto por ID.
  * `PATCH /{id}/changed/{changed}`: Cambiar estado del proyecto.
  * `DELETE /{id}`: Eliminar proyecto.

* **Task Controller (`/task`) - Requiere Rol USER/ADMIN:**
  * `POST /`: Crear una nueva tarea.
  * `GET /{id}`: Obtener tarea por ID.
  * `GET /{id_responsible}/responsible`: Obtener todas las tareas asignadas a un responsable.
  * `PATCH /{id}/change/{change}`: Cambiar estado de la tarea.
  * `DELETE /{id}`: Eliminar tarea.