from flask import current_app, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import sqlite3
from models import User  # 确保导入了 User 模型
# from app import db

class PasswordResetService:
    # ini
    @staticmethod
    def generate_reset_token(email):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
# button   仅仅发送邮件     比如发送到我qq邮箱
    @staticmethod
    def sendUpdatePassword(user_email):
        token = PasswordResetService.generate_reset_token(user_email)
        reset_url = url_for('reset_password', token=token, _external=True)
        # reset_url = url_for('change_password', token=token, _external=True)
        # 这是   给我的邮箱   发送的内容     reset_password  url
        msg = Message("Password Reset Requested",
                      recipients=[user_email])
        msg.body = f'This is from the cits5505 project, to reset your password, please visit the following link: {reset_url}'
        from app import mail
        mail.send(msg)

    @staticmethod
    def verify_reset_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=current_app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except (SignatureExpired, BadSignature):
            return None
        return email

    # @staticmethod
    # def update_password(email, new_password):
    #     con = sqlite3.connect("database.db")
    #     cur = con.cursor()
    #     cur.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
    #     con.commit()
    #     con.close()
    # @staticmethod
    # def update_password(email, new_password):
    #     # 使用 SQLAlchemy 查询用户
    #     from app import db  # 这个导入移到了函数内部
    #     user = User.query.filter_by(email=email).first()
        
    #     # 如果找到用户，则更新密码
    #     if user:
    #         user.password = new_password  # 假设这里密码已经过哈希处理
    #         db.session.commit()
    @staticmethod
    def update_password(email, new_password):
        from app import db
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = new_password
            db.session.commit()            