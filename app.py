from flask import Flask, request, render_template, redirect, url_for, session,make_response, flash
import sqlite3
# from passwordReset import PasswordResetService
from flask_mail import Mail
import os
from routes import UserViews
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from models import User  # 确保从 models.py 导入了 User
# from app import app, db


# 项目启动       student.html 这是主界面  名字没事
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate = Migrate(app,db)
app.secret_key = 'your_secret_key'  # 用于保持会话安全
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


# back
# register 注册   http://127.0.0.1:5000  应该也返回这个       http://127.0.0.1:5000/register/
# register比login复杂    GET 请求通常用于从服务器获取数据或者显示一个页面 POST 请求通常用于当用户提交表单数据到服务器
# @app.route('/register/', methods=['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#         try:
#             # form get   从表单请求中获取用户名、密码和邮箱的数据
#             username = request.form['name']
#             password = request.form['password']
#             email = request.form['email']
#             with sqlite3.connect("database.db") as con:
#                 cur = con.cursor()  
#                 cur.execute("INSERT INTO users (name, password, email) VALUES (?, ?, ?)", (username, password, email))
#                 con.commit()  
#                 msg = "Registration successful"
#         except Exception as e:
#             # 如果执行到这里，说明 'con' 已经被定义了，我们在 'with' 语句内部
#             msg = f"Registration failed, error: {str(e)}"  # 设置错误消息
#             return render_template("result.html", msg=msg)  # 使用同一个结果页面来显示错误消息
#         # 成功的情况下也返回结果页面，并传递成功消息
#         return render_template("result.html", msg=msg)
#     else:
#         # 如果不是POST请求，则渲染注册表单的页面
#         # 用户首次访问你的注册页面，他们还没有提交任何信息。在这种情况下，他们是通过 GET 请求来访问页面的。
#         # 这时候，你的代码中的 else 部分会执行，并显示注册表单，允许用户输入他们的信息
#         return render_template("student.html")
#         # return render_template("register.html")

@app.route('/register/', methods=['POST', 'GET'])
def register():
    # from models import User
    if request.method == 'POST':
        try:
            username = request.form['name']
            password = request.form['password']
            email = request.form['email']

            new_user = User(name=username, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()
            msg = "Registration successful"
        except Exception as e:
            db.session.rollback()
            msg = f"Registration failed, error: {str(e)}"
            return render_template("result.html", msg=msg)
        return render_template("result.html", msg=msg)
    else:
        return render_template("student.html")





# login   登录    http://127.0.0.1:5000  应该也返回这个    login    http://127.0.0.1:5000/login/
@app.route('/login/', methods=['POST', 'GET'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(name=username, password=password).first()
        if user:
            # 用户验证成功，设置用户会话
            session['loggedin'] = True
            session['username'] = user.name
            msg = 'Login successful!'
            # 登录成功后重定向到主页面
            return render_template('main.html', msg=msg)
        else:
            # 登录失败，设置错误消息
            msg = 'Incorrect username or password！'
        # 登录失败时返回登录页面，并显示错误信息
        return render_template("result.html", msg=msg)  # 确保你有一个 login.html 模板
    # 如果不是POST请求，渲染登录表单页面
    return redirect(url_for('login'))
    # return render_template("login.html", msg=msg)
# @app.route('/login/', methods=['POST', 'GET'])
# def login():
#     # 默认情况下，假设没有错误消息
#     msg = ''
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         try:
#             with sqlite3.connect("database.db") as con:
#                 con.row_factory = sqlite3.Row
#                 cur = con.cursor()
#                 cur.execute("SELECT * FROM users WHERE name = ? AND password = ?", (username, password))

#                 user = cur.fetchone()
#                 if user:
#                     # 用户验证成功，设置用户会话
#                     session['loggedin'] = True
#                     session['username'] = user['name']
#                     msg = 'Login successful!'
#                     # 登录成功后   保存   测试
#                     session['username'] = username  # 假设这是登录视图函数中的代码
#                     # login   登录成功     
#                     return render_template('main.html', msg=msg)
#                     # return redirect(url_for('main'))
#                 else:
#                     # 登录失败，设置错误消息
#                     msg = 'Incorrect username or password！'
#         except Exception as e:
#             # 处理异常，设置错误消息
#             msg = f"Error: {str(e)}"
#         # 登录失败或发生异常，使用同一个结果页面来显示错误消息
#         return render_template("result.html", msg=msg)
#     # 如果不是POST请求，或者出现其他情况，重定向到登录页面
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

# 发起帖子        http://127.0.0.1:5000/createRequest/
@app.route('/createRequest', methods=['GET', 'POST'])
def createRequest():
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            username = session.get('username')

            # 检查用户是否登录
            if not username:
                return redirect(url_for('login'))

            # 创建一个新的请求实例
            new_request = Request(title=title, description=description, username=username)
            db.session.add(new_request)  # 添加到数据库会话
            db.session.commit()  # 提交更改

            # 操作成功，重定向到查找请求的页面或回到主页
            return redirect(url_for('main'))  # 只需要一个重定向

        except Exception as e:
            # 处理异常，可以记录到日志，并向用户显示错误信息
            print(f"Failed to create request, error: {e}")
            return render_template('errorPage.html', error=str(e))
    else:
        # 如果不是POST请求，则渲染创建请求的页面
        return render_template('createRequest.html')
# def createRequest():
#     if request.method == 'POST':  
#         try:
#             # 从表单请求中获取标题和描述的数据
#             title = request.form['title']
#             description = request.form['description']
#             # 从会话中获取username
#             username = session.get('username')
#             # 确保在登录后才能创建请求    这个更严谨
#             # if not username:
#             #     # 可能需要重定向到登录页面或显示错误消息
#             #     return redirect(url_for('login'))
#             with sqlite3.connect("database.db") as con:
#                 cur = con.cursor()  # 获取游标
#                 # 将请求信息添加到数据库，包括用户名
#                 cur.execute("INSERT INTO requests (title, description, username) VALUES (?, ?, ?)", (title, description, username))
#                 con.commit()  
#                 # 操作成功，这里有两个重定向，只需要一个    重定向到查找请求的页面或回到主页
#                 return redirect(url_for('main'))
#                 return render_template('main.html')
#                 return redirect(url_for('findRequest'))  # 假设你有一个叫做findRequest的视图函数来显示所有请求
#         except Exception as e:
#             print(f"Failed to create request, error: {e}")
#             return redirect(url_for('main', error=str(e)))
#             return render_template('main.html', error=str(e))
#             return render_template('errorPage.html', error=str(e))
        
#     else:
#         # 啥有没干
#         # 如果不是POST请求，则渲染创建请求的页面
#         # response = make_response(render_template('createRequest.html'))
#         # # Prevent caching the form page to avoid resubmission issues
#         # response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
#         # response.headers['Pragma'] = 'no-cache'  # HTTP 1.0 compatibility
#         # response.headers['Expires'] = '0'  # Proxies
#         # return response
        
#         return render_template('createRequest.html')





#  搜索帖子       http://127.0.0.1:5000/main/          @app.route('/findRequest')
@app.route('/findRequest')
def findRequest():
    search_queryFR = request.args.get('searchQueryFR', '').strip()
    rows = []
    message = ''

    if search_queryFR:
        try:
            # 使用SQLAlchemy ORM进行模糊搜索
            matched_requests = Request.query.filter(Request.title.like('%' + search_queryFR + '%')).all()
            rows = [r.as_dict() for r in matched_requests]  # 假设 Request 模型有 as_dict 方法来转换对象为字典

            # 对每个匹配的请求，获取相关回复
            for row in rows:
                replies = Reply.query.filter_by(request_id=row['id']).all()
                row['replies'] = [reply.as_dict() for reply in replies]

            if not rows:
                message = 'No matching requests found.'


        except Exception as e:
            message = 'An issue occurred during the search process.'
            print(f"Search request failed, error: {e}")

    return render_template('findRequest.html', rows=rows, message=message, search_queryFR=search_queryFR)
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
























# reply          回复 帖子                 请求的路由（示例）
@app.route('/replyRequest', methods=['GET', 'POST'])
def replyRequest():
    if request.method == 'POST':
        reply_content = request.form['reply']
        responderName = session.get('username')
        request_title = request.form.get('search_queryFR')

        if not responderName:
            # 用户未登录或会话已过期
            return redirect(url_for('login'))

        if reply_content and request_title:
            # 使用 SQLAlchemy 查询请求
            matching_request = Request.query.filter(Request.title.like('%' + request_title + '%')).first()
            
            if matching_request:
                # 创建回复
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















# 这里是对的    user和email   需要匹配   点击Forget my password  仅仅跳转界面 
@app.route('/forgot_password')
def forgot_password():
    # 渲染忘记密码的 HTML 表单
    return render_template('forgotPassword.html')


# button   仅仅发送邮件     比如发送到我qq邮箱   检查这个邮箱   是不是在数据库里面
@app.route('/send_link', methods=['POST'])
def sendLink():
    if request.method == 'POST':
        email = request.form['email']

        # Use SQLAlchemy ORM to query the user
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and send the password reset email
        if user:
            from passwordReset import PasswordResetService
            PasswordResetService.sendUpdatePassword(email)
            return render_template('student.html', message="Send the email, please check personal email")
        else:
            return render_template('forgotPassword.html', error="This email is not in Database")
            
    return render_template('forgotPassword.html')
# def sendLink():
#     if request.method == 'POST':
#         email = request.form['email']
#         con = sqlite3.connect("database.db")
#         cur = con.cursor()
#         cur.execute("SELECT * FROM users WHERE email = ?", (email,))
#         user = cur.fetchone()
#         # 根据这个email     查询到  user存在    PasswordResetService类    
#         if user:
#             PasswordResetService.sendUpdatePassword(email)
#             return render_template('student.html', message="Send the email, please check personal email")
#         # 只跳转到student.html  避免有困惑 return render_template('notification.html', message="重置邮件发送，检查邮箱")
#         else:
#             return render_template('forgotPassword.html', error="This email is not in Database")
#     return render_template('forgotPassword.html')


# qq邮箱  打开链接                                        delete  输入新的密码       点击   reset button  新密码替换
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'GET':
        # If it's a GET request, just render the reset_password.html template with the token
        return render_template('reset_password.html', token=token)

    # 输入新的密码        If it's a POST request, process the form submission
    new_password = request.form['new_password']
    if not new_password:
        flash('No new password provided.', 'error')
        return redirect(url_for('reset_password', token=token))  # Redirect back to the same page
    from passwordReset import PasswordResetService
    email = PasswordResetService.verify_reset_token(token)
    if email is None:
        flash('The reset token is invalid or has expired.', 'error')
        return redirect(url_for('reset_request'))  # Redirect to the request reset page

    # 更新      At this point, we have a valid email and new password
    PasswordResetService.update_password(email, new_password)
    flash('Your password has been updated!', 'success')
    return redirect(url_for('user_views.user'))
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
from models import User,Request,Reply,Like
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
# # app.py 的末尾
# from views import *  # 或者具体的视图函数

