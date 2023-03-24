import unittest
from flask import url_for
from app import app, db
from models import User, Product
from config import TestConfig
from werkzeug.security import generate_password_hash, check_password_hash

class FlaskTest(unittest.TestCase):

    def setUp(self):
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_products(self):
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)

    def test_new_user(self):
        with app.app_context():
            data = {
                'username': 'test_user',
                'email': 'test_user@test.com',
                'password': 'password'
            }
            response = self.app.post('/user/new', data =data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(User.query.filter_by(email='test_user@test.com').first())

    # def test_login_logout(self):
    #     data = {
    #         'email': 'testuser@test.com',
    #         'password': 'testpassword'
    #     }
    #     # test login with valid credentials
    #     response = self.app.post('/login', data=data, follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(User.query.filter_by(username='testuser').first().is_authenticated)

    #     # test logout
    #     response = self.app.get('/logout', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(User.query.filter_by(username='testuser').first().is_authenticated)

    # def test_new_product(self):
    #     # create a test user
    #     user = User(username='testuser', email='testuser@test.com', password='testpassword')
    #     with app.app_context():
    #         db.session.add(user)
    #         db.session.commit()

    #     # test creating a new product while logged in
    #     with self.app.session_transaction() as sess:
    #         sess['user_id'] = user.id
    #     data = {
    #         'title': 'Test Product',
    #         'description': 'This is a test product.',
    #         'price': 9.99
    #     }
    #     response = self.app.post('/{}/product/new'.format(user.id), data=data, follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(Product.query.filter_by(title='Test Product').first())

    # def test_delete_user(self):
    #     # create a test user
    #     user = User(username='testuser', email='testuser@test.com', password='testpassword')
    #     with app.app_context():
    #         db.session.add(user)
    #         db.session.commit()

    #     # test deleting a user while logged in
    #     with self.app.session_transaction() as sess:
    #         sess['user_id'] = user.id
    #     data = {
    #         'password': 'testpassword'
    #     }
    #     response = self.app.post('/delete_user/{}'.format(user.id), data=data, follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(User.query.filter_by(username='testuser').first())

