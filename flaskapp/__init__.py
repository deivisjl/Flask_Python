from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.login_message_category = 'info'

#importar namespaces de controladores
from flaskapp.user.routes import user

from flaskapp.main.routes import main
from flaskapp.detail.routes import detail
from flaskapp.admin.pelicula.routes import pelicula
from flaskapp.admin.comentario.routes import comentario

from flaskapp.errors.handlers import errors

def create_app():
    app = Flask(__name__)
    #app.config from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    app.config['SECRET_KEY']='279b51201dfd37aadc88b71c7f795e6d'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskdb.db'

    #registrar controladores
    app.register_blueprint(user)

    app.register_blueprint(main)
    app.register_blueprint(detail)
    app.register_blueprint(pelicula)
    app.register_blueprint(comentario)
    
    app.register_blueprint(errors)

    return app
