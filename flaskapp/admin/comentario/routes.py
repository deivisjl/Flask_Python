from flask import render_template, request, redirect, url_for, flash,Blueprint
from flaskapp import db
from flask_login import current_user, login_required
from flaskapp.models import Pelicula, Comentario
from flaskapp.admin.comentario.forms import TrainingForm
#
from flaskapp.analyzer.vectorizer import vect
import pickle
import os
import numpy as np

comentario = Blueprint('comentario',__name__)
directorio_actual = os.path.dirname(os.path.abspath(__file__ + "/../../"))
print(directorio_actual)
clf = pickle.load(open(os.path.join(directorio_actual,'analyzer/pkl_objects/classifier.pkl'), 'rb'))

def entrenar(documento, y):
    X = vect.transform([documento])
    clf.partial_fit(X, [y])

@comentario.route("/admin/listado-peliculas")
@login_required
def lista_peliculas():
    page = request.args.get('page',1, type=int)
    peliculas = Pelicula.query.order_by(Pelicula.fecha_registro.asc()).paginate(page=page, per_page=10)
    return render_template('admin/lista_pelicula.html',peliculas=peliculas)

@comentario.route("/admin/pelicula-comentario/<int:pelicula_id>", methods=['GET'])
@login_required
def lista_comentarios(pelicula_id):
    page = request.args.get('page',1, type=int)
    pelicula = Pelicula.query.get_or_404(pelicula_id)
    comentarios = Comentario.query.filter_by(pelicula_id=pelicula.id,procesado=0).order_by(Comentario.fecha_registro.desc()).paginate()
    return render_template('admin/lista_comentarios.html', comentarios=comentarios, pelicula=pelicula)

@comentario.route("/admin/comentario-calificar/<int:id>", methods=['GET','POST'])
@login_required
def calificar(id):
    comentario = Comentario.query.get_or_404(id)
    form = TrainingForm()
    if form.validate_on_submit():
        inv_label = {'negative': 0, 'positive': 1}
        if form.sentimiento.data==1:
            y_sent = 'positive'
        else:
            y_sent = 'negative'
        y = inv_label[y_sent]
        if form.calificar==2:
            y = int(not(y))
            entrenar(form.comentario.data, y)
        comentario.procesado = 1
        db.session.merge(comentario)
        db.session.commit()
        return redirect(url_for('comentario.lista_comentarios',pelicula_id=comentario.pelicula_id))
    form.comentario_id.data = comentario.id
    form.comentario.data = comentario.comentario 
    form.pelicula_id.data = comentario.pelicula_id
    form.sentimiento.data = comentario.sentimiento   
    return render_template('admin/calificar.html',form=form)