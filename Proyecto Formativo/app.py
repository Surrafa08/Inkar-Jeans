from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inicio_sesion.html')
def inicio_sesion():
    return render_template('inicio_sesion.html')

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