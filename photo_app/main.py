from __future__ import annotations

import mimetypes
import os
import re
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
from pathlib import Path
from typing import Any

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
TEMPLATES_DIR = ROOT_DIR / "templates"
STATIC_DIR = ROOT_DIR / "static"
UPLOAD_DIR = ROOT_DIR / "uploads"

CATEGORIES = ["Fotos", "Videos", "Links", "Archivos"]

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR),
)
app.secret_key = os.environ.get("SECRET_KEY", "photo-app-dev-secret")
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)

app.config["SMTP_SERVER"] = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
app.config["SMTP_PORT"] = int(os.environ.get("SMTP_PORT", "587"))
app.config["SMTP_USERNAME"] = os.environ.get("SMTP_USERNAME", "tu_correo@gmail.com")
app.config["SMTP_PASSWORD"] = os.environ.get("SMTP_PASSWORD", "tu_contraseña_de_aplicacion")

users: dict[str, dict[str, str]] = {}
reset_tokens: dict[str, str] = {}
file_records: list[dict[str, Any]] = []


def ensure_directories() -> None:
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def normalize_email(raw_email: str) -> str:
    email = raw_email.strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValueError("invalid email")
    return email


def get_current_user() -> str | None:
    return session.get("user")


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not get_current_user():
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapper


def build_dashboard_context(user_email: str) -> dict[str, Any]:
    user_files = [record for record in file_records if record["owner"] == user_email]
    return {
        "categories": CATEGORIES,
        "files": user_files,
    }


def infer_file_category(content_type: str | None, filename: str) -> str:
    mime_type = (content_type or mimetypes.guess_type(filename)[0] or "").lower()
    if mime_type.startswith("image/"):
        return "Fotos"
    if mime_type.startswith("video/"):
        return "Videos"
    if mime_type in {"application/pdf"}:
        return "Archivos"
    return "Archivos"


def infer_file_type(content_type: str | None, filename: str) -> str:
    mime_type = (content_type or mimetypes.guess_type(filename)[0] or "").lower()
    if mime_type.startswith("image/"):
        return "image"
    if mime_type.startswith("video/"):
        return "video"
    if mime_type == "application/pdf":
        return "pdf"
    return "file"


def send_recovery_email(target_email: str, reset_link: str) -> bool:
    msg = MIMEMultipart()
    msg["From"] = app.config["SMTP_USERNAME"]
    msg["To"] = target_email
    msg["Subject"] = "Restablece tu contraseña - Vault App"

    html = f"""
    <html>
        <body style="font-family: sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
                <h2 style="color: #4A90E2;">Restablecer contraseña</h2>
                <p>Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace para continuar:</p>
                <p style="margin: 25px 0;">
                    <a href="{reset_link}" style="background-color: #4A90E2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                        Restablecer Contraseña
                    </a>
                </p>
                <p style="font-size: 12px; color: #777;">Si no solicitaste esto, puedes ignorar este correo de forma segura.</p>
                <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="font-size: 11px; color: #aaa;">Si el botón no funciona, copia y pega este enlace en tu navegador:<br>{reset_link}</p>
            </div>
        </body>
    </html>
    """
    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP(app.config["SMTP_SERVER"], app.config["SMTP_PORT"])
        server.starttls()
        server.login(app.config["SMTP_USERNAME"], app.config["SMTP_PASSWORD"])
        server.sendmail(app.config["SMTP_USERNAME"], target_email, msg.as_string())
        server.quit()
        return True
    except Exception:
        return False


@app.route("/")
def home():
    if get_current_user():
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(STATIC_DIR, "favicon.ico")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        raw_email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        try:
            email = normalize_email(raw_email)
        except ValueError:
            return render_template(
                "register.html",
                error="Ingresa un correo válido.",
                email=raw_email,
            )

        if len(password) < 6:
            return render_template(
                "register.html",
                error="La contraseña debe tener al menos 6 caracteres.",
                email=email,
            )

        if email in users:
            return render_template(
                "register.html",
                error="Ese correo ya está registrado.",
                email=email,
            )

        users[email] = {
            "email": email,
            "password": generate_password_hash(password),
        }
        return redirect(url_for("login", message="Cuenta creada. Ya puedes iniciar sesión."))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        raw_email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        try:
            email = normalize_email(raw_email)
        except ValueError:
            return render_template(
                "login.html",
                error="Ingresa un correo válido.",
                email=raw_email,
            )

        user = users.get(email)
        if not user or not check_password_hash(user["password"], password):
            return render_template(
                "login.html",
                error="Correo o contraseña incorrectos.",
                email=email,
            )

        session["user"] = email
        return redirect(url_for("dashboard"))

    message = request.args.get("message")
    return render_template("login.html", message=message)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login", message="Sesión cerrada correctamente."))


@app.route("/recover", methods=["GET", "POST"])
def recover():
    if request.method == "POST":
        raw_email = request.form.get("email", "").strip()

        try:
            email = normalize_email(raw_email)
        except ValueError:
            return render_template(
                "recover.html",
                error="Ingresa un correo válido.",
                email=raw_email,
            )

        if email in users:
            token = secrets.token_urlsafe(24)
            reset_tokens[token] = email
            reset_link = url_for("reset_password", token=token, _external=True)
            send_recovery_email(email, reset_link)

        return render_template(
            "recover.html",
            message="Si el correo está registrado, recibirás un enlace para restablecer tu contraseña en unos minutos.",
            email=email,
        )

    return render_template("recover.html")


@app.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token: str):
    email = reset_tokens.get(token)
    if not email:
        abort(404)

    if request.method == "POST":
        password = request.form.get("password", "").strip()
        if len(password) < 6:
            return render_template(
                "reset.html",
                error="La contraseña debe tener al menos 6 caracteres.",
            )

        users[email]["password"] = generate_password_hash(password)
        reset_tokens.pop(token, None)
        return redirect(url_for("login", message="Contraseña actualizada. Inicia sesión de nuevo."))

    return render_template("reset.html")


@app.route("/dashboard")
@login_required
def dashboard():
    user_email = get_current_user()
    assert user_email is not None
    context = build_dashboard_context(user_email)
    context["message"] = request.args.get("message")
    context["error"] = request.args.get("error")
    return render_template("dashboard.html", **context)


@app.route("/index")
@login_required
def index():
    return redirect(url_for("dashboard"))


@app.route("/uploads/<path:filename>")
@login_required
def uploaded_file(filename: str):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/upload", methods=["POST"])
@login_required
def upload_file():
    user_email = get_current_user()
    assert user_email is not None

    category = request.form.get("category", "Archivos")
    if category not in CATEGORIES:
        category = "Archivos"

    uploaded = request.files.get("file")
    url_value = request.form.get("url", "").strip()

    if uploaded and uploaded.filename:
        filename = secure_filename(uploaded.filename)
        if not filename:
            return redirect(url_for("dashboard", error="El archivo no tiene un nombre válido."))
        destination = UPLOAD_DIR / filename
        uploaded.save(destination)
        file_records.append(
            {
                "_id": secrets.token_urlsafe(12),
                "owner": user_email,
                "filename": filename,
                "url": "",
                "type": infer_file_type(uploaded.content_type, filename),
                "category": category if category != "Links" else infer_file_category(uploaded.content_type, filename),
            }
        )
        return redirect(url_for("dashboard", message="Archivo subido correctamente."))

    if url_value:
        file_records.append(
            {
                "_id": secrets.token_urlsafe(12),
                "owner": user_email,
                "filename": "",
                "url": url_value,
                "type": "link",
                "category": "Links",
            }
        )
        return redirect(url_for("dashboard", message="Enlace guardado correctamente."))

    return redirect(url_for("dashboard", error="Debes subir un archivo o pegar una URL."))


@app.route("/delete/<path:filename>", methods=["POST"])
@login_required
def delete_file(filename: str):
    user_email = get_current_user()
    assert user_email is not None

    remaining: list[dict[str, Any]] = []
    removed = False

    for record in file_records:
        if record["owner"] == user_email and record.get("filename") == filename and record.get("type") != "link":
            removed = True
            file_path = UPLOAD_DIR / filename
            if file_path.exists():
                file_path.unlink()
            continue
            remaining.append(record)

    file_records[:] = remaining
    return redirect(url_for("dashboard", message="Archivo eliminado." if removed else "No se encontró el archivo."))


@app.route("/delete_link/<link_id>", methods=["POST"])
@login_required
def delete_link(link_id: str):
    user_email = get_current_user()
    assert user_email is not None

    remaining: list[dict[str, Any]] = []
    removed = False

    for record in file_records:
        if record["owner"] == user_email and record.get("_id") == link_id and record.get("type") == "link":
            removed = True
            continue
        remaining.append(record)

    file_records[:] = remaining
    return redirect(url_for("dashboard", message="Enlace eliminado." if removed else "No se encontró el enlace."))


ensure_directories()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG", "0") == "1")
