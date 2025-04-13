from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        
        if username == 'test' and password == 'password':
            flash('Login exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales inválidas', 'danger')
    
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
    
        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')