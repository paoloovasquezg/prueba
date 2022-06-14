import sys
import random
from crypt import methods
from flask import (
    Flask,
    abort,
    jsonify, 
    render_template, 
    request,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/pc1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#models
class Credit(db.Model):
    __tablename__ = 'credito'
    id = db.Column(db.Integer,primary_key=True)
    nombres = db.Column(db.String(), nullable=False)
    apellidos = db.Column(db.String(), nullable=False)
    sexo = db.Column(db.String(), nullable=False)
    tipo_documento = db.Column(db.String(), nullable=False)
    num_documento = db.Column(db.BigInteger(),nullable=False)
    email = db.Column(db.String(), nullable=False)
    val_vehiculo = db.Column(db.BigInteger(),nullable=False)
    cout_inicial = db.Column(db.BigInteger(),nullable=False)
    operacion = db.Column(db.BigInteger(),nullable=False)

# db.create_all()

#controller
@app.route('/', methods=['GET'])
def index():
    str = 'Usuario'
    return render_template('index.html', data=Credit.query.all()[-1], mandado = str)

@app.route('/credito/simular', methods=['POST'])
def create_todo():
    error = False
    response = {}
    try:
        nombres = request.get_json()['nombre']
        apellidos = request.get_json()['apellidos']
        sexo = request.get_json()['sexo']
        td = request.get_json()['td']
        nd = request.get_json()['nd']
        email = request.get_json()['em']
        val = request.get_json()['vv']
        cout = request.get_json()['mc']
        operacion = (random.randint(100,1000) * int(cout)) - (int(val)/500)
        credito = Credit(nombres=nombres,apellidos = apellidos, sexo = sexo,tipo_documento=td,
        num_documento=nd,email=email,val_vehiculo=val,cout_inicial=cout,operacion=operacion)
        db.session.add(credito)
        db.session.commit()
        response['nombres'] = nombres
        response['apellidos'] = apellidos
        response['sexo'] = sexo
        response['tipo_documento'] = td
        response['num_documento'] = nd
        response['email'] = email
        response['val_vehiculo'] = val
        response['cout_inicial'] = cout
        response['operacion'] = operacion
    except Exception as e:
        error = True
        print(e)
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5001)