from flask import render_template, request, Blueprint
from flaskapp import db
from flaskapp.models import Pelicula
# from flaskapp.posts.forms import UserForm

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/listado")
def home():
    page = request.args.get('page',1, type=int)
    peliculas = Pelicula.query.order_by(Pelicula.fecha_registro.asc()).paginate(page=page, per_page=8)
    return render_template('home.html',peliculas=peliculas)

@main.route("/about")
def about():
    return render_template('about.html', title='about')