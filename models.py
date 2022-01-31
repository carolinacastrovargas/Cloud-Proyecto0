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

class TipoEvento(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column( db.String(50) )

class CategoriaEvento(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column( db.String(50) )

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
        return f'<Evento {self.title}>'
    def save(self):
        if not self.id:
            db.session.add(self)
        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                count += 1
    def public_url(self):
        return url_for('show_evento', evento_id=self.id)
    @staticmethod
    def get_by_id(evento_id):
        return Evento.query.filter_by(id=evento_id).first()
    @staticmethod
    def get_all():
        return Evento.query.all()