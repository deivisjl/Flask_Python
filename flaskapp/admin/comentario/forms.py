from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, RadioField, HiddenField
from wtforms.validators import DataRequired

class TrainingForm(FlaskForm):
        comentario_id = HiddenField('comentario_id', validators=[DataRequired()])
        comentario = HiddenField('comentario',validators=[DataRequired()])
        pelicula_id = HiddenField('pelicula_id',validators=[DataRequired()])
        sentimiento = HiddenField('sentimiento',validators=[DataRequired()])
        calificar = RadioField('Calificar', choices=[('1','Correcto'),('2','Incorrecto')], validators=[DataRequired()])
        submit = SubmitField('Enviar respuesta')