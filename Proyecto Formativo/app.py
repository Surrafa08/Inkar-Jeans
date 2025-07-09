from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app=Flask(__name__)

engine = create_engine("sqlite:///basedatos.db", echo=True)
tablita=declarative_base()

class Usuario(tablita):
    __tablename__='Usuarios'
    id=Column(Integer, primary_key=True)
    nombre=Column(String(50), nullable=False)
    email=Column(String(50), nullable=False)
    usuario=Column(String(50), nullable=False)
    password=Column(String(50),nullable=False)

tablita.metadata.create_all(engine)

Session=sessionmaker(bind=engine)
session=Session()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/administracion', methods=['GET', 'POST'])
def administracion():
    if request.method=='POST':
        usuario=request.form.get('usuario')
        password=request.form.get('password')

        if usuario=='admin' and password=='123':
            return render_template('administracion.html')
        else:
            return "Usuario o contraseña incorrectos", 401
    return render_template('administracion.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method=='POST':
        nombre=request.form['nombre']
        email=request.form['email']
        usuario=request.form['usuario']
        password=request.form['password']
        
        yaexiste=session.query(Usuario).filter_by(email=email).first()
        if yaexiste:
            return "Ya estás registrado."
        else:
            nuevo_usuario = Usuario(
                nombre=nombre,
                email=email,
                usuario=usuario,
                password=password
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