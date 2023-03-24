import unittest
from flask import current_app
from app import create_app, db
import os
import sys
from app.models import User, Product
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_app_exists(self):
        self.assertFalse(current_app is None)
        
    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])
        
    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_users(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)

    def test_products(self):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)

    def test_new_user(self):
        response = self.client.post("/user/new", data={
            "username" : "testuser1",
            "email" : "testuser1@gmail.com",
            "password" : "testpassword"
        })

        self.assertEqual(response.status_code, 302)
        user = User.query.filter_by(username='testuser1').first()

        self.assertTrue(user)
        response = self.client.get(f"/user/{user.id}")
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f"/logout")
        self.assertEqual(response.status_code, 302)

        response = self.client.get("/redirect_new_product")
        self.assertEqual(response.status_code, 302)

        response = self.client.post("/login", data={
            "email" : "testuser1@gmail.com",
            "password" : "testpassword"
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post(f"/delete_user/{user.id}", data={
            "email" : "testuser1@gmail.com",
            "password" : "testpassword"
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.query.filter_by(username='testuser1').first())

        response = self.client.get(f"/user/{user.id}")
        self.assertEqual(response.status_code, 404)

    def test_new_product(self):
        response = self.client.post("/user/new", data={
            "username" : "testuser2",
            "email" : "testuser2@gmail.com",
            "password" : "testpassword"
        })

        self.assertEqual(response.status_code, 302)
        user = User.query.filter_by(username='testuser2').first()
        self.assertTrue(user)

        response = self.client.get("/redirect_new_product")
        self.assertEqual(response.status_code, 302)

        response = self.client.post(f"/{user.id}/product/new", data={
            "title" : "testproduct",
            "description" : "good",
            "price" : "10"
        })
        self.assertEqual(response.status_code, 302)
        product = Product.query.filter_by(title='testproduct').first()
        self.assertTrue(product)

        response = self.client.get(f'/product/{product.id}')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/delete_product/{product.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)       