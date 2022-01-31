from flask import Flask
from flask import render_template, request, redirect, url_for, g, abort
from forms import SignupForm, EventoForm, LoginForm
from flask_login import LoginManager, logout_user, current_user, login_user, login_required
from datetime import datetime
#from models import users, User
from werkzeug.urls import url_parse

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB_proyecto0.db' 
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
db = SQLAlchemy(app) 

login_manager = LoginManager(app)
login_manager.login_view = "login"
db = SQLAlchemy(app)

@app.route("/")
def index():
    eventos = Evento.get_by_user(0)
    if current_user.is_authenticated:
        eventos = Evento.get_by_user(current_user.id)
    return render_template("index.html", eventos=eventos)

@app.route("/e/<int:evento_id>/")
def show_evento(evento_id):
    evento = Evento.get_by_id(evento_id)
    if evento is None:
        abort(404)
    return render_template("evento_view.html", evento=evento)

@app.route("/eventoDelete/<int:evento_id>/", methods=['GET', 'POST'])   
def evento_delete(evento_id):
    evento = Evento.get_by_id(evento_id)
    db.session.delete(evento)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/eventoupdate/<int:evento_id>/", methods=['GET', 'POST'])   
def evento_update(evento_id):
    evento = Evento.get_by_id(evento_id)
    if evento:
        form = EventoForm(formdata=request.form, obj=evento)
        if request.method == 'POST' and form.validate():
            evento.nombre = form.nombre.data
            evento.idCategoriaEvento = form.idCategoriaEvento.data
            evento.lugar = form.lugar.data
            evento.direccion = form.direccion.data
            evento.fechaInicio = form.fechaInicio.data
            evento.fechaFin = form.fechaFin.data
            evento.idTipoEvento = form.idTipoEvento.data
            db.session.commit()

            return redirect(url_for('index')) 
        return render_template('evento_form.html', form=form)

@app.route("/evento/", methods=['GET', 'POST'], defaults={'evento_id': None})
@app.route("/evento/<int:evento_id>/", methods=['GET', 'POST','PUT'])
#@login_required
def evento_form(evento_id):   
    form = EventoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        idCategoriaEvento = form.idCategoriaEvento.data
        lugar = form.lugar.data
        direccion = form.direccion.data
        fechaInicio = form.fechaInicio.data
        fechaFin = form.fechaFin.data
        idTipoEvento = form.idTipoEvento.data
        fechaCreacion = datetime.now()
        evento = Evento(user_id=current_user.id, nombre=nombre,idCategoriaEvento=idCategoriaEvento,lugar=lugar,direccion=direccion,fechaInicio=fechaInicio,fechaFin=fechaFin,idTipoEvento=idTipoEvento,fechaCreacion=fechaCreacion)
        evento.save()
        return redirect(url_for('index'))
    return render_template("evento_form.html", form=form)


@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya se encuentra registrado con nosotros'
        else:
            user = User(email=email)
            user.set_password(password)
            user.save()
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template("signup_form.html", form=form, error=error)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
#from run import db

class User(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

from sqlalchemy.exc import IntegrityError
class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False)
    nombre = db.Column( db.String(250) )
    idCategoriaEvento = db.Column( db.Integer )
    lugar = db.Column( db.String(250) )
    direccion = db.Column( db.String(250) )
    fechaInicio = db.Column( db.DateTime )
    fechaFin = db.Column( db.DateTime )
    idTipoEvento = db.Column( db.Integer )
    fechaCreacion = db.Column( db.DateTime )
    def __repr__(self):
        return f'<Evento {self.id}>'
    def save(self):
        if not self.id:
            db.session.add(self)
            db.session.commit()
    def public_url(self):
        return url_for('show_evento', evento_id=self.id)
    def evento_delete(self):
        return url_for('evento_delete',evento_id=self.id)
    def evento_update(self):
         return url_for('evento_update',evento_id=self.id)
    @staticmethod
    def get_by_id(evento_id):
        return Evento.query.filter_by(id=evento_id).first()
    @staticmethod
    def get_all():
        return Evento.query.all()
    def get_by_user(user_id):
        evento = Evento.query.filter_by(user_id=user_id).order_by(desc(Evento.fechaCreacion)).all()
        return evento


class TipoEvento(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column( db.String(50) )

class CategoriaEvento(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column( db.String(50) )

#if __name__ == '__main__':
 #   app.run(debug=True)

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=8080, debug=False)