from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/cine'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Peliculas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), unique=True)
    Descripcion = db.Column(db.String(200))
    Calificacion = db.Column(db.String(10))


    def __init__(self, Nombre, Descripcion,Calificacion):
        self.Nombre = Nombre
        self.Descripcion = Descripcion
        self.Calificacion = Calificacion

db.create_all()

class PeliculaSchema(ma.Schema):
    class Meta:
        fields = ('id', ' Nombre', 'Descripcion','Calificacion')


pelicula_schema = PeliculaSchema()
peliculas_schema = PeliculaSchema(many=True)

@app.route('/insert', methods=['Post'])
def create_pelicula():
  Nombre = request.json['Nombre']
  Descripcion = request.json['Descripcion']
  Calificacion = request.json['Calificacion']

  new_peli= Peliculas(Nombre, Descripcion,Calificacion)

  db.session.add(new_peli)
  db.session.commit()

  return pelicula_schema.jsonify(new_peli)

@app.route('/show', methods=['GET'])
def get_pelicula():
  all_peliculas = Peliculas.query.all()
  result = peliculas_schema.dump(all_peliculas)
  return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True)