# test_config.py
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///test_database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'test_secret_key'
MAIL_SUPPRESS_SEND = True
WTF_CSRF_ENABLED = False
