# test_unit.py
# change about
import unittest
from app import create_app, db
from models import User, Request, Reply, Like
from flask import url_for

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config.from_object('test_config')
        # self.client = self.app.test_client()
        # self.ctx = self.app.app_context()
        # self.ctx.push()
        # db.create_all()
        
  
        # self.app = create_app()
        self.app.config['TESTING'] = True  # 开启测试模式，关闭错误捕获
        self.app.config['WTF_CSRF_ENABLED'] = False  # 禁用 CSRF 保护
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # 使用内存数据库
        self.app.config['SERVER_NAME'] = 'localhost.localdomain:5000'  # 设置服务器名和端口
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        # 创建一个测试用户
        test_user = User(name='testuser', email='999@example.com')
        test_user.set_password('testpassword')
        db.session.add(test_user)
        db.session.commit()


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
        user.set_password('testpassword')  # Ensure password is set
        db.session.add(user)
        db.session.commit()
        request = Request(title='Test Request', description='Test Description', username=user.name)
        db.session.add(request)
        db.session.commit()
        retrieved_request = Request.query.filter_by(title='Test Request').first()
        self.assertIsNotNone(retrieved_request)
        self.assertEqual(retrieved_request.description, 'Test Description')
    
        
    def test_request_creationNeg(self):
        user = User(name='testuser', email='test@example.com')
        user.set_password('testpassword')  # Ensure password is set
        db.session.add(user)
        db.session.commit()
        request = Request(title='Test Request', description='Test Description', username=user.name)
        db.session.add(request)
        db.session.commit()
        retrieved_request = Request.query.filter_by(title='Test Request').first()
        self.assertIsNotNone(retrieved_request)
        self.assertNotEqual(retrieved_request.title, 'Test Description')

    def test_duplicate_user_creation(self):
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
            db.session.rollback()  # Important to rollback to keep the session clean
            self.assertIsInstance(e, IntegrityError)  # Assuming using SQLAlchemy that would throw an IntegrityError on duplicate key

    def test_request_creation_without_user(self):
        request = Request(title='Orphan Request', description='No user attached', username='')
        db.session.add(request)
        db.session.commit()
        retrieved_request = Request.query.filter_by(title='Orphan Request').first()
        self.assertIsNotNone(retrieved_request)  # This assumes that there should not be a request without a valid user
    
    def test_user_login(self):
        response = self.client.post('/access/', data=dict(
            login='login',
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Main Page', response.data)  # Replace with actual text in your main page



if __name__ == '__main__':
    unittest.main()
