from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt
import sqlite3
from datetime import datetime

app=Flask(__name__)

engine = create_engine("sqlite:///basedatos.db", echo=True)
tablita=declarative_base()

class Usuario(tablita):
    __tablename__='Usuarios'
    id=Column(Integer, primary_key=True)
    nombre=Column(String(50), nullable=False)
    email=Column(String(50), nullable=False)
    usuario=Column(String(50), nullable=False)
    password=Column(String(100),nullable=False)

tablita.metadata.create_all(engine)

class Empleado(tablita):
    __tablename__="Empleados"
    id=Column(Integer, primary_key=True)
    nombre=Column(String(50), nullable=False)
    cedula=Column(String(50), nullable=False)
    correo=Column(String(50), nullable=False)
    telefono=Column(String(50), nullable=False)
    direccion=Column(String(50), nullable=False)
    salario=Column(String(50), nullable=False)
    horario=Column(String(50), nullable=False)
    fechaingreso=Column(String(50), default=datetime.now().strftime("%Y-%m-%d"))
    
tablita.metadata.create_all(engine)

Session=sessionmaker(bind=engine)
session=Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/administracion', methods=['GET', 'POST'])
def administracion():
    error=None
    if request.method=='POST':
        usuario_input=request.form.get('usuario')
        password_input=request.form.get('password')

        usu=session.query(Usuario).filter_by(usuario=usuario_input).first()

        if usu and bcrypt.checkpw(password_input.encode('utf-8'), usu.password.encode('utf-8')):
            return render_template('administracion.html', nombre=usu.nombre)
        else:
            error = "Usuario o contraseña incorrectos o no estás registrado"
            return render_template('index.html', error=error)
        
    return render_template('administracion.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method=='POST':
        nombre=request.form['nombre']
        email=request.form['email']
        usuarioregis=request.form['usuarioregis']
        clave=request.form['password']

        password_hash=bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        yaexiste=session.query(Usuario).filter_by(email=email).first()
        if yaexiste:
            return "Ya estás registrado."
        else:
            nuevo_usuario = Usuario(
                nombre=nombre,
                email=email,
                usuario=usuarioregis,
                password=password_hash
            )
            session.add(nuevo_usuario)
            session.commit()
            return redirect(url_for('index'))

    return render_template('registro.html')

@app.route('/restablecer_contra.html')
def restablecer_contra():
    return render_template('restablecer_contra.html')

@app.route('/empleados')
def empleados():
    lista_empleados=session.query(Empleado).all()
    return render_template('empleados.html', empleados=lista_empleados)

@app.route('/agregar_empleado', methods=['GET', 'POST'])
def agregar_empleado():
    if request.method=='POST':
        nuevo=Empleado(
            nombre=request.form['nombre'],
            cedula=request.form['cedula'],
            correo=request.form['correo'],
            telefono=request.form['telefono'],
            direccion=request.form['direccion'],
            salario=request.form['salario'],
            horario=request.form['horario'],
            fechaingreso=datetime.now().strftime("%Y-%m-%d")
        )
        session.add(nuevo)
        session.commit()
        print("Empleado guardado:", nuevo.nombre)
        return redirect(url_for('empleados'))
    return render_template('agregar_empleado.html')

@app.route('/editar_empleado')
def editar_empleado():
    return render_template('editar_empleado.html')

@app.route('/mostrar_index')
def mostrar_index():
    return render_template('index.html') 

if __name__=='__main__':
    app.run(debug=True)