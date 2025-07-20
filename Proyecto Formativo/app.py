from flask import Flask, render_template, request, redirect, url_for, request, session as flask_session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt
import sqlite3
from datetime import datetime
import os

app=Flask(__name__)
app.secret_key=os.urandom(23)

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

class HorasTrabajadas(tablita):
    __tablename__ = "Horas"
    id = Column(Integer, primary_key=True)
    empleado = Column(String(100), nullable=False)
    fecha = Column(String(20), nullable=False)
    horas = Column(Integer, nullable=False)
    actividad = Column(String(200), nullable=False)

tablita.metadata.create_all(engine)

Session=sessionmaker(bind=engine)
session=Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/administracion', methods=['GET', 'POST'])
def administracion():
    nombre=flask_session.get('nombre')
    error=None
    if request.method=='POST':
        usuario_input=request.form.get('usuario')
        password_input=request.form.get('password')

        usu=session.query(Usuario).filter_by(usuario=usuario_input).first()

        if usu and bcrypt.checkpw(password_input.encode('utf-8'), usu.password.encode('utf-8')):
            flask_session['nombre']=usu.nombre
            return render_template('administracion.html', nombre=usu.nombre)
        else:
            error = "Usuario o contraseña incorrectos o no estás registrado"
            return render_template('index.html', error=error)
    
    return render_template('administracion.html', nombre=flask_session.get('nombre'))

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

@app.route('/restablecer_contra.html', methods=['GET', 'POST'])
def restablecer_contra():
    if request.method=='POST':
        email=request.form['email']
        nueva_contra=request.form['password']

        usuario=session.query(Usuario).filter_by(email=email).first()
        
        if not usuario:
            return "Correo no registrado."
        
        nueva_contra_hash=bcrypt.hashpw(nueva_contra.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        usuario.password = nueva_contra_hash
        session.commit()
        
        return redirect(url_for('index'))
    
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
        return redirect(url_for('empleados'))
    
    return render_template('agregar_empleado.html')

@app.route('/editar_empleado/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    empleado = session.query(Empleado).get(id)
    if not empleado:
        return "Empleado no encontrado", 404
    
    if request.method == 'POST':
        empleado.nombre = request.form['nombre']
        empleado.cedula = request.form['cedula']
        empleado.correo = request.form['correo']
        empleado.telefono = request.form['telefono']
        empleado.direccion = request.form['direccion']
        empleado.salario = request.form['salario']
        empleado.horario = request.form['horario']
        
        empleado.fechaingreso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        session.commit()
        return redirect(url_for('empleados'))
    
    return render_template('editar_empleado.html', empleado=empleado)

@app.route('/eliminar_empleado/<int:id>', methods=['POST'])
def eliminar_empleado(id):
    empleado=session.query(Empleado).get(id)
    if empleado:
        session.delete(empleado)
        session.commit()
    return redirect(url_for('empleados'))

@app.route('/horas', methods=['GET', 'POST'])
def horas_trabajadas():
    if request.method == 'POST':
        empleado = request.form['empleado']
        fecha = request.form['fecha']
        horas = request.form['horas']
        actividad = request.form['actividad']

        nueva_hora = HorasTrabajadas(
            empleado=empleado,
            fecha=fecha,
            horas=horas,
            actividad=actividad
        )
        session.add(nueva_hora)
        session.commit()
        return redirect(url_for('horas_trabajadas'))

    horas = session.query(HorasTrabajadas).all()
    return render_template('horas_trabajadas.html', horas=horas)


@app.route('/eliminar_hora', methods=['POST'])
def eliminar_hora():
    id = request.form.get('id')
    if id:
        hora = session.query(HorasTrabajadas).get(int(id))
        if hora:
            session.delete(hora)
            session.commit()
    return redirect(url_for('horas_trabajadas'))

@app.route('/mostrar_index')
def mostrar_index():
    return render_template('index.html') 
    

if __name__=='__main__':
    app.run(debug=True)