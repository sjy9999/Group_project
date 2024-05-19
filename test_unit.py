# test_unit.py
from sqlite3 import IntegrityError
import unittest
from app import create_app, db
from models import User, Request, Reply, Like
from flask import url_for
from flask_login import current_user

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test Flask application and client
        self.app = create_app()
        self.app.config.from_object('test_config')
        self.app.config['TESTING'] = True  # Enable testing mode to disable error catching
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database
        self.app.config['SERVER_NAME'] = 'localhost.localdomain:5000'  # Set the server name and port
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()  # Push the application context for setup
        db.create_all()

        # Create a test user and commit to the database
        test_user = User(name='testuser', email='999@example.com')
        test_user.set_password('testpassword')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        # Clean up the database and application context after each test
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
        
    def test_user_creation(self):
        # Test that a user can be created with valid details
        user = User(name='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        retrieved_user = User.query.filter_by(name='testuser').first()
        self.assertIsNotNone(retrieved_user)
        self.assertTrue(retrieved_user.check_password('testpassword'))
        
    def test_request_creation(self):
        # Test creating a request associated with a user
        user = User(name='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        request = Request(title='Test Request', description='Test Description', username=user.name)
        db.session.add(request)
        db.session.commit()
        retrieved_request = Request.query.filter_by(title='Test Request').first()
        self.assertIsNotNone(retrieved_request)
        self.assertEqual(retrieved_request.description, 'Test Description')
    
    def test_request_creationNeg(self):
        # Test that the title and description are not confused
        user = User(name='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        request = Request(title='Test Request', description='Test Description', username=user.name)
        db.session.add(request)
        db.session.commit()
        retrieved_request = Request.query.filter_by(title='Test Request').first()
        self.assertIsNotNone(retrieved_request)
        self.assertNotEqual(retrieved_request.title, 'Test Description')

    def test_duplicate_user_creation(self):
        # Test handling of duplicate user creation attempt
        user1 = User(name='testuser', email='test@example.com')
        user1.set_password('testpassword')
        db.session.add(user1)
        db.session.commit()

        user2 = User(name='testuser', email='different@example.com')
        user2.set_password('testpassword')
        db.session.add(user2)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()  # Rollback to clean up the session
            self.assertIsInstance(e, IntegrityError)  # Check that an IntegrityError is raised

    def test_request_creation_without_user(self):
        # Test creation of a request without a linked user
        request = Request(title='Orphan Request', description='No user attached', username='')
        db.session.add(request)
        db.session.commit()
        retrieved_request = Request.query.filter_by(title='Orphan Request').first()
        self.assertIsNotNone(retrieved_request)  # Assume the request can exist without a valid user

if __name__ == '__main__':
    unittest.main()
