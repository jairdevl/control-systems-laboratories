# Import libraries
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from datetime import datetime
import mysql.connector
from io import BytesIO
import pandas as pd
import secrets
import re

# New instace Flask
app = Flask(__name__)

# Settings database
app.config["MYSQL_HOST"] = "localhost"  
app.config["MYSQL_USER"] = "root"        
app.config["MYSQL_PASSWORD"] = "whoami"  
app.config["MYSQL_DB"] = "database"         
app.config["SECRET_KEY"] = secrets.token_hex(16)

# Connection database
cnx = mysql.connector.connect(
    host=app.config["MYSQL_HOST"],         
    user=app.config["MYSQL_USER"],         
    password=app.config["MYSQL_PASSWORD"], 
    database=app.config["MYSQL_DB"],        
    charset='utf8mb4',                       
    collation='utf8mb4_unicode_ci'         
)

# Create table database
cursor = cnx.cursor()
query = """
CREATE TABLE IF NOT EXISTS control_aulas_sistemas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_registro DATETIME,
    identificador_aula VARCHAR(255),
    nombre_docente VARCHAR(255),
    correo_electronico VARCHAR(255),
    programa VARCHAR(255),
    hora_ingreso TIME,
    hora_salida TIME,
    observaciones TEXT,
    respuesta_incidencias TEXT
)
"""
cursor.execute(query)
cnx.commit()

# Create table database
cursor = cnx.cursor()
query = """
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    hash VARCHAR(255) NOT NULL
)
"""
cursor.execute(query)
cnx.commit()

# Define routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_data", methods=['POST'])
def add_data():
    form_data = {
        'identificador_aula': request.form.get('identificador_aula'),
        'nombre_docente': request.form.get('nombre_docente'),
        'correo_electronico': request.form.get('correo_electronico'),
        'programa': request.form.get('programa'),
        'hora_ingreso': request.form.get('hora_ingreso'),
        'hora_salida': request.form.get('hora_salida'),
        'observaciones': request.form.get('observaciones')
    }
    try:
        # Get form data
        fecha_registro = datetime.now().strftime('%Y-%m-%d')
        # Form fields validation
        if not all(form_data.values()):
            flash("Todos los campos son obligatorios.", category='warning')
            return render_template('index.html', form_data=form_data)
        if not re.match(r"^[A-Za-z\s]+$", form_data['nombre_docente']):
            flash("El nombre del docente solo puede contener letras y espacios.", category='warning')
            return render_template('index.html', form_data=form_data)
        if not re.match(r"^[^,\s]+@(gmail\.com|unicesmag\.edu\.co)$", form_data['correo_electronico']):
            flash("Correo electrónico no válido. Debe ser un correo de Gmail o de la universidad.", category='warning')
            return render_template('index.html', form_data=form_data)
        if form_data['hora_ingreso'] >= form_data['hora_salida']:
            flash("La hora de salida debe ser después de la hora de ingreso.", category='warning')
            return render_template('index.html', form_data=form_data)
        # Save data to database
        cursor = cnx.cursor()
        query = """
        INSERT INTO control_aulas_sistemas (fecha_registro, identificador_aula, nombre_docente, correo_electronico, programa, hora_ingreso, hora_salida, observaciones)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (fecha_registro, *form_data.values()))
        cnx.commit()
        flash("Datos guardados exitosamente.", category='success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Error: {e}", category='danger')
        return render_template('index.html', form_data=form_data)
 
@app.route("/login", methods=["GET", "POST"])
def login_admin():
    # Clean session exising
    session.clear() 
    # Check if then from is submitted
    if request.method == "POST": 
        input_username = request.form.get("username") 
        input_password = request.form.get("password") 
        # Validate field input
        if not input_username:
            return render_template("login.html", messager=1) 
        elif not input_password:
            return render_template("login.html", messager=2) 
        # Create cursor to return dictionary 
        cursor = cnx.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (input_username,))
        user = cursor.fetchone()
        # Validate credencials user
        if user is None or not check_password_hash(user["hash"], input_password):
            return render_template("login.html", messager=3)
        session["user_id"] = user["id"] 
        return redirect("/admin") 
    return render_template("/login.html")

@app.route("/goback")
@login_required
def goback():
    return redirect("/admin")

@app.route("/admin")
@login_required
def admin_data():
    cursor = cnx.cursor()
    # Select table database
    cursor.execute('SELECT * FROM control_aulas_sistemas')
    data = cursor.fetchall()
    return render_template("/admin.html", data = data)

@app.route("/edit/<id>")
@login_required
def get_data(id):
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM control_aulas_sistemas WHERE id = %s',(id,))
    data = cursor.fetchall()
    return render_template("edit.html", id = data[0])

@app.route("/update/<id>", methods = ['POST'])
@login_required
def update_data(id):
    if request.method == 'POST':
        # Get updated form data
        fecha_registro = request.form['fecha_registro']
        identificador_aula = request.form['identificador_aula']
        nombre_docente = request.form['nombre_docente']
        correo_electronico = request.form['correo_electronico']
        programa = request.form["programa"]
        hora_ingreso = request.form['hora_ingreso']
        hora_salida = request.form['hora_salida']
        observaciones = request.form['observaciones']
        respuesta_incidencias = request.form['respuesta_incidencias']
        # Update data in database
        cursor = cnx.cursor()
        query = """
            UPDATE control_aulas_sistemas
            SET fecha_registro = %s,
                identificador_aula = %s,
                nombre_docente = %s,
                correo_electronico = %s,
                programa = %s,
                hora_ingreso = %s,
                hora_salida = %s,
                observaciones = %s,
                respuesta_incidencias = %s
            WHERE id = %s
            """
        cursor.execute(query, (fecha_registro, identificador_aula, nombre_docente, correo_electronico, programa, hora_ingreso, hora_salida, observaciones, respuesta_incidencias, id))
        cnx.commit()
        flash('Datos actualizados exitosamente.')
        return redirect(url_for('admin_data'))

@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = cnx.cursor()
    # Delete data form
    cursor.execute('DELETE FROM control_aulas_sistemas WHERE id = {0}'.format(id))
    cnx.commit()
    flash("Datos eliminados correctamente.")
    return redirect(url_for('admin_data'))

@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":
        # Get data user
        input_username = request.form.get("username")
        input_password = request.form.get("password")
        input_confirmation = request.form.get("confirmation")
        # Validate data user
        if not input_username:
            return render_template("register.html", messager=1)
        elif not input_password:
            return render_template("register.html", messager=2)
        elif not input_confirmation:
            return render_template("register.html", messager=4)
        elif input_password != input_confirmation:
            return render_template("register.html", messager=3)
        # Create cursor database
        cursor = cnx.cursor()
        cursor.execute('SELECT username FROM users WHERE username = %s', (input_username,))
        if cursor.fetchone():
            return render_template("register.html", messager=5)
        # Generate hashed password
        hash_password = generate_password_hash(input_password, method='pbkdf2:sha256', salt_length=8)
        cursor.execute('INSERT INTO users (username, hash) VALUES (%s, %s)', (input_username, hash_password))
        cnx.commit()
        new_user_id = cursor.lastrowid
        # Saving id user
        session["user_id"] = new_user_id
        flash(f"Usuario registrado como {input_username}")
        return redirect("/admin")
    return render_template("register.html")

@app.route("/users")
@login_required
def users():
    cursor = cnx.cursor()
    # Select table users
    cursor.execute('SELECT * FROM users')
    data = cursor.fetchall()
    return render_template("/users.html", data=data)

@app.route("/restore/<id>", methods=['GET', 'POST'])
@login_required
def restore(id):
    cursor = cnx.cursor()
    # Get form restore
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        # Initialize message variable
        message_code = 0
        # Get the current username from the database to keep it unchanged
        cursor.execute("SELECT username FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
        current_username = user[0] if user else ''
        # Validate passwords
        if not new_password:
            message_code = 2  # Password is empty
        elif new_password != confirmation:
            message_code = 3  # Passwords do not match
        else:
            # Generate hash for new password
            hash_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)
            cursor.execute("UPDATE users SET hash = %s WHERE id = %s", (hash_password, id))
        # Commit changes only if there are no validation errors
        if message_code == 0:
            cnx.commit()
            flash("Datos actualizados exitosamente.")
            return redirect("/users")
        # Render template with appropriate message and current username
        return render_template("restore.html", messager=message_code, id=id, username=current_username)
    # Get data user form
    cursor.execute("SELECT username FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    username = user[0] if user else ''
    return render_template("restore.html", messager=0, id=id, username=username)

@app.route("/deleteuser/<id>")
@login_required
def deleteuser(id):
    cursor = cnx.cursor()
    # Detele user database
    cursor.execute('DELETE FROM users WHERE id = %s', (id,))
    cnx.commit()
    flash("Usuario eliminado correctamente.")
    return redirect("/users")

@app.route("/reports", methods=['GET'])
@login_required
def reports():
    # Render template reports
    return render_template("/reports.html")
"""
@app.route("/generate", methods=['GET', 'POST'])
@login_required
def generate():
    # Create cursor database 
    cursor = cnx.cursor()
     # Check if the request method is POST
    if request.method == 'POST':
        start_end = request.form['start_date']
        end_date = request.form['end_date']
        cursor.execute('SELECT * FROM control_aulas_sistemas WHERE fecha_registro BETWEEN %s AND %s', (start_end, end_date))
    else:
        # If the request method is GET retrieve all records from the table
        cursor.execute('SELECT * FROM control_aulas_sistemas')
    # Get results store in date
    data = cursor.fetchall()
    return render_template("/generate.html", data = data)
"""


@app.route("/logout")
@login_required
def logout():
    # Clean session
    session.clear() 
    return redirect("/")

# Inicialize web
if __name__ == "__main__":
    app.run(debug=True, port=5014)