# test_unit.py

import unittest
from app import create_app, db
from models import User, Request, Reply, Like

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config.from_object('test_config')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_user_creation(self):
        user = User(name='testuser', email='test@example.com')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        retrieved_user = User.query.filter_by(name='testuser').first()
        self.assertIsNotNone(retrieved_user)
        self.assertTrue(retrieved_user.check_password('testpassword'))

    def test_request_creation(self):
        user = User(name='testuser', email='test@example.com')
        user.set_password('testpassword')  # 确保设置密码
        db.session.add(user)
        db.session.commit()
        request = Request(title='Test Request', description='Test Description', username=user.name)
        db.session.add(request)
        db.session.commit()
        retrieved_request = Request.query.filter_by(title='Test Request').first()
        self.assertIsNotNone(retrieved_request)
        self.assertEqual(retrieved_request.description, 'Test Description')

if __name__ == '__main__':
    unittest.main()
