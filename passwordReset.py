from flask import current_app, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import sqlite3
from models import User  # import User
from werkzeug.security import generate_password_hash


class PasswordResetService:
    # ini
    @staticmethod
    def generate_reset_token(email):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
# button   send message to my email address
    @staticmethod
    def sendUpdatePassword(user_email):
        token = PasswordResetService.generate_reset_token(user_email)
        reset_url = url_for('reset_password', token=token, _external=True)
        msg = Message("Password Reset Requested",
                      recipients=[user_email])
        msg.body = f'This is from the cits5505 project, to reset your password, please visit the following link: {reset_url}'
        
        mail = current_app.extensions['mail']
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

    @staticmethod
    def update_password(email, new_password):
        from app import db
        user = User.query.filter_by(email=email).first()
        if user is None:
            return False

        hashed_password = generate_password_hash(new_password)  # create hash
        user.password = hashed_password  # update hash
        db.session.commit()
        return True        