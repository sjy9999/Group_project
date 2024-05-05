
# from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()

# user_id = request.form['user_id']
# user = session.query(User).filter(User.id == user_id).one()
import hashlib
class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    @classmethod
    def get_requests(cls,user_name):
        return Request.query.filter_by(username=user_name).all()

    @staticmethod
    def get(user_id):
        return db.session.get(User, int(user_id))
    def set_password(self, password):
        """创建哈希密码的方法"""
        self.password = generate_password_hash(password)
    def check_password(self, password):
        """检查哈希密码的方法"""
        return check_password_hash(self.password, password)
    
    def gravatar_url(self, size=100, default='retro', rating='g'):
        """Generate a gravatar URL based on the user's email."""
        hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        url = f"https://www.gravatar.com/avatar/{hash}?s={size}&d={default}&r={rating}"
        return url
    
    
    


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100))  # Changed to match the type of User.name

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def responder(self):
        return User.query.filter_by(name=self.responderName).first()
    
    
    
    


class Reply(db.Model):
    __tablename__ = 'replies'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))

    reply_content = db.Column(db.String(255))
    responderName = db.Column(db.String(255))
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    @hybrid_property
    def user(self):
        return User.query.filter_by(name=self.responderName).first()
    
    @hybrid_property
    def responder(self):
        return User.query.get(self.responder_id)
    

class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 点赞用户的ID
    reply_id = db.Column(db.Integer, db.ForeignKey('replies.id'), nullable=False)  # 点赞的回复ID
    status = db.Column(db.String(10), default='active', nullable=False)  # 点赞状态，'active' 或 'revoked'

    # 关系定义
    user = db.relationship('User', backref=db.backref('likes', lazy='dynamic'))
    reply = db.relationship('Reply', backref=db.backref('likes', lazy='dynamic'))

    # 保证每个用户对每个回复只能点赞一次
    __table_args__ = (db.UniqueConstraint('user_id', 'reply_id', name='unique_user_reply'),)
    



def create_bd():
    db.create_all()