<img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/c0d03a49-ac75-427a-b40d-f951669b60ee" />
Olmeda Castillo Jared Fernando
24308060610036@cetis61.edu.mx
<img width="250" height="250" alt="image" src="https://github.com/user-attachments/assets/1150920d-610d-4e32-a4d4-492558223228" />
Almanza Garcia Dylan Kareem
24308060610588@cetis61.edu.mx

Sistema de Autenticación

Este proyecto es un sistema básico de inicio de sesión, registro y recuperación de contraseña usando Flask y MongoDB Atlas.

## Para qué sirve cada librería

- `flask`
  - Framework principal para crear la aplicación web.
  - Maneja rutas, renderizado de plantillas y servidor local.

- `flask-login`
  - Administra el inicio de sesión de usuarios.
  - Controla sesiones, protección de rutas y estados de usuario autenticado.

- `flask-wtf`
  - Proporciona integración de formularios con Flask.
  - Maneja validación de formularios y protección CSRF.

- `wtforms`
  - Define los campos de formulario y las reglas de validación.
  - Se usa para crear los formularios de login, registro y reset.

- `pymongo`
  - Conecta la aplicación a MongoDB.
  - Permite leer y escribir datos de usuarios en la base de datos.

- `bcrypt`
  - Encripta las contraseñas antes de guardarlas en la base de datos.
  - Verifica contraseñas de forma segura.

- `flask-mail`
  - Envía correos electrónicos desde Flask.
  - Se usa para enviar enlaces de recuperación de contraseña.

- `python-dotenv`
  - Carga variables de entorno desde el archivo `.env`.
  - Permite mantener claves y configuraciones fuera del código.

- `dnspython`
  - Dependencia de `pymongo` para resolver URIs `mongodb+srv`.

## Explicación de `app.py`

### Configuración inicial

- `load_dotenv()`
  - Carga las variables del archivo `.env`.

- `app = Flask(__name__)`
  - Crea la aplicación Flask.

- `app.config[...]`
  - Configura la clave secreta, correo y otros ajustes.

### Configuración de `Mail` y `LoginManager`

- `mail = Mail(app)`
  - Inicializa el envío de correos.

- `login_manager = LoginManager()`
  - Configura la lógica de login.

- `login_manager.login_view = 'login'`
  - Define la página de redirección cuando el usuario no está autenticado.

### Conexión a MongoDB

- `mongo_uri = os.getenv('MONGO_URI')`
  - Lee la cadena de conexión desde `.env`.

- `MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)`
  - Intenta conectarse a MongoDB en 5 segundos.

- `client.admin.command('ping')`
  - Verifica que la conexión esté activa.

- Si el URI es un placeholder, el código usa un fallback local:
  - `mongodb://localhost:27017/trevi3`

- `db = client['trevi3']`
  - Selecciona la base de datos `trevi3`.

- `users_collection = db['users']`
  - Colección para guardar usuarios.

- `reset_tokens_collection = db['reset_tokens']`
  - Colección para guardar tokens de recuperación.

### Clase `User`

- `class User(UserMixin):`
  - Define el usuario que usa Flask-Login.

- `self.id = str(user_data['_id'])`
  - Usa el `_id` de MongoDB como identificador.

- `self.email = user_data['email']`
  - Guarda el email para mostrarlo y verificarlo.

### Función `load_user`

- `@login_manager.user_loader`
  - Carga el usuario desde la sesión.

- Busca el usuario en MongoDB por `_id`.

### Formularios

- `LoginForm`
  - Campos: `email`, `password`, `submit`.
  - Valida que el email y la contraseña existan.

- `RegisterForm`
  - Campos: `email`, `password`, `confirm_password`, `submit`.
  - Valida contraseña mínima y coincidencia.

- `ResetForm`
  - Campo: `email`.
  - Envía la solicitud de recuperación.

- `ResetPasswordForm`
  - Campos: `password`, `confirm_password`, `submit`.
  - Permite establecer nueva contraseña.

### Rutas

- `/` - `home()`
  - Ruta protegida con `@login_required`.
  - Muestra la página principal después de iniciar sesión.

- `/login` - `login()`
  - Muestra el formulario de login.
  - Si los datos son correctos, autentica y redirige a `/`.
  - Usa `checkpw()` de `bcrypt` para verificar la contraseña.

- `/register` - `register()`
  - Muestra formulario de registro.
  - Verifica que el email no exista.
  - Hashea la contraseña con `hashpw()` y la guarda en MongoDB.

- `/reset` - `reset()`
  - Muestra el formulario de recuperación.
  - Si el email existe, crea un token único.
  - Envía un correo con el enlace de recuperación.

- `/reset/<token>` - `reset_password(token)`
  - Verifica que el token exista.
  - Permite guardar la nueva contraseña.
  - Borra el token después de usarlo.

- `/logout` - `logout()`
  - Cierra la sesión del usuario.
  - Redirige a la página de login.

## Archivos de plantillas

- `templates/base.html`
  - Plantilla base común para todas las páginas.

- `templates/login.html`
  - Formulario de inicio de sesión.

- `templates/register.html`
  - Formulario de registro de usuario.

- `templates/reset.html`
  - Formulario para pedir el enlace de recuperación.

- `templates/reset_password.html`
  - Formulario para escribir la nueva contraseña.

- `templates/home.html`
  - Página principal para usuarios autenticados.

## Cómo ejecutar

1. Abre la terminal en la carpeta del proyecto.
2. Activa el entorno virtual:
   - `& ".venv\Scripts\Activate.ps1"`
3. Ejecuta la aplicación:
   - `uv run flask run`
4. Abre `http://127.0.0.1:5000/` en el navegador.

## Variables de entorno necesarias

- `MONGO_URI` - Cadena de conexión de MongoDB Atlas.
- `SECRET_KEY` - Clave secreta para Flask.
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD` - Configuración de correo.























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
├── main.py          # Lógica principal de la aplicación
├── pyproject.toml   # Configuración de dependencias
├── README.md        # Documentación
├── uv.lock          # Bloqueo de versiones
├── templates/       # Vistas HTML
├── static/          # Archivos CSS/JS
├── uploads/         # Archivos subidos por usuarios
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












# photo-app

`photo-app` es una aplicación web funcional desarrollada con Flask que permite la gestión de archivos y enlaces organizados por categorías, con un sistema completo de usuarios.

---

## Resumen del proyecto

El archivo `main.py` ya no es un punto de entrada básico, sino que implementa toda la lógica del servidor web. Actualmente, el proyecto permite:

- **Autenticación completa**: Registro, inicio y cierre de sesión de usuarios.
- **Seguridad**: Hasheo de contraseñas con Werkzeug.
- **Recuperación de cuenta**: Sistema de restablecimiento de contraseña mediante envío de correos electrónicos (SMTP).
- **Gestión de archivos**: Subida de archivos físicos y guardado de enlaces URL.
- **Categorización automática**: Clasificación de contenido en Fotos, Videos, Links o Archivos según su tipo MIME.

- aplicación web con Flask,
- validación de correos,
- persistencia con MongoDB,
- manejo de archivos,
- seguridad de contraseñas con Werkzeug.

Sin embargo, el archivo `main.py` todavía no implementa la lógica de la app web; por ahora solo sirve como entrada básica.

---

## Tecnologías y librerías instaladas

Las dependencias definidas en `photo_app/pyproject.toml` son las siguientes:

### 1. `flask>=3.1.3`
Framework web principal.

#### Para qué sirve
- Crear rutas HTTP.
- Renderizar vistas.
- Manejar solicitudes `GET`, `POST`, etc.
- Gestionar sesiones, cookies y contexto de petición.
- Construir una aplicación web tradicional o una API.

#### Uso típico en este proyecto
Aunque todavía no se usa en `main.py`, está pensada para:
- formularios de login/registro,
- páginas HTML,
- endpoints para subida de archivos,
- recuperación de contraseña,
- manejo de sesión de usuario.

---

### 2. `pymongo>=4.17.0`
Driver oficial de MongoDB para Python.

#### Para qué sirve
- Conectarse a una base de datos MongoDB.
- Insertar documentos.
- Buscar documentos.
- Actualizar registros.
- Eliminar documentos.

#### Uso típico en este proyecto
Está orientada a guardar información como:
- usuarios,
- archivos subidos,
- tokens de recuperación,
- metadatos de contenido.

---

### 3. `flask-pymongo>=3.0.1`
Integración entre Flask y MongoDB.

#### Para qué sirve
- Simplifica el uso de MongoDB dentro de una app Flask.
- Permite configurar la conexión desde la app Flask de forma más limpia.
- Facilita el acceso a colecciones desde la aplicación.

#### Ventaja
Reduce la cantidad de código de conexión manual frente a usar solo `pymongo`.

---

### 4. `werkzeug>=3.1.8`
Biblioteca base usada por Flask.

#### Para qué sirve
- Seguridad de contraseñas con `generate_password_hash` y `check_password_hash`.
- Utilidades para manejo de peticiones y respuestas.
- Manejo de archivos con `secure_filename`.
- Parte interna de la infraestructura de Flask.

#### Uso típico en este proyecto
Ideal para:
- encriptar contraseñas de usuarios,
- validar contraseñas,
- sanitizar nombres de archivo antes de guardarlos.

---

### 5. `email-validator>=2.3.0`
Librería de validación de direcciones de correo electrónico.

#### Para qué sirve
- Verificar si un email tiene formato válido.
- Evitar guardar direcciones mal escritas.
- Mejorar formularios de registro y recuperación de cuenta.

---

## Estructura actual del proyecto

Actualmente los archivos principales son:

```text
photo_app/
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

### `main.py`
Punto de entrada mínimo del proyecto.

### `pyproject.toml`
Archivo de configuración del proyecto y dependencias.

### `README.md`
Documentación del proyecto.

### `uv.lock`
Bloqueo de versiones exactas de dependencias para reproducibilidad.
## Archivo `main.py`

Contenido actual:

```python
def main():
    print("Hello from photo-app!")


if __name__ == "__main__":
    main()
```

### Función `main()`

#### Responsabilidad
Es la función principal del programa.

#### Qué hace
- Imprime en consola el texto `Hello from photo-app!`.

#### Observaciones técnicas
- No recibe parámetros.
- No devuelve nada explícitamente.
- Sirve como base para crecer a una app más completa.
- Hoy funciona como demostración de arranque.

---

### Bloque `if __name__ == "__main__":`

#### Responsabilidad
Permite ejecutar `main()` solo cuando el archivo se corre directamente.

#### Qué significa
- Si ejecutas `python main.py`, se llama a `main()`.
- Si importas `main.py` desde otro módulo, no se ejecuta automáticamente.

#### Beneficio
Es la forma estándar en Python para separar:
- ejecución directa del script,
- reutilización como módulo importable.

---

## Funciones y responsabilidades del código actual

Por ahora, el proyecto tiene una sola función propia:

### `main()`
- Punto de inicio.
- Imprime un mensaje simple.
- No depende de otras partes del proyecto.
- Todavía no inicia servidor web, no conecta a base de datos, y no procesa formularios.

---

## Lo que el proyecto ya está preparado para hacer

Aunque el código visible es mínimo, las dependencias muestran una intención clara de crecimiento hacia una app con estas capacidades:

### Autenticación
- registro de usuarios,
- inicio de sesión,
- hash seguro de contraseñas,
- validación de credenciales.

### Base de datos
- guardar usuarios en MongoDB,
- almacenar metadatos,
- persistir estados de recuperación de cuenta.

### Manejo de archivos
- subir archivos,
- validar nombres de archivo,
- asociar archivos a usuarios.

### Validación de formularios
- comprobar emails,
- validar entradas antes de procesarlas.

---

## Flujo esperado de una futura versión del proyecto

Un flujo lógico para esta base podría ser:

1. El usuario abre la aplicación web.
2. Se muestra una pantalla de registro o login.
3. El sistema valida el correo con `email-validator`.
4. La contraseña se guarda con hash usando `werkzeug`.
5. Los datos del usuario se almacenan en MongoDB.
6. El usuario inicia sesión.
7. Se pueden subir archivos y guardar sus metadatos.
8. La app usa Flask para servir rutas y páginas.

---

## Instalación

### Requisitos
- Python 3.13 o superior
- Acceso a MongoDB si se va a implementar la parte de persistencia
- `uv` o `pip` para gestionar dependencias

### Instalar dependencias
Si usas `uv`:

```bash
uv sync
```

Si usas `pip`:

```bash
pip install flask flask-pymongo pymongo werkzeug email-validator
```

---

## Ejecución

Actualmente, el proyecto solo imprime un mensaje desde consola.

### Ejecutar el script actual
```bash
python main.py
```

### Salida esperada
```text
Hello from photo-app!
```

---

## Convenciones y buenas prácticas observables

### Punto de entrada claro
`main.py` usa el patrón estándar de Python para ejecución directa.

### Configuración centralizada de dependencias
Las librerías se definen en `pyproject.toml`, lo que facilita reproducibilidad.

### Preparación para escalar
Las dependencias instaladas sugieren que el proyecto está pensado para evolucionar hacia una aplicación completa con backend web y base de datos.

---

## Estado actual del código

### Implementado
- Archivo principal con función `main()`
- Gestión moderna de dependencias en `pyproject.toml`
- Dependencias listas para una app Flask + MongoDB

### Aún no implementado
- rutas web,
- plantillas HTML,
- conexión real a MongoDB en el código visible,
- autenticación,
- subida de archivos,
- validación de formularios,
- sistema de emails,
- manejo de sesiones web.

---

## Próximos pasos recomendados


- estructura real de carpetas de la aplicación,
- rutas y funciones de cada módulo,
- variables de entorno necesarias,
- endpoints disponibles,
- ejemplo de uso de MongoDB,
- flujo de autenticación y recuperación de contraseña.

---

## Licencia

Aún no se ha definido una licencia en el contenido actual del proyecto.
