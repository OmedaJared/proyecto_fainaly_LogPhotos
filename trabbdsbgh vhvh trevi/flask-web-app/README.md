# photo-app

`photo-app` es una aplicación web Flask para registrar usuarios, iniciar sesión, recuperar contraseñas y administrar archivos o enlaces por categorías.  
El proyecto usa una estructura simple, dependencias modernas en `pyproject.toml` y un archivo `main.py` que contiene toda la lógica funcional de la app.

---

## Resumen rápido

La aplicación actualmente permite:

- registro de usuarios,
- inicio y cierre de sesión,
- recuperación de contraseña con token temporal,
- subida de archivos al servidor,
- guardado de enlaces,
- categorización de contenido,
- eliminación de archivos y enlaces,
- protección de rutas privadas con sesión.

La persistencia todavía es en memoria para usuarios, tokens y registros de archivos, por lo que los datos se pierden al reiniciar la aplicación.

---

## Tecnologías y librerías

### Flask
Framework web principal.

#### Se usa para
- crear la aplicación `app`,
- definir rutas con `@app.route`,
- renderizar plantillas HTML,
- redirigir con `redirect`,
- construir URLs con `url_for`,
- manejar solicitudes con `request`,
- trabajar con sesiones con `session`,
- enviar archivos con `send_from_directory`,
- abortar errores con `abort`.

#### En este proyecto
Flask es el núcleo de toda la aplicación y administra:
- `/`
- `/register`
- `/login`
- `/logout`
- `/recover`
- `/reset/<token>`
- `/dashboard`
- `/index`
- `/uploads/<path:filename>`
- `/upload`
- `/delete/<path:filename>`
- `/delete_link/<link_id>`
- `/favicon.ico`

---

### Werkzeug
Librería base del ecosistema Flask.

#### Se usa para
- `generate_password_hash(password)` para almacenar contraseñas con hash,
- `check_password_hash(hash, password)` para validar credenciales,
- `secure_filename(filename)` para limpiar nombres de archivo antes de guardarlos.

#### En este proyecto
Evita guardar contraseñas en texto plano y reduce riesgos al recibir nombres de archivo desde el usuario.

---

### `email-validator`
Dependencia declarada en `pyproject.toml`.

#### Uso esperado
Está pensada para validar direcciones de correo electrónico en formularios.

#### En el código actual
La validación de email se hace con una expresión regular en `normalize_email()`, pero la dependencia sigue disponible para una validación más robusta si el proyecto evoluciona.

---

### `pymongo`
Driver oficial de MongoDB para Python.

#### Uso esperado
- conectar con MongoDB,
- leer y escribir documentos,
- manejar usuarios, archivos y tokens de recuperación.

#### En el código actual
No está conectado todavía; el almacenamiento real se hace en estructuras de memoria:
- `users`
- `reset_tokens`
- `file_records`

---

### `flask-pymongo`
Integración entre Flask y MongoDB.

#### Uso esperado
- simplificar la configuración de MongoDB dentro de Flask,
- exponer colecciones desde la app,
- reducir código de conexión manual.

#### En el código actual
Está instalada pero no utilizada todavía.

---

## Estructura del proyecto

```text
photo_app/
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

### Archivos y carpetas relacionadas con la app
Además de la carpeta `photo_app/`, el proyecto usa estas rutas en la raíz:

```text
templates/
static/
uploads/
```

### `templates/`
Contiene las vistas HTML de la app:
- `login.html`
- `register.html`
- `recover.html`
- `reset.html`
- `dashboard.html`

### `static/`
Contiene archivos estáticos, como estilos CSS.

### `uploads/`
Carpeta donde se guardan los archivos subidos por usuarios autenticados.

---

## Dependencias declaradas en `pyproject.toml`

```toml
dependencies = [
    "email-validator>=2.3.0",
    "flask>=3.1.3",
    "flask-pymongo>=3.0.1",
    "pymongo>=4.17.0",
    "werkzeug>=3.1.8",
]
```

### Qué aporta cada una

- **flask**: servidor web, rutas, plantillas, sesiones.
- **werkzeug**: seguridad de contraseñas y sanitización de nombres.
- **email-validator**: validación de emails.
- **pymongo**: conexión a MongoDB.
- **flask-pymongo**: integración Flask + MongoDB.

---

## Configuración principal de `main.py`

### Variables globales

#### Rutas de carpetas
- `BASE_DIR`: carpeta `photo_app/`
- `ROOT_DIR`: raíz del proyecto
- `TEMPLATES_DIR`: carpeta `templates/`
- `STATIC_DIR`: carpeta `static/`
- `UPLOAD_DIR`: carpeta `uploads/`

#### Categorías disponibles
```python
CATEGORIES = ["Fotos", "Videos", "Links", "Archivos"]
```

Estas categorías se usan para clasificar contenido en el dashboard.

#### Instancia Flask
```python
app = Flask(...)
```

Se inicializa con:
- `template_folder` apuntando a `templates/`
- `static_folder` apuntando a `static/`

#### Clave secreta
```python
app.secret_key = os.environ.get("SECRET_KEY", "photo-app-dev-secret")
```

Se usa para firmar sesiones de Flask.

#### Configuración de subida
```python
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)
```

#### Almacenamiento en memoria
```python
users: dict[str, dict[str, str]] = {}
reset_tokens: dict[str, str] = {}
file_records: list[dict[str, Any]] = []
```

---

## Funciones internas

### `ensure_directories()`
Crea las carpetas necesarias para estilos y uploads.

#### Responsabilidad
Asegurar que existan:
- `static/`
- `uploads/`

#### Cuándo se ejecuta
Se llama al cargar el módulo.

---

### `normalize_email(raw_email: str) -> str`
Normaliza y valida un correo.

#### Hace lo siguiente
- elimina espacios,
- convierte a minúsculas,
- valida formato básico con regex,
- lanza `ValueError` si el correo no es válido.

#### Uso
Se utiliza en:
- registro,
- login,
- recuperación de contraseña.

---

### `get_current_user() -> str | None`
Devuelve el usuario actual desde la sesión.

#### Retorna
- correo del usuario si existe sesión,
- `None` si no hay sesión activa.

---

### `login_required(view)`
Decorador que protege rutas privadas.

#### Comportamiento
- si no hay sesión, redirige a `/login`,
- si hay sesión, ejecuta la vista normal.

#### Se usa en
- `/dashboard`
- `/index`
- `/uploads/<path:filename>`
- `/upload`
- `/delete/<path:filename>`
- `/delete_link/<link_id>`

---

### `build_dashboard_context(user_email: str) -> dict[str, Any]`
Construye los datos que se envían al dashboard.

#### Hace lo siguiente
- filtra `file_records` por propietario,
- devuelve categorías y archivos del usuario.

#### Retorna
Un diccionario con:
- `categories`
- `files`

---

### `infer_file_category(content_type: str | None, filename: str) -> str`
Infiera una categoría según el MIME type o la extensión.

#### Reglas
- imágenes → `Fotos`
- videos → `Videos`
- PDFs → `Archivos`
- lo demás → `Archivos`

---

### `infer_file_type(content_type: str | None, filename: str) -> str`
Infiera el tipo técnico del archivo.

#### Retorna
- `image`
- `video`
- `pdf`
- `file`

---

## Rutas de la aplicación

### `GET /`
#### Función
`home()`

#### Comportamiento
- si el usuario está autenticado, redirige a `/dashboard`
- si no, redirige a `/login`

---

### `GET /favicon.ico`
#### Función
`favicon()`

#### Comportamiento
Sirve el favicon desde la carpeta `static/`.

---

### `GET /register`
### `POST /register`
#### Función
`register()`

#### GET
Muestra el formulario de registro.

#### POST
- lee `email` y `password`,
- normaliza el correo,
- valida longitud mínima de contraseña,
- evita correos repetidos,
- guarda el usuario en memoria con contraseña hasheada,
- redirige al login con mensaje de éxito.

#### Errores manejados
- correo inválido,
- contraseña muy corta,
- correo ya registrado.

---

### `GET /login`
### `POST /login`
#### Función
`login()`

#### GET
Renderiza el formulario de acceso.

#### POST
- valida correo,
- busca el usuario en `users`,
- compara contraseña con `check_password_hash`,
- guarda `session["user"]`,
- redirige al dashboard.

#### Errores manejados
- correo inválido,
- credenciales incorrectas.

---

### `GET /logout`
#### Función
`logout()`

#### Comportamiento
- elimina `user` de la sesión,
- redirige al login con mensaje de cierre de sesión.

---

### `GET /recover`
### `POST /recover`
#### Función
`recover()`

#### POST
- valida el correo,
- si el usuario existe, genera un token seguro,
- guarda el token en `reset_tokens`,
- construye un enlace de restablecimiento con `url_for(..., _external=True)`.

#### Si el correo no existe
No revela información sensible; muestra un mensaje genérico.

---

### `GET /reset/<token>`
### `POST /reset/<token>`
#### Función
`reset_password(token: str)`

#### Comportamiento
- busca el token en `reset_tokens`,
- si no existe, responde 404,
- si existe y se envía POST:
  - valida nueva contraseña,
  - actualiza el hash en `users`,
  - elimina el token usado,
  - redirige al login.

#### Errores manejados
- token inválido o expirado,
- contraseña demasiado corta.

---

### `GET /dashboard`
#### Función
`dashboard()`

#### Requiere
Sesión activa.

#### Comportamiento
- obtiene el usuario actual,
- construye el contexto del dashboard,
- pasa `message` y `error` desde query params,
- renderiza `dashboard.html`.

---

### `GET /index`
#### Función
`index()`

#### Comportamiento
Redirige a `/dashboard`.

#### Motivo
Actúa como alias de navegación.

---

### `GET /uploads/<path:filename>`
#### Función
`uploaded_file(filename: str)`

#### Comportamiento
Sirve archivos subidos desde `UPLOAD_FOLDER`.

#### Requiere
Sesión activa.

---

### `POST /upload`
#### Función
`upload_file()`

#### Comportamiento
Permite dos modos:

1. **Subir un archivo**
   - toma el archivo desde `request.files["file"]`,
   - limpia el nombre con `secure_filename`,
   - lo guarda en `uploads/`,
   - agrega un registro a `file_records`,
   - asigna tipo y categoría.

2. **Guardar un enlace**
   - toma el valor desde `request.form["url"]`,
   - crea un registro tipo `link`,
   - lo clasifica en `Links`.

#### Validaciones
- categoría inválida → usa `Archivos`
- archivo sin nombre válido → redirige con error
- falta archivo y URL → redirige con error

---

### `POST /delete/<path:filename>`
#### Función
`delete_file(filename: str)`

#### Comportamiento
- elimina el registro del archivo si pertenece al usuario actual,
- borra el archivo físico del directorio `uploads/`,
- actualiza `file_records`,
- responde con mensaje de éxito o no encontrado.

---

### `POST /delete_link/<link_id>`
#### Función
`delete_link(link_id: str)`

#### Comportamiento
- elimina un enlace por `_id`,
- solo si pertenece al usuario autenticado,
- actualiza `file_records`,
- redirige con mensaje.

---

## Flujo completo de uso

### Registro
1. El usuario abre `/register`.
2. Envía correo y contraseña.
3. El sistema valida el formato del correo.
4. La contraseña se guarda con hash.
5. La cuenta queda disponible para iniciar sesión.

### Inicio de sesión
1. El usuario abre `/login`.
2. Envía credenciales.
3. Flask valida usuario y contraseña.
4. Se guarda la sesión en `session["user"]`.
5. El usuario entra al dashboard.

### Recuperación de contraseña
1. El usuario abre `/recover`.
2. Envía su correo.
3. El sistema genera un token temporal.
4. Se construye un enlace `/reset/<token>`.
5. Se actualiza la contraseña con el formulario de restablecimiento.

### Subida de archivos
1. El usuario autenticado abre el dashboard.
2. Sube un archivo o pega una URL.
3. El sistema guarda el registro.
4. El contenido aparece organizado por categorías.

### Eliminación
1. El usuario pulsa eliminar.
2. Se valida propiedad del archivo o enlace.
3. Se elimina el archivo físico o el registro correspondiente.

---

## Variables de entorno útiles

### `SECRET_KEY`
Clave secreta para sesiones de Flask.

#### Ejemplo
```bash
SECRET_KEY=una-clave-segura
```

### `PORT`
Puerto donde corre la aplicación.

#### Valor por defecto
`5000`

### `FLASK_DEBUG`
Activa o desactiva modo debug.

#### Valores
- `1` → debug activado
- `0` → debug desactivado

---

## Ejecución

### Instalar dependencias
```bash
uv sync
```

### Ejecutar la app
```bash
python main.py
```

### Abrir en el navegador
La aplicación corre por defecto en:

```text
http://localhost:5000
```

---

## Estado actual

### Implementado
- autenticación básica en memoria,
- registro y login,
- recuperación de contraseña con token,
- dashboard privado,
- subida de archivos,
- guardado de enlaces,
- eliminación de recursos,
- validación básica de correo y contraseña,
- uso de hashes para contraseñas,
- sanitización de nombres de archivo.

### Pendiente de mejorar
- persistencia real en MongoDB,
- expiración de tokens,
- validación más robusta de email,
- limpieza automática de archivos huérfanos,
- paginación del dashboard,
- manejo de errores más detallado,
- separación del código en módulos,
- pruebas automatizadas,
- documentación de plantillas y estilos.

---

## Observaciones técnicas importantes

- El almacenamiento de usuarios y archivos es temporal.
- Los datos se pierden al reiniciar el proceso.
- `email-validator` está declarado pero no se usa aún en el código.
- El proyecto está listo para migrar a una arquitectura con base de datos real.
- El uso de `secure_filename` reduce riesgos al guardar archivos.
- Las contraseñas nunca se guardan en texto plano.

---

## Próximos pasos recomendados

Si quieres seguir documentando el proyecto, los siguientes pasos serían:

1. documentar cada plantilla HTML,
2. documentar el CSS y las clases principales,
3. extraer rutas a módulos separados,
4. integrar MongoDB real,
5. añadir ejemplos de requests y responses,
6. incluir capturas o diagramas del flujo de usuario.

---

## Licencia

Aún no se ha definido una licencia en el repositorio.
