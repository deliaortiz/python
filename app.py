from flask import Flask, render_template, request, redirect, url_for, session
from db_connection import get_db_connection
import mysql.conector
import hashlib

app = Flask(__name__)
app.secret_key = 'mi_secreto'

@app.route('/')
def home ():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'usernanme' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO users (username, password)VALUES(%s,%s)"
        try:
            cursor.execute(query, (username, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return f"Error: {err}"
        
    return render_template('register.html')

@app.route('/login', methods = ['POST'])
def login():
    if request.methods == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query,(username, hashed_password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Usuario o contraseña incorrectos"
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)