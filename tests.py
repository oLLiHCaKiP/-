import os
import unittest
import datetime

from config import basedir
from app import app, db
from app.models import Participant, Competition

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_competition(self):
        competition = Competition(name='сорев',
                                description='сорев', 
                                city = 'сорев',
                                start_date = datetime.datetime(2021,11,28),
                                end_date = datetime.datetime(2021,11,28)
                                )
        db.session.add(competition)
        db.session.commit()

        competition = Competition.query.first()
        assert competition.name == 'сорев', f'{competition.name} не совпадает с сорев'
        assert competition.start_date == datetime.datetime(2021,11,28), f'{competition.start_date} не совпадает с datetime.datetime(2021,11,28)'

    def test_create_participant(self):
        user = Participant(
            username='user', 
            name='user',
            surname = 'user',
            patronymic = 'user',
            city = 'user',
            description = 'user',
            gender = True
            )
        
        db.session.add(user)
        db.session.commit()

        user = Participant.query.first()

        assert user.name == 'user'
            
    #test loading index page
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #test login page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(u'Login' in response.data)
if __name__ == '__main__':
    unittest.main()
