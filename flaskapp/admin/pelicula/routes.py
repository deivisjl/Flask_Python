from flask import render_template, request, redirect, url_for, flash,Blueprint
from flaskapp import db
from flask_login import current_user, login_required
# from flaskapp.models import User
# from flaskapp.posts.forms import UserForm
from flaskapp.models import Pelicula
from flaskapp.admin.pelicula.forms import PeliculaForm
from flaskapp.admin.pelicula.utils import save_picture

pelicula = Blueprint('pelicula',__name__)

@pelicula.route("/admin/peliculas")
@login_required
def peliculas():
    page = request.args.get('page',1, type=int)
    peliculas = Pelicula.query.order_by(Pelicula.fecha_registro.asc()).paginate(page=page, per_page=10)
    return render_template('admin/pelicula.html',peliculas=peliculas)

@pelicula.route("/admin/peliculas/agregar", methods=['GET','POST'])
@login_required
def agregar():
    form = PeliculaForm()
    if form.validate_on_submit():
        if form.imagen.data:
            archivo = save_picture(form.imagen.data)
            pelicula = Pelicula(titulo=form.titulo.data, director=form.director.data, img_url=archivo)
            db.session.add(pelicula)
            db.session.commit()
            flash('El registro ha sido guardado con éxito','success')
            return redirect(url_for('pelicula.peliculas'))
    return render_template('admin/agregar.html', title='Agregar',form=form, legend='Agregar película')

@pelicula.route("/admin/peliculas/<int:pelicula_id>/borrar", methods=['GET'])
@login_required
def borrar_pelicula(pelicula_id):
    pelicula = Pelicula.query.get_or_404(pelicula_id)
    db.session.delete(pelicula)
    db.session.commit()
    flash('El registro ha sido eliminado con éxito','success')
    return redirect(url_for('pelicula.peliculas'))

