from flask import render_template, request, flash, url_for, redirect, Blueprint
from flaskapp import db
from flaskapp.models import Pelicula
from flaskapp.models import Comentario
from flaskapp.detail.forms import ComentarioForm
#
from flaskapp.analyzer.vectorizer import vect
import pickle
import os
import numpy as np

detail = Blueprint('detail',__name__)
directorio_actual = os.path.dirname(os.path.abspath(__file__ + "/../"))
clf = pickle.load(open(os.path.join(directorio_actual,'analyzer/pkl_objects/classifier.pkl'), 'rb'))

def calificar(documento):
    label = {0: 'negativo', 1: 'positivo'}
    X = vect.transform([documento])
    y = clf.predict(X)[0]
    proba = clf.predict_proba(X).max()
    if label[y]=='positivo':
        sentimiento = 1
    else:
        sentimiento = 0    
    return sentimiento, proba #label[y]

@detail.route("/detail/<int:pelicula_id>", methods=['GET','POST'])
def details(pelicula_id):
    pelicula = Pelicula.query.get_or_404(pelicula_id)
    comentarios = Comentario.query.filter_by(pelicula_id=pelicula.id).order_by(Comentario.fecha_registro.desc()).paginate()
    form = ComentarioForm()
    if form.validate_on_submit():
        comentario = form.dato.data
        sentimiento, probabilidad = calificar(comentario)
        registro = Comentario(pelicula_id=pelicula.id,comentario=form.dato.data,prediccion=round(probabilidad*100, 2),sentimiento=sentimiento,procesado=0)
        db.session.add(registro)
        db.session.commit()
        flash('Su comentario ha sido guardado con éxito','success')
        return redirect(url_for('main.home'))
    return render_template('detail.html',title="detalle",form=form,pelicula=pelicula,comentarios=comentarios)
