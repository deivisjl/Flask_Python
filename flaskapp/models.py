from datetime import datetime
from flaskapp import db, login_manager
from flask import current_app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"Usuario('{self.id}','{self.email}')"

class Pelicula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(100), nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    comentario = db.relationship('Comentario',backref='pelicula', lazy=True)

    def __repr__(self):
        return f"Pelicula('{self.id}','{self.titulo}','{self.director}','{self.img_url}','{self.fecha_registro}')"

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pelicula_id = db.Column(db.Integer, db.ForeignKey('pelicula.id'), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    prediccion = db.Column(db.Integer,nullable=True)
    sentimiento = db.Column(db.Integer,nullable=True)
    procesado = db.Column(db.Integer,nullable=True)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


    def __repr__(self):
        return f"Comentario('{self.id}','{self.pelicula_id}','{self.comentario}','{self.prediccion}','{self.fecha_registro}')"