from flask import Blueprint, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
import os
from pymongo import MongoClient

files_bp = Blueprint('files', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@files_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@files_bp.route('/upload', methods=['POST'])
def upload_file():
    category = request.form.get('category', 'General')
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    mongo_client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/photo_db"))
    mongo_db = mongo_client["photo_db"]
    mongo_db.files.insert_one({
        "filename": filename,
        "owner": session['user'],
        "type": file.content_type,
        "category": category
    })

    return redirect(url_for('index'))

@files_bp.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    mongo_client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/photo_db"))
    mongo_db = mongo_client["photo_db"]
    file_doc = mongo_db.files.find_one({"filename": filename, "owner": session['user']})
    if file_doc:
        mongo_db.files.delete_one({"_id": file_doc['_id']})
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    return redirect(url_for('index'))

@files_bp.route('/delete_link/<link_id>', methods=['POST'])
def delete_link(link_id):
    from bson import ObjectId
    mongo_client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/photo_db"))
    mongo_db = mongo_client["photo_db"]
    mongo_db.files.delete_one({"_id": ObjectId(link_id), "owner": session['user']})
    return redirect(url_for('index'))