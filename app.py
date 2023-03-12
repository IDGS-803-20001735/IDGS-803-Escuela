from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from Alumnos.routes import alumnos

app = Flask(__name__)
app.config['SECRET_KEY'] = "Esta es la clave encriptada"
csrf = CSRFProtect()

@app.route("/")
def index():
    return render_template('index.html')

app.register_blueprint(alumnos)

if __name__ == '__main__':
    csrf.init_app(app)
    app.run(debug = True, port = 3000)