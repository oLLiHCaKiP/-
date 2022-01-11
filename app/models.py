'''
Файл с классами-сущностями из базы данных
'''
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class Participant(db.Model, UserMixin):
    '''
    Сущность участника
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64)) # Имя
    surname = db.Column(db.String(64)) # Фамилия
    patronymic = db.Column(db.String(64)) # Отчество
    city = db.Column(db.String(64),index=True) # Город
    description = db.Column(db.String(256)) # Описание-биография
    gender = db.Column(db.Boolean()) # True - male, False - female
    applications = db.relationship('Application', backref='author', lazy='dynamic')

    username = db.Column(db.String(64), index=True, unique=True) # логин
    password_hash = db.Column(db.String(128)) # Пароль в виде хеша


    def __repr__(self):
        return f'<Participant {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(user_id):
    '''
    Пользовательский загрузчик пользователя
    '''
    return Participant.query.get(int(user_id))

class Competition(db.Model):
    '''
    Сущность соревнования
    содержит всю необходимую информацию о соревновании
    '''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True) # Имя
    description = db.Column(db.String(256)) # Описание соревнования
    city = db.Column(db.String(64),index=True) # Город

    applications = db.relationship('Application', backref='competition', lazy='dynamic')

    # Дата начала и конца
    start_date = db.Column(db.DateTime, index = True)
    end_date = db.Column(db.DateTime, index = True)

    def __repr__(self):
        return f'<Competition {self.name}>' 

class Application(db.Model):
    '''
    Сущность соревнования
    содержит всю необходимую информацию о соревновании
    '''
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256)) # Описание соревнования
    rating = db.Column(db.Integer, default = 0) # Выставленные баллы за заявку


    participant_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))

    def __repr__(self):
        return f'<Application {self.id}>' 

