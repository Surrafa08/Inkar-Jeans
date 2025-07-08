from flask import Flask, render_template
from sqlalchemy import create_engine, Column, Integer, String

app=Flask(__name__)

create_engine = ("sqlite:///basedatos.db")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/administracion.html')
def administracion():
    return render_template('administracion.html')

@app.route('/registro.html')
def registro():
    return render_template('registro.html')

@app.route('/restablecer_contra.html')
def restablecer_contra():
    return render_template('restablecer_contra.html')

@app.route('/mostrar_index')
def mostrar_index():
    return render_template('index.html') 

if __name__=='__main__':
    app.run(debug=True)