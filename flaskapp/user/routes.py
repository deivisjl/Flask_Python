from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp import db, bcrypt
from flaskapp.user.forms import RegistrarForm, LoginForm
from flaskapp.models import Usuario

user = Blueprint('user',__name__)

@user.route('/registrarse', methods=['GET','POST'])
def registrar():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrarForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Usuario( email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Su cuenta ha sido registrada! ya puedes ingresar','success')
        return redirect(url_for('user.login'))
    return render_template('register.html',title='Registro', form=form)

@user.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('pelicula.peliculas'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('pelicula.peliculas'))            
        else:
            flash('Credenciales inválidas. Inténtelo nuevamente', 'danger') 
    return render_template('login.html',title='Login', form=form)

@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))