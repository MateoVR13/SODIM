from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Implementa la lógica para la autenticación
        username = request.form['username']
        password = request.form['password']
        
        # Aquí podrías agregar la validación con la base de datos
        if username == 'test' and password == 'password':  # Esto es solo un ejemplo
            flash('Login exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales inválidas', 'danger')
    
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Implementa la lógica para el registro
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Aquí agregarías la lógica para insertar el nuevo usuario en la base de datos
        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('auth.login'))  # Redirigir a login después del registro
    
    return render_template('register.html')

# Asegúrate de registrar estas rutas en __init__.py
