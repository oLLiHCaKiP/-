'''
Файл с обработкой логики для всех страниц нашего приложения
'''
from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, СreateApplicationForm, EditApplicationForm
from app.forms import CreateCompetitionForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import Participant, Competition, Application
from werkzeug.urls import url_parse
from app import db

@app.route('/')
@app.route('/index')
def index():
    '''
    Главная страница приложения со списком всех соревнований
    '''
    applications = Application.query.all()
    competitions = Competition.query.all()
    return render_template('index.html', 
                            title='Home', 
                            applications = applications,
                            competitions = competitions)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Страница входа для участника по логину и паролю
    '''
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Participant.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Participant(
            username=form.username.data, 
            name=form.name.data,
            surname = form.surname.data,
            patronymic = form.patronymic.data,
            city = form.city.data,
            description = form.description.data,
            gender = form.gender.data
            )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = Participant.query.filter_by(username=username).first_or_404()
    applications = Application.query.filter_by(participant_id=user.id)
    return render_template('profile.html', user=user, applications = applications)

@app.route('/application/<competition_id>',methods=['GET', 'POST'])
@login_required
def create_application(competition_id):
    '''
    Страница создания заявки на соревнование
    '''
    form = СreateApplicationForm()
    if form.validate_on_submit():
        application = Application.query.filter_by(competition_id=competition_id, participant_id = current_user.id).first()
        if application is not None:
            flash('Вы уже зарегистрированы на это соревнование')
            return redirect(url_for('index'))
        else:
            application = Application(description=form.description.data, participant_id = current_user.id, competition_id = int(competition_id))
            db.session.add(application)
            db.session.commit()
            flash('Поздравляем, вы зарегистрированы на соревнование!')
            return redirect(url_for('index'))
        
    return render_template('create_application.html',
                            title='Create application',
                            competition_id = competition_id,
                            form = form)

@app.route('/edit_application/<application_id>', methods=['GET', 'POST'])
@login_required
def edit_application(application_id):
    if current_user.username == 'admin':
        form = EditApplicationForm()
        application = Application.query.filter_by(id = application_id).first_or_404()
        if form.validate_on_submit():
            application.description = form.description.data
            application.rating = form.rating.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('index'))
        elif request.method == 'GET':
            form.description.data = application.description
            form.rating.data = application.rating
        return render_template('edit_application.html', title='Edit application',
                            form=form)
    else:
        return redirect(url_for('index'))

@app.route('/create_competition', methods=['GET', 'POST'])
@login_required
def create_competition():
    if current_user.username == 'admin':
        form = CreateCompetitionForm()
        if form.validate_on_submit():
            competition = Competition(name=form.name.data,
                                    description=form.description.data, 
                                    city = form.city.data,
                                    start_date = form.start_date.data,
                                    end_date = form.end_date.data 
                                    )
            db.session.add(competition)
            db.session.commit()
            flash('Поздравляем, вы создали соревнование!')
            return redirect(url_for('index'))
        return render_template('create_competition.html', title='Create competition', form = form)
    else:
        return redirect(url_for('index'))
