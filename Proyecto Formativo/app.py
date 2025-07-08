from flask import Flask, render_template
import sqlalchemy

print("SQLALchemy instalado correctamente. Version:", sqlalchemy.__version__)

app=Flask(__name__)

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