import unittest
from flask import current_app
from app import create_app, db
import os
import sys
from app.models import User, Product
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestCase(unittest.TestCase):
    # set up testing environment
    def setUp(self):
        # create app run on testing config which use a different database (test.db)
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
    
    # clear database after test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    # test to see if app exist
    def test_app_exists(self):
        # check if app is None
        self.assertFalse(current_app is None)
        
    # check if app is running in testing config
    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])
        
    # check if home page is showing
    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        # check if it has the 'Welcome' string
        self.assertIn(b"Welcome", response.data)

    # check if the users page is showing
    def test_users(self):
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 200)
        # check if is has 'All Users' string
        self.assertIn(b"All Users", response.data)

    # check if the products page is showing
    def test_products(self):
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)
        # check if is has 'All Products' string
        self.assertIn(b"All Products", response.data)

    # This function test a lot of routes so I have more comments in the code
    def test_new_user(self):
        # try registering a new user
        response = self.client.post("/user/new", data={
            "username" : "testuser1",
            "email" : "testuser1@gmail.com",
            "password" : "testpassword"
        })

        # 302 means a success insert
        self.assertEqual(response.status_code, 302)
        # check for new user in the User database
        user = User.query.filter_by(username='testuser1').first()

        # check if the user is None
        self.assertTrue(user)

        # check the user page
        response = self.client.get(f"/user/{user.id}")
        # 200 means the page is found
        self.assertEqual(response.status_code, 200)
        # double check to see if username is on the page
        self.assertIn(b"testuser1", response.data)

        # check the logout page
        response = self.client.get(f"/logout", follow_redirects=True)
        # 200 means the page is found
        self.assertEqual(response.status_code, 200)
        # double check to see if it redirect to correct destination
        self.assertIn(b"All Users", response.data)

        # check the redirect_new_product route
        response = self.client.get("/redirect_new_product", follow_redirects=True)
        # 200 means the page is found
        self.assertEqual(response.status_code, 200)

        # check the login route
        response = self.client.post("/login", data={
            "email" : "testuser1@gmail.com",
            "password" : "testpassword"
        })
        # 302 means login success
        self.assertEqual(response.status_code, 302)

        # check the delete route
        response = self.client.post(f"/delete_user/{user.id}", data={
            "email" : "testuser1@gmail.com",
            "password" : "testpassword"
        })

        # 302 means data accepted
        self.assertEqual(response.status_code, 302)
        # check if the user is deleted in the database
        self.assertFalse(User.query.filter_by(username='testuser1').first())

        # test the error route
        response = self.client.get(f"/user/{user.id}")
        # user is deleted so it should be 404
        self.assertEqual(response.status_code, 404)

    def test_new_product(self):
        # try registering a new user
        response = self.client.post("/user/new", data={
            "username" : "testuser2",
            "email" : "testuser2@gmail.com",
            "password" : "testpassword"
        })

        # 302 means a success insert
        self.assertEqual(response.status_code, 302)
        # check for new user in the User database
        user = User.query.filter_by(username='testuser2').first()
        # check if the user is None
        self.assertTrue(user)

        # check the redirect_new_product again but this time we are log in
        response = self.client.get("/redirect_new_product", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"submit", response.data)

        # try creating a new product
        response = self.client.post(f"/{user.id}/product/new", data={
            "title" : "testproduct",
            "description" : "good",
            "price" : "10"
        })
        # 302 means data accepted
        self.assertEqual(response.status_code, 302)
        # check to see if the product is in the database
        product = Product.query.filter_by(title='testproduct').first()
        self.assertTrue(product)

        # check to see if the product page exist
        response = self.client.get(f'/product/{product.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"testproduct", response.data)

        # check deleting a product
        response = self.client.get(f'/delete_product/{product.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)  
        self.assertIn(b"All Products", response.data)     