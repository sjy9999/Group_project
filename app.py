from flask import Flask, request, render_template, redirect, url_for, session,make_response, flash
import sqlite3
# from passwordReset import PasswordResetService
from flask_mail import Mail
import os
from routes import UserViews
from flask_sqlalchemy import SQLAlchemy
# from models import User  # 确保从 models.py 导入了 User
# from app import app, db


#要求
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from flask_wtf.csrf import CSRFProtect,generate_csrf
from wtforms.validators import InputRequired, Email
from wtforms.validators import DataRequired


# 项目启动       student.html 这是主界面  名字没事
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.secret_key = 'JunyiSun_secret_key'  # 用于保持会话安全
# app.secret_key = 'your_secret_key'  # 用于保持会话安全
app.config['SECRET_KEY'] = '8f42a73054b1749f8f58848be5e6502c'
app.config['SECURITY_PASSWORD_SALT'] = '3243f6a8885a308d313198a2e0370734'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail的SMTP服务器  smtp.sina.com       smtp.gmail.com
app.config['MAIL_PORT'] = 587  # 邮件发送端口
app.config['MAIL_USE_TLS'] = True  # 启用传输层安全性协议
app.config['MAIL_USERNAME'] = 's395615470@gmail.com'
app.config['MAIL_PASSWORD'] = 'johgpueksgsakecj'  # 你的Gmail密码或应用密码
app.config['MAIL_DEFAULT_SENDER'] = 's395615470@gmail.com'  # 默认的发件人邮箱地址

mail = Mail(app)
app.register_blueprint(UserViews.bp)

with app.app_context():
    db.create_all()

# this is WTForms  CSRFProtect
csrf = CSRFProtect(app)
login_manager = LoginManager(app)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[Email()])



# 先留着    先打开   这个界面   注册 登录账号       这是   http://127.0.0.1:5000/create/
# @app.route('/create/')
# def create_student():
#     return render_template('student.html')    #渲染student.html模板

# 先留着    添加学生的路由，支持POST和GET请求    @app.route('/addstudent/')     http://127.0.0.1:5000/addstudent/
# @app.route('/addstudent/',methods = ['POST', 'GET'])
# def add_student():
#     try:
#         #获取请求中的nm、add、city、pin的数据
#         nm = request.form['nm']
#         addr = request.form['add']
#         city = request.form['city']
#         pin = request.form['pin']
#         with sqlite3.connect("database.db") as con:  
#            cur = con.cursor()     
#            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )                
#            con.commit()    
#            msg = "添加这个新的学生   成功"
#     except:
#         con.rollback()
#         msg = "添加这个新的学生   失败"
#     finally:
#         # 这个才是对的
#         if con:
#             con.close()
#         # 改url_for       而不是返回html
#         return redirect(url_for('show_student'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/access/', methods=['GET', 'POST'])
def access():
    login_form = LoginForm()
    register_form = RegisterForm()
    if 'login' in request.form and login_form.validate_on_submit():
        # 处理登录逻辑
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(name=username).first()
        if user and user.check_password(password):
            login_user(user)
            session['loggedin'] = True
            session['username'] = user.name
            return redirect(url_for('main'))  # 主页或成功页
        else:
            return render_template('result.html', login_form=login_form, register_form=register_form, login_msg='Incorrect username or password!')

    elif 'register' in request.form and register_form.validate_on_submit():
        # 处理注册逻辑
        try:
            username = register_form.username.data
            password = register_form.password.data
            email = register_form.email.data
            new_user = User(name=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main'))  # 主页或成功页
        except Exception as e:
            db.session.rollback()
            return render_template('result.html', login_form=login_form, register_form=register_form, register_msg=f'Registration failed, error: {str(e)}')

    return render_template('student.html', login_form=login_form, register_form=register_form)

# back
# register 注册   http://127.0.0.1:5000  应该也返回这个       http://127.0.0.1:5000/register/
# register比login复杂    GET 请求通常用于从服务器获取数据或者显示一个页面 POST 请求通常用于当用户提交表单数据到服务器
@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Register function called")  # 调试语句
    register_form = RegisterForm()
    
    if register_form.validate_on_submit():
        try:
            username = register_form.username.data
            password = register_form.password.data
            email = register_form.email.data
            new_user = User(name=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('some_success_page'))
        except Exception as e:
            db.session.rollback()
            return render_template("error.html", message=f"Registration failed, error: {str(e)}")

    return render_template("student.html", register_form=register_form)



# @app.route('/register/', methods=['POST', 'GET'])
# def register():
#     register_form = RegisterForm()
    
#     if register_form.validate_on_submit():  # 检查是否是POST请求并且是否通过验证
#         try:
#             username = register_form.username.data
#             password = register_form.password.data
#             email = register_form.email.data

#             new_user = User(name=username, email=email)
#             new_user.set_password(password)  # 假设你有一个设置密码的方法，它也应该处理密码散列
#             db.session.add(new_user)
#             db.session.commit()
#             return render_template("result.html", msg="Registration successful")
#         except Exception as e:
#             db.session.rollback()
#             return render_template("result.html", msg=f"Registration failed, error: {str(e)}")

#     return render_template("student.html", register_form=register_form)

# def register():
#     # from models import User
#     if request.method == 'POST':
#         try:
#             username = request.form['name']
#             password = request.form['password']
#             email = request.form['email']

#             new_user = User(name=username, password=password, email=email)
#             new_user.set_password(password)  # 设置哈希密码
#             db.session.add(new_user)
#             db.session.commit()
#             msg = "Registration successful"
#         except Exception as e:
#             db.session.rollback()
#             msg = f"Registration failed, error: {str(e)}"
#             return render_template("result.html", msg=msg)
#         return render_template("result.html", msg=msg)
#     else:
#         return render_template("student.html")



login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))



# login   登录    http://127.0.0.1:5000  应该也返回这个    login    http://127.0.0.1:5000/login/
@app.route('/login/', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.query.filter_by(name=username).first()
        if user and user.check_password(password):
            login_user(user)
            session['loggedin'] = True
            session['username'] = user.name
            return render_template('main.html', msg='Login successful!')  
            # return redirect(url_for('index'))  # 假设你有一个名为 'index' 的视图函数
        else:
            return render_template('result.html', form=login_form, msg='Incorrect username or password！')
    return render_template('login.html', login_form=login_form)
# def login():
#     msg = ''
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(name=username).first()
#         # user = User.query.filter_by(name=username, password=password).first()
#         if user and user.check_password(password):
#             login_user(user)  # 使用 Flask-Login 登录用户
#             session['loggedin'] = True  # 设置 session 中的登录标记
#             session['username'] = user.name  # 保存用户的用户名到 session
#             return render_template('main.html', msg='Login successful!')        
#         else:
#             # 登录失败，设置错误消息
#             msg = 'Incorrect username or password！'
#         # 登录失败时返回登录页面，并显示错误信息
#         return render_template("result.html", msg=msg)  # 确保你有一个 login.html 模板
#     # 如果不是POST请求，渲染登录表单页面
#     return redirect(url_for('login'))





    

    










































# 先留着       这个甚至     可能不需要吧 
# @app.route('/logout/')
# def logout():
#     # 移除会话中的用户信息
#     session.pop('loggedin', None)
#     session.pop('username', None)
#     return redirect(url_for('login'))

# 先留着           显示所有学生的路由   显示出来    这个是为了检查  好看    http://127.0.0.1:5000/show/ 
# @app.route('/show/')
# def show_student():
#     con = sqlite3.connect("database.db")  
#     con.row_factory = sqlite3.Row      #设置row_factory,对查询到的数据，通过字段名获取列数据
#     cur = con.cursor()        
#     cur.execute("select * from students")   
#     rows = cur.fetchall()      #获取多条记录数据   
#     return render_template("show.html",rows = rows)  #渲染show.html模板并传递rows值

# 先留着       http://127.0.0.1:5000/errorPage/
@app.route('/errorPage')
def errorPage():
    # 这里可以展示错误信息或提供错误反馈
    return "There is an error and please try later"




# 这是一个测试       没有路径    只是    http://127.0.0.1:5000      @app.route('/')def index():  return "Hello, World!"
@app.route('/')
def regi_login():
    return render_template('student.html')




































# 几个view    和后端息息相关        http://127.0.0.1:5000/main/
@app.route('/main')
def main():
    #  如果没有用户名就不显示错误信息，并且不执行需要登录的操作            这是最开始  没问题的
    return render_template('main.html')

class RequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

# 发起帖子        http://127.0.0.1:5000/createRequest/
@app.route('/createRequest', methods=['GET', 'POST'])
def createRequest():
    form = RequestForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        username = session.get('username')

        if not username:
            return redirect(url_for('login'))

        new_request = Request(title=title, description=description, username=username)
        db.session.add(new_request)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('createRequest.html', form=form)

# def createRequest():
#     if request.method == 'POST':
#         try:
#             title = request.form['title']
#             description = request.form['description']
#             username = session.get('username')

#             # 检查用户是否登录
#             if not username:
#                 return redirect(url_for('login'))

#             # 创建一个新的请求实例
#             new_request = Request(title=title, description=description, username=username)
#             db.session.add(new_request)  # 添加到数据库会话
#             db.session.commit()  # 提交更改

#             # 操作成功，重定向到查找请求的页面或回到主页
#             return redirect(url_for('main'))  # 只需要一个重定向

#         except Exception as e:
#             # 处理异常，可以记录到日志，并向用户显示错误信息
#             print(f"Failed to create request, error: {e}")
#             return render_template('errorPage.html', error=str(e))
#     else:
#         # 如果不是POST请求，则渲染创建请求的页面
#         return render_template('createRequest.html')


def model_to_dict(model):
    return {column.name: getattr(model, column.name) for column in model.__table__.columns}

class ReplyForm(FlaskForm):
    reply = TextAreaField('Reply', validators=[DataRequired()])

#  搜索帖子       http://127.0.0.1:5000/main/          @app.route('/findRequest')
@app.route('/findRequest')
def findRequest():
    # print("Request object:", request)
    search_queryFR = request.args.get('searchQueryFR', '').strip()
    rows = []
    message = ''
    if search_queryFR:
        try:
            matched_requests = Request.query.filter(Request.title.like('%' + search_queryFR + '%')).all()
            rows = []
            for req in matched_requests:
                row = model_to_dict(req)  # 将每个请求转换为字典
                # 获取与此请求相关的所有回复
                replies = Reply.query.filter_by(request_id=req.id).all()
                row['replies'] = [model_to_dict(reply) for reply in replies]

                # 为此请求实例化一个回复表单
                row['form'] = ReplyForm()

                # 添加到结果列表
                rows.append(row)

            # matched_requests = Request.query.filter(Request.title.like('%' + search_queryFR + '%')).all()
            # rows = [r.as_dict() for r in matched_requests]
            # for row in rows:
            #     form = ReplyForm()  # 为每个请求创建一个回复表单实例
            #     row['form'] = form

            if not rows:
                message = 'No matching requests found.'
        except Exception as e:
            message = 'An issue occurred during the search process.'
            print(f"Search request failed, error: {e}")
    else:
        requests  = Request.query.order_by(Request.title).limit(5).all()
        # rows = [r.as_dict() for r in rows]
        rows = []
        for req in requests:  # 改变变量名以避免覆盖全局 request 对象
            row = model_to_dict(req)
            # 获取与此请求相关的所有回复
            replies = Reply.query.filter_by(request_id=req.id).all()
            row['replies'] = [model_to_dict(reply) for reply in replies]

            # 为此请求实例化一个回复表单
            row['form'] = ReplyForm()

            # 添加到结果列表
            rows.append(row)

        # for request in requests :
        #     row = model_to_dict(row)
        #     # 获取与此请求相关的所有回复
        #     replies = Reply.query.filter_by(request_id=request.id).all()
        #     row['replies'] = [model_to_dict(reply) for reply in replies]

        #     # 为此请求实例化一个回复表单
        #     row['form'] = ReplyForm()

        #     # 添加到结果列表
        #     rows.append(row)

        #     # form = ReplyForm()
        #     # row['form'] = form
    return render_template('findRequest.html', rows=rows, message=message, search_queryFR=search_queryFR)



# def findRequest():
#     search_queryFR = request.args.get('searchQueryFR', '').strip()
#     rows = []
#     message = ''

#     if search_queryFR:
#         try:
#             # 使用SQLAlchemy ORM进行模糊搜索
#             matched_requests = Request.query.filter(Request.title.like('%' + search_queryFR + '%')).all()
#             rows = [r.as_dict() for r in matched_requests]  # 假设 Request 模型有 as_dict 方法来转换对象为字典

#             # 对每个匹配的请求，获取相关回复
#             for row in rows:
#                 replies = Reply.query.filter_by(request_id=row['id']).all()
#                 row['replies'] = [reply.as_dict() for reply in replies]

#             if not rows:
#                 message = 'No matching requests found.'


#         except Exception as e:
#             message = 'An issue occurred during the search process.'
#             print(f"Search request failed, error: {e}")
#     else:
#         # 如果没有提供搜索查询，直接加载前五个请求
#         rows = Request.query.order_by(Request.title).limit(5).all()
#         rows = [r.as_dict() for r in rows]
#         # 对这五个请求也获取相关回复
#         for row in rows:
#             replies = Reply.query.filter_by(request_id=row['id']).all()
#             row['replies'] = [reply.as_dict() for reply in replies]
#     return render_template('findRequest.html', rows=rows, message=message, search_queryFR=search_queryFR)

# def findRequest():
#     search_queryFR = request.args.get('searchQueryFR', '').strip()
#     rows = []
#     message = ''
#     if search_queryFR:
#         try:
#             with sqlite3.connect("database.db") as con:
#                 con.row_factory = sqlite3.Row
#                 cur = con.cursor()
#                 cur.execute("SELECT * FROM requests WHERE title LIKE ?", ('%'+search_queryFR+'%',))
#                 rows = [dict(row) for row in cur.fetchall()]

#                 for row in rows:
#                     cur.execute("SELECT * FROM replies WHERE request_id=?", (row["id"],))
#                     row["replies"] = [dict(reply) for reply in cur.fetchall()]

#                 if not rows:
#                     message = 'No matching requests found.'
#         except Exception as e:
#             message = 'An issue occurred during the search process.'
#             print(f"Search request failed, error: {e}")

#     # 注意这里将 search_queryFR 变量回传给模板
#     return render_template('findRequest.html', rows=rows, message=message, search_queryFR=search_queryFR)
























# reply          回复 帖子       点击submit reply的button            请求的路由（示例）
@app.route('/replyRequest', methods=['GET', 'POST'])
def replyRequest():
    if request.method == 'POST':
        reply_content = request.form['reply']
        responderName = session.get('username')
        request_title = request.form.get('search_queryFR')
        request_id = request.form.get('request_id')

        if not responderName:
            # 用户未登录或会话已过期
            return redirect(url_for('login'))
        
        if reply_content and request_title and request_id:
        # if reply_content and request_id:
                    # 使用request_title和request_id同时进行查询，确保精确匹配
            matching_request = Request.query.filter(
                        Request.title.like('%' + request_title + '%'),
                        Request.id == request_id  # 确保ID也匹配
                    ).first()
        # if reply_content and request_title:
        #     # 使用 SQLAlchemy 查询请求
        #     matching_request = Request.query.filter(Request.title.like('%' + request_title + '%')).first()
            
            if matching_request:
                # 创建回复
                # new_reply = Reply(request_id=matching_request.id, reply_content=reply_content, responderName=responderName)
                new_reply = Reply(request_id=matching_request.id, reply_content=reply_content, responderName=responderName)
                db.session.add(new_reply)
                db.session.commit()

                return redirect(url_for('findRequest'))
            else:
                return render_template('findRequest.html', error="Cannot find the request")

        else:
            return render_template('findRequest.html', error="Reply content cannot be empty")

    else:
        request_title = request.args.get('search_queryFR')
        return render_template('findRequest.html', request_title=request_title)
# def replyRequest():
#     if request.method == 'POST':
#         reply_content = request.form['reply']
#         responderName = session['username']
#         # 假设 'search_queryFR' 是表单字段，用户提交的是请求的标题
#         request_title = request.form.get('search_queryFR')

#         if reply_content:
#             with sqlite3.connect("database.db") as con:
#                 cur = con.cursor()
#                 # 首先根据标题找到请求的 ID
#                 # cur.execute("SELECT id FROM requests WHERE title = ?", (request_title,))   这是完全匹配   不完善
#                 cur.execute("SELECT id FROM requests WHERE title LIKE ?", ('%' + request_title + '%',))
#                 result = cur.fetchone()  #  没有回复   是none

#                 # 检查是否找到了对应的请求
#                 if result:
#                     request_id = result[0]

#                     # 然后像之前一样处理回复逻辑
#                     cur.execute("INSERT INTO replies (request_id, reply_content, answerName) VALUES (?, ?, ?)",
#                                 (request_id, reply_content, responderName))
#                     con.commit()

#                     return redirect(url_for('findRequest'))
#                 else:
#                     # 如果根据标题找不到请求，返回错误消息
#                     return render_template('findRequest.html', error="can not find the request")
#         else:
#             return render_template('findRequest.html', error="can not be empty")
#     else:
#         # 对于 GET 请求，从 URL 参数中获取标题      注意：这里的参数名应该与POST请求中表单字段的名称保持一致
#         request_title = request.args.get('search_queryFR')
#         return render_template('findRequest.html', request_title=request_title)










@app.route('/student')
def student():
    register_form = RegisterForm()
    login_form = LoginForm()  # 创建登录表单实例
    # 确保将 login_form 也传递给模板
    return render_template('student.html', register_form=register_form, login_form=login_form)



class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')

# 这里是对的    user和email   需要匹配   点击Forget my password  仅仅跳转界面 
@app.route('/forgot_password')
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    return render_template('forgotPassword.html', form=form)

# def forgot_password():
#     # 渲染忘记密码的 HTML 表单
#     return render_template('forgotPassword.html')


# button   仅仅发送邮件     比如发送到我qq邮箱   检查这个邮箱   是不是在数据库里面
@app.route('/send_link', methods=['POST'])
def sendLink():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            from passwordReset import PasswordResetService
            PasswordResetService.sendUpdatePassword(email)
            flash("Send the email, please check personal email", 'success')
            return redirect(url_for('student'))
        else:
            flash("This email is not in Database", 'danger')
            return render_template('forgotPassword.html', form=form)
    return render_template('forgotPassword.html', form=form) 

# def sendLink():
#     email = request.form['email']
#     user = User.query.filter_by(email=email).first()

#     if user:
#         from passwordReset import PasswordResetService
#         PasswordResetService.sendUpdatePassword(email)
#         return render_template('student.html', message="Send the email, please check personal email")
#     else:
#         return render_template('forgotPassword.html', error="This email is not in Database")
    
# def sendLink():
#     if request.method == 'POST':
#         email = request.form['email']

#         # Use SQLAlchemy ORM to query the user
#         user = User.query.filter_by(email=email).first()

#         # Check if the user exists and send the password reset email
#         if user:
#             from passwordReset import PasswordResetService
#             PasswordResetService.sendUpdatePassword(email)
#             return render_template('student.html', message="Send the email, please check personal email")
#         else:
#             return render_template('forgotPassword.html', error="This email is not in Database")
            
#     return render_template('forgotPassword.html')


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


# 使用9    qq邮箱
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    register_form = RegisterForm()
    login_form = LoginForm()
    if form.validate_on_submit():
        new_password = form.new_password.data
        from passwordReset import PasswordResetService  # 确保导入路径正确
        email = PasswordResetService.verify_reset_token(token)
        if email is None:
            flash('The reset token is invalid or has expired.', 'error')
            return redirect(url_for('reset_request'))
        PasswordResetService.update_password(email, new_password)
        flash('Your password has been updated!', 'success')
        return redirect(url_for('student'))
    return render_template('reset_password.html', form=form, register_form=register_form, login_form=login_form, token=token)


    # # register_form = RegisterForm()
    # # login_form = LoginForm()
    # form = ResetPasswordForm()  # 使用新的表单类
    # if form.validate_on_submit():  # 处理表单提交
    #     new_password = form.new_password.data
    #     from passwordReset import PasswordResetService
    #     email = PasswordResetService.verify_reset_token(token)
    #     if email is None:
    #         flash('The reset token is invalid or has expired.', 'error')
    #         return redirect(url_for('reset_request'))
    #     PasswordResetService.update_password(email, new_password)
    #     flash('Your password has been updated!', 'success')
    #     return redirect(url_for('user_views.user'))
    # return render_template('reset_password.html', form=form, token=token)

# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     register_form = RegisterForm()
#     login_form = LoginForm()
#     if request.method == 'GET':
#         # 仅 GET 请求需要渲染表单
#         return render_template('reset_password.html', token=token, register_form=register_form, login_form=login_form)
    
#     # if request.method == 'GET':
#     #     # 正确地生成 CSRF 令牌并传递到模板
#     #     return render_template('reset_password.html', token=token, csrf_token=generate_csrf())

#     # 处理 POST 请求，提交新密码
#     new_password = request.form.get('new_password')
#     if not new_password:
#         flash('No new password provided.', 'error')
#         return redirect(url_for('reset_password', token=token, register_form=register_form, login_form=login_form))
#         # return redirect(url_for('reset_password', token=token))  # 确保使用正确的重定向

#     from passwordReset import PasswordResetService
#     email = PasswordResetService.verify_reset_token(token)
#     if email is None:
#         flash('The reset token is invalid or has expired.', 'error')
#         return redirect(url_for('reset_request'))  # 确保重定向到请求重置页面

#     # 更新密码
#     PasswordResetService.update_password(email, new_password)
#     flash('Your password has been updated!', 'success')
#     return redirect(url_for('user_views.user'))  # 确保 user_views.user 是正确的端点


# 在qq邮箱里面     打开链接                         delete  输入新的密码       点击   reset button  新密码替换
# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if request.method == 'GET':
#         # If it's a GET request, just render the reset_password.html template with the token
#         return render_template('reset_password.html', token=token, csrf_token=generate_csrf())
#         return render_template('reset_password.html', token=token)

#     # 输入新的密码        If it's a POST request, process the form submission
#     new_password = request.form['new_password']
#     if not new_password:
#         flash('No new password provided.', 'error')
#         return redirect(url_for('reset_password', token=token))  # Redirect back to the same page
#     from passwordReset import PasswordResetService
#     email = PasswordResetService.verify_reset_token(token)
#     if email is None:
#         flash('The reset token is invalid or has expired.', 'error')
#         return redirect(url_for('reset_request'))  # Redirect to the request reset page

#     # 更新      At this point, we have a valid email and new password
#     PasswordResetService.update_password(email, new_password)
#     flash('Your password has been updated!', 'success')
#     return redirect(url_for('user_views.user'))
# Redirect to the login page after success





#  可能不用了  debug看看是否进入    用reset_password替换了   qq邮箱  打开网页   输入新的密码   submit
@app.route('/change_password', methods=['POST'])
def change_password():
    token = request.args.get('token')  # 或者从表单中获取 token，如果它是以隐藏字段传递的
    new_password = request.form['new_password']
    if not new_password:
        flash('No new password provided.', 'error')  # 没有提供新密码
        return redirect(url_for('reset_request'))  # 重定向回重置请求页面
    from passwordReset import PasswordResetService
    email = PasswordResetService.verify_reset_token(token)
    if email is None:
        flash('The reset token is invalid or has expired.', 'error')
        return redirect(url_for('reset_request'))  # 重定向回重置请求页面

    if not email:  # 这是一个额外的检查，以防 email 为空字符串
        flash('The email is invalid.', 'error')
        return redirect(url_for('reset_request'))  # 重定向回重置请求页面

    # 在这里，我们已经验证了 email 不是 None 也不是空字符串
    PasswordResetService.update_password(email, new_password)
    flash('Your password has been updated!', 'success')
    return redirect(url_for('login'))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from passwordReset import PasswordResetService
    app.password_reset_service = PasswordResetService()

    return app













# back   可能要用部分




# if __name__ == "__main__":
#     # print(app.url_map)     这是一个测试     打印出来  app.url_map  print(app.url_map+'999')
#     # app.run(debug=True)
#     from models import *
#     db.create_all()
#     app.run(debug=True)
from app import app, db
from models import User,Request,Reply
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
# # app.py 的末尾
# from views import *  # 或者具体的视图函数

