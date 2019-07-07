from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PeliculaForm(FlaskForm):
        titulo = StringField('Título', validators=[DataRequired()])
        director = StringField('Director', validators=[DataRequired()])
        imagen = FileField('Subir imagen', validators=[FileAllowed(['jpg','png'])])
        submit = SubmitField('Guardar')