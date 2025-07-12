from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import bcrypt

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
    return render_template('empleados.html')

@app.route('/mostrar_index')
def mostrar_index():
    return render_template('index.html') 

if __name__=='__main__':
    app.run(debug=True)