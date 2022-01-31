from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,TextAreaField, BooleanField,DateField,IntegerField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')

class EventoForm(FlaskForm):
    id = IntegerField('id')
    nombre =  StringField('Nombre', validators=[Length(max=128)])
    idCategoriaEvento =  StringField('Categoría', validators=[Length(max=128)])
    lugar = StringField('Lugar', validators=[Length(max=128)])
    direccion =  StringField('Dirección', validators=[Length(max=128)])
    fechaInicio = DateField('Fecha Inicio')
    fechaFin = DateField('Fecha Finalizacióm')
    idTipoEvento =  StringField('Tipo de evento', validators=[Length(max=128)])
    submit = SubmitField('Enviar')
    update = SubmitField('Actualizar')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')