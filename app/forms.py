'''
Файл с формами ввода для веб приложения
В первую очередь для формы логина
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from app.models import Participant

class CreateCompetitionForm(FlaskForm):
    name = StringField('Название соревнования: ',validators=[DataRequired()])
    description = TextAreaField('Описание заявки:', validators=[DataRequired(),Length(min=0, max=500)])
    city = StringField('Город проведения: ', validators=[DataRequired()])
    start_date = DateTimeField('Время начала',validators=[DataRequired()])
    end_date = DateTimeField('Время конца',validators=[DataRequired()])

    submit = SubmitField('Submit')

class СreateApplicationForm(FlaskForm):
    '''
    Форма регистрации заявки на соревнование
    '''
    description = TextAreaField('Расскажите почему хотите участвовать в соревновании', validators=[DataRequired(),Length(min=0, max=500)])
    
    submit = SubmitField('Create')

class EditApplicationForm(FlaskForm):
    description = TextAreaField('Описание заявки:', validators=[DataRequired(), Length(min=0, max=500)])
    rating = IntegerField('Рейтинг заявки:')
    submit = SubmitField('Submit')




class LoginForm(FlaskForm):
    '''
    Форма ввода данных пользователя для входа
    Состоит из кнопки Sign In
    И полей ввода с проверкой на наличие данных внутри них
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    '''
    Форма регистрации пользователя в системе
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name',validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    patronymic = StringField('Patronymic', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=140),DataRequired()])
    gender = BooleanField('Male')
    
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Participant.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

