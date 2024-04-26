from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 's395615470@gmail.com'
app.config['MAIL_PASSWORD'] = 'johgpueksgsakecj'  # 应用密码
app.config['MAIL_DEFAULT_SENDER'] = 's395615470@gmail.com'

mail = Mail(app)


def send_email():
    """发送邮件的函数"""
    msg = Message("Hello",
                  recipients=["395615470@qq.com"])
    msg.body = "This is a test email sent automatically from a Flask app!"
    mail.send(msg)
    print("Email sent successfully!")

if __name__ == "__main__":
    with app.app_context():
        send_email()  # 在应用上下文中发送邮件
    app.run(debug=True)