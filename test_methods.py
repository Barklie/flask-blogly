from unittest import TestCase
from models import db, User
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_methods_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    def set_up(self):
        User.query.delete()

    def tear_down(self):
        User.query.rollback()

    
    def test_update_user(self):
        user = User(first_name='Barklie', last_name='Griggs', profile_picture='pro_pic')

        user.update_user('John', 'Locke', 'pro_pic_2')
        # db.session.add(user)

        self.assertEquals(user.first_name, 'John')
        self.assertEquals(user.last_name, 'Locke')
        self.assertEquals(user.profile_picture, 'pro_pic_2')

    def test_users(self):
        with app.test_client() as client:
            user = User(first_name='Barklie', last_name='Griggs', profile_picture='pro_pic')
            db.session.add(user)
            resp = client.get('/users')

            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="users/1">Barklie Griggs</a></li>', html)  

    def test_redirection(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")         