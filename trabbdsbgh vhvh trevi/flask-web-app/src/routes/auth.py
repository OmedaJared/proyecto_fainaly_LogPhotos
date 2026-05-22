from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import os

auth_bp = Blueprint('auth', __name__)

# Configuración de MongoDB: usa tu URI real o local
mongo_client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017/photo_db"))
mongo_db = mongo_client["photo_db"]

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'])
        mongo_db.users.insert_one({
            "email": request.form['email'],
            "password": hashed_pw
        })
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    message = request.args.get('message')
    if request.method == 'POST':
        user = mongo_db.users.find_one({"email": request.form['email']})
        if user and check_password_hash(user['password'], request.form['password']):
            session['user'] = user['email']
            return redirect(url_for('index'))
    return render_template('login.html', message=message)

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))