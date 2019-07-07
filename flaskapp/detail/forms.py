from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ComentarioForm(FlaskForm):
        dato = TextAreaField('Escribe tu comentario', validators=[DataRequired()])
        submit = SubmitField('Enviar')



# pelicula_id = StringField('Pelicula_id')
        # prediccion = StringField('Prediccion')
        # sentimiento = StringField('Sentimiento')
        # procesado = StringField('Procesado')