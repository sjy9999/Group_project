from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
# 项目启动
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于保持会话安全


# 先打开   这个界面   注册学生账号       这是   http://127.0.0.1:5000/create/
@app.route('/create/')
def create_student():
    return render_template('student.html')  #渲染student.html模板



# 添加学生的路由，支持POST和GET请求    @app.route('/addstudent/')     http://127.0.0.1:5000/addstudent/
@app.route('/addstudent/',methods = ['POST', 'GET'])
def add_student():
    try:
        #获取请求中的nm、add、city、pin的数据
        nm = request.form['nm']
        addr = request.form['add']
        city = request.form['city']
        pin = request.form['pin']
        #连接    建立与database.db数据库的连接
        with sqlite3.connect("database.db") as con:  
           cur = con.cursor()    #获取游标
           #添加数据，执行单条的sql语句
        #    cur.execute("IN INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )   
           cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )                
           con.commit()     #提交事务
           msg = "添加这个新的学生   成功"
    except:
        con.rollback()
        #撤消当前事务中所做的所有更改
        #要故意触发 except 块，你可以：
        # 断开数据库连接：移除或重命名 database.db 文件。
        # 修改 SQL 语句，使其含有错误：改变列名为一个不存在的列名。
        # 传入不合法的数据：比如对于一个要求整数的字段，传入一个文本字符串
        msg = "添加这个新的学生   失败"
    finally:
        # 这个才是对的
        if con:
            con.close()
        # 改url_for       而不是返回html
        return redirect(url_for('show_student'))


# http://127.0.0.1:5000    返回这个   form action    register    http://127.0.0.1:5000/register/
# register比login复杂    GET 请求通常用于从服务器获取数据或者显示一个页面 POST 请求通常用于当用户提交表单数据到服务器
@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            # 从表单请求中获取用户名、密码和邮箱的数据
            username = request.form['name']
            password = request.form['password']
            email = request.form['email']
            # 连接数据库
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()  # 获取游标
                # 添加用户数据，执行单条的SQL语句
                cur.execute("INSERT INTO users (name, password, email) VALUES (?, ?, ?)", (username, password, email))
                con.commit()  # 提交事务
                msg = "注册成功"
        except Exception as e:
            # 如果执行到这里，说明 'con' 已经被定义了，我们在 'with' 语句内部
            msg = f"注册失败，错误: {str(e)}"  # 设置错误消息
            return render_template("result.html", msg=msg)  # 使用同一个结果页面来显示错误消息
        # 成功的情况下也返回结果页面，并传递成功消息
        return render_template("result.html", msg=msg)
        

    else:
        # 如果不是POST请求，则渲染注册表单的页面
        # 用户首次访问你的注册页面，他们还没有提交任何信息。在这种情况下，他们是通过 GET 请求来访问页面的。
        # 这时候，你的代码中的 else 部分会执行，并显示注册表单，允许用户输入他们的信息
        return render_template("student.html")
        # return render_template("register.html")



# http://127.0.0.1:5000    返回这个   form action   login    http://127.0.0.1:5000/login/
@app.route('/login/', methods=['POST', 'GET'])
def login():
    # 默认情况下，假设没有错误消息
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            # 连接数据库
            with sqlite3.connect("database.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                # 修改查询语句中的列名为实际的列名
                cur.execute("SELECT * FROM users WHERE name = ? AND password = ?", (username, password))

                user = cur.fetchone()
                if user:
                    # 用户验证成功，设置用户会话
                    session['loggedin'] = True
                    session['username'] = user['name']
                    msg = '登录成功！'
                    # 登录成功后   保存   测试
                    session['username'] = username  # 假设这是登录视图函数中的代码
                    # login   登录成功     重定向到主界面或其他页面，取决于你的应用逻辑
                    return render_template('main.html', msg=msg)
                    # return redirect(url_for('main'))
                else:
                    # 登录失败，设置错误消息
                    msg = '用户名或密码错误！'
        except Exception as e:
            # 处理异常，设置错误消息
            msg = f"错误: {str(e)}"
        # 登录失败或发生异常，使用同一个结果页面来显示错误消息
        return render_template("result.html", msg=msg)
    # 如果不是POST请求，或者出现其他情况，重定向到登录页面
    return redirect(url_for('login'))





    

    










































# 这个甚至     可能不需要吧
@app.route('/logout/')
def logout():
    # 移除会话中的用户信息
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


# 显示所有学生的路由   显示出来    这个是为了检查  好看    http://127.0.0.1:5000/show/ 
@app.route('/show/')
def show_student():
    con = sqlite3.connect("database.db")  #建立数据库连接
    con.row_factory = sqlite3.Row      #设置row_factory,对查询到的数据，通过字段名获取列数据
    cur = con.cursor()        #获取游标
    cur.execute("select * from students")   #执行sql语句选择数据表
    rows = cur.fetchall()      #获取多条记录数据   
    return render_template("show.html",rows = rows)  #渲染show.html模板并传递rows值


# 这是一个测试       没有路径    只是    http://127.0.0.1:5000
# @app.route('/')
# def index():
#     return "Hello, World!"
@app.route('/')
def regi_login():
    return render_template('student.html')


# http://127.0.0.1:5000/errorPage/
@app.route('/errorPage')
def errorPage():
    # 这里可以展示错误信息或提供错误反馈
    return "出错了！请稍后重试。"

































# 剩余3个view    和后端息息相关
# http://127.0.0.1:5000/main/
@app.route('/main')
def main():
    return render_template('main.html')

# http://127.0.0.1:5000/createRequest/
@app.route('/createRequest', methods=['GET', 'POST'])
def createRequest():
    if request.method == 'POST':  
        try:
            # 从表单请求中获取标题和描述的数据
            title = request.form['title']
            description = request.form['description']
            # 从会话中获取username
            username = session.get('username')
            # 确保在登录后才能创建请求
            # if not username:
            #     # 可能需要重定向到登录页面或显示错误消息
            #     return redirect(url_for('login'))

            # 连接数据库
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()  # 获取游标
                # 将请求信息添加到数据库，包括用户名
                cur.execute("INSERT INTO requests (title, description, username) VALUES (?, ?, ?)", (title, description, username))
                con.commit()  # 提交事务
                # 操作成功，这里你有两个重定向，只需要一个
                # 重定向到查找请求的页面或回到主页
                return render_template('main.html')
                return redirect(url_for('findRequest'))  # 假设你有一个叫做findRequest的视图函数来显示所有请求
        except Exception as e:
            print(f"创建请求失败，错误: {e}")
            return render_template('main.html', error=str(e))
            return render_template('errorPage.html', error=str(e))
             
        try:
            # 从表单请求中获取标题和描述的数据
            title = request.form['title']
            description = request.form['description']
            # 连接数据库
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()  # 获取游标
                # requests        将请求信息添加到数据库
                cur.execute("INSERT INTO requests (title, description) VALUES (?, ?)", (title, description))
                con.commit()  # 提交事务
                # 操作成功，重定向到查找请求的页面
                return render_template('main.html')
                return redirect(url_for('findRequest'))
        except Exception as e:
            # 如果操作失败，可能是数据库连接问题或执行SQL语句有误
            print(f"创建请求失败，错误: {e}")  # 打印错误信息，实际应用中应考虑记录日志
            # 操作失败，也可以选择重定向到某个页面，或返回错误信息
            return render_template('main.html')
            return redirect(url_for('errorPage'))  # 假设有一个显示错误的页面
    else:
        # 如果不是POST请求，则渲染创建请求的页面
        return render_template('createRequest.html')


# http://127.0.0.1:5000/main/
@app.route('/findRequest')
def findRequest():
    search_queryFR = request.args.get('searchQueryFR', '').strip()
    # search_query = request.args.get('searchQuery', '')  # 获取搜索关键词
    rows = []
    message = ''  # 初始化消息为空字符串

    if search_queryFR:
        try:
            with sqlite3.connect("database.db") as con:
                con.row_factory = sqlite3.Row  # 使行为字典
                cur = con.cursor()
                # 只根据标题搜索requests表
                cur.execute("SELECT * FROM requests WHERE title LIKE ?", ('%'+search_queryFR+'%',))
                rows = cur.fetchall()  # 获取所有查询结果
                if not rows:  # 如果没有找到任何行
                    message = '未找到匹配的请求。'  # 设置消息为“未找到”
        except Exception as e:
            message = '搜索过程中出现问题。'  # 如果出现异常，设置一个通用消息
            print(f"搜索请求失败，错误: {e}")  # 可以选择在服务器日志中记录真实的错误

    # 渲染页面，将查询结果和消息传递给模板
    return render_template('findRequest.html', rows=rows, message=message)


    return render_template('findRequests.html', rows=rows)
    # 在这里实现搜索逻辑
    # return "这是查找请求的页面"
    return render_template('findRequest.html')



# 可能要用
# @app.route('/findRequest', methods=['GET'])
# def findRequest():
#     search_query = request.args.get('searchQuery', '')
#     with sqlite3.connect("database.db") as con:
#         con.row_factory = sqlite3.Row
#         cur = con.cursor()
#         # 基于标题搜索请求
#         cur.execute("SELECT * FROM requests WHERE title LIKE ?", ('%' + search_query + '%',))
#         rows = cur.fetchall()
#     return render_template('findRequests.html', rows=rows)



# 处理回复请求的路由（示例）
@app.route('/reply_request/<int:request_id>', methods=['GET', 'POST'])
def reply_request(request_id):
    if request.method == 'POST':
        # 这里应该处理回复逻辑，比如保存回复到数据库
        reply_content = request.form['reply']
        # 假设有一个replies表用来保存回复
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO replies (request_id, content) VALUES (?, ?)", (request_id, reply_content))
            con.commit()
        return redirect(url_for('findRequest'))
    else:
        # 对于GET请求，渲染回复表单的页面
        return render_template('replyRequest.html', request_id=request_id)
    







if __name__ == "__main__":
    # print(app.url_map)     这是一个测试     打印出来  app.url_map  print(app.url_map+'999')
    app.run(debug=True)
