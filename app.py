from flask import Flask, request, render_template, redirect, url_for, session,make_response
import sqlite3
# 项目启动       student.html 这是主界面  名字没事
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于保持会话安全


# 先打开   这个界面   注册学生账号       这是   http://127.0.0.1:5000/create/
@app.route('/create/')
def create_student():
    return render_template('student.html')    #渲染student.html模板



# 先留着    添加学生的路由，支持POST和GET请求    @app.route('/addstudent/')     http://127.0.0.1:5000/addstudent/
@app.route('/addstudent/',methods = ['POST', 'GET'])
def add_student():
    try:
        #获取请求中的nm、add、city、pin的数据
        nm = request.form['nm']
        addr = request.form['add']
        city = request.form['city']
        pin = request.form['pin']
        with sqlite3.connect("database.db") as con:  
           cur = con.cursor()     
           cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )                
           con.commit()    
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


# 注册     http://127.0.0.1:5000    返回这个   form action    register    http://127.0.0.1:5000/register/
# register比login复杂    GET 请求通常用于从服务器获取数据或者显示一个页面 POST 请求通常用于当用户提交表单数据到服务器
@app.route('/register/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            # 从表单请求中获取用户名、密码和邮箱的数据
            username = request.form['name']
            password = request.form['password']
            email = request.form['email']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()  
                cur.execute("INSERT INTO users (name, password, email) VALUES (?, ?, ?)", (username, password, email))
                con.commit()  
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



# 登录    http://127.0.0.1:5000    返回这个   form action   login    http://127.0.0.1:5000/login/
@app.route('/login/', methods=['POST', 'GET'])
def login():
    # 默认情况下，假设没有错误消息
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with sqlite3.connect("database.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE name = ? AND password = ?", (username, password))

                user = cur.fetchone()
                if user:
                    # 用户验证成功，设置用户会话
                    session['loggedin'] = True
                    session['username'] = user['name']
                    msg = '登录成功！'
                    # 登录成功后   保存   测试
                    session['username'] = username  # 假设这是登录视图函数中的代码
                    # login   登录成功     
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





    

    










































# 先留着       这个甚至     可能不需要吧 
@app.route('/logout/')
def logout():
    # 移除会话中的用户信息
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


# 先留着           显示所有学生的路由   显示出来    这个是为了检查  好看    http://127.0.0.1:5000/show/ 
@app.route('/show/')
def show_student():
    con = sqlite3.connect("database.db")  
    con.row_factory = sqlite3.Row      #设置row_factory,对查询到的数据，通过字段名获取列数据
    cur = con.cursor()        
    cur.execute("select * from students")   
    rows = cur.fetchall()      #获取多条记录数据   
    return render_template("show.html",rows = rows)  #渲染show.html模板并传递rows值


# 这是一个测试       没有路径    只是    http://127.0.0.1:5000
# @app.route('/')
# def index():
#     return "Hello, World!"
@app.route('/')
def regi_login():
    return render_template('student.html')


# 先留着       http://127.0.0.1:5000/errorPage/
@app.route('/errorPage')
def errorPage():
    # 这里可以展示错误信息或提供错误反馈
    return "出错了！请稍后重试。"

































# 剩余几个view    和后端息息相关
# http://127.0.0.1:5000/main/
@app.route('/main')
def main():
    #  如果没有用户名就不显示错误信息，并且不执行需要登录的操作
# 这是最开始  没问题的
    return render_template('main.html')
    # username = session.get('username', None)
    # if not username:
    #     # 如果用户没有登录，可以选择渲染一个不同的页面或者不需要登录的主页版本
    #     return render_template('login.html')  # 假设这是登录页面
    # # 如果用户已登录，继续正常操作
    # return render_template('main.html')

# 发起帖子        http://127.0.0.1:5000/createRequest/
@app.route('/createRequest', methods=['GET', 'POST'])
def createRequest():
    if request.method == 'POST':  
        try:
            # 从表单请求中获取标题和描述的数据
            title = request.form['title']
            description = request.form['description']
            # 从会话中获取username
            username = session.get('username')
            # 确保在登录后才能创建请求    这个更严谨
            # if not username:
            #     # 可能需要重定向到登录页面或显示错误消息
            #     return redirect(url_for('login'))
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()  # 获取游标
                # 将请求信息添加到数据库，包括用户名
                cur.execute("INSERT INTO requests (title, description, username) VALUES (?, ?, ?)", (title, description, username))
                con.commit()  
                # 操作成功，这里有两个重定向，只需要一个    重定向到查找请求的页面或回到主页
                return redirect(url_for('main'))
                return render_template('main.html')
                return redirect(url_for('findRequest'))  # 假设你有一个叫做findRequest的视图函数来显示所有请求
        except Exception as e:
            print(f"创建请求失败，错误: {e}")
            return redirect(url_for('main', error=str(e)))
            return render_template('main.html', error=str(e))
            return render_template('errorPage.html', error=str(e))
        
    else:
        # 如果不是POST请求，则渲染创建请求的页面
        # response = make_response(render_template('createRequest.html'))
        # # Prevent caching the form page to avoid resubmission issues
        # response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        # response.headers['Pragma'] = 'no-cache'  # HTTP 1.0 compatibility
        # response.headers['Expires'] = '0'  # Proxies
        # return response
        
        return render_template('createRequest.html')





#  搜索帖子       http://127.0.0.1:5000/main/          @app.route('/findRequest')
@app.route('/findRequest')
def findRequest():
    search_queryFR = request.args.get('searchQueryFR', '').strip()
    rows = []
    message = ''

    if search_queryFR:
        try:
            with sqlite3.connect("database.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("SELECT * FROM requests WHERE title LIKE ?", ('%'+search_queryFR+'%',))
                rows = [dict(row) for row in cur.fetchall()]

                for row in rows:
                    cur.execute("SELECT * FROM replies WHERE request_id=?", (row["id"],))
                    row["replies"] = [dict(reply) for reply in cur.fetchall()]

                if not rows:
                    message = '未找到匹配的请求。'
        except Exception as e:
            message = '搜索过程中出现问题。'
            print(f"搜索请求失败，错误: {e}")

    # 注意这里将 search_queryFR 变量回传给模板
    return render_template('findRequest.html', rows=rows, message=message, search_queryFR=search_queryFR)
# def findRequest():
#     search_queryFR = request.args.get('searchQueryFR', '').strip()
#     rows = []
#     message = ''  # 初始化消息为空字符串
#     # search_queryFR   筛选框   有内容
#     if search_queryFR:
#         try:
#             with sqlite3.connect("database.db") as con:
#                 con.row_factory = sqlite3.Row  # 使行     为字典
#                 cur = con.cursor()
#                 # 找到这个帖子             只根据标题   搜索requests表     
#                 cur.execute("SELECT * FROM requests WHERE title LIKE ?", ('%'+search_queryFR+'%',))
#                 rows = cur.fetchall()
#                 # rows是全部   这些帖子
                
#                 # row是    对于每个帖子   查询其所有回答
#                 for row in rows:
#                     row = dict(row)  # row 是每个帖子     确保row是字典格式以便我们可以修改它
#                     cur.execute("SELECT * FROM replies WHERE request_id=?", (row["id"],))
#                     replies = cur.fetchall()
#                     row["replies"] = [dict(reply) for reply in replies] if replies else []  # 如果没有回答，确保是空列表[]
#                     print(row["replies"])
#                     # for reply in replies:
#                     #     print(dict(reply))
#                     #回答 [<sqlite3.Row object at 0x0000029965FBAB60>]

#                 if not rows:
#                     message = '未找到匹配的请求。'



#                 # back
#                 # con.row_factory = sqlite3.Row  # 使行为字典
#                 # cur = con.cursor()
#                 # # 只根据标题搜索requests表
#                 # cur.execute("SELECT * FROM requests WHERE title LIKE ?", ('%'+search_queryFR+'%',))
#                 # rows = cur.fetchall()  # 获取所有查询结果
#                 # if not rows:  # 如果没有找到任何行
#                 #     message = '未找到匹配的请求。'  # 设置消息为“未找到”
#         except Exception as e:
#             message = '搜索过程中出现问题。'  # 如果出现异常，设置一个通用消息
#             print(f"搜索请求失败，错误: {e}")  # 可以选择在服务器日志中记录真实的错误
#     return render_template('findRequest.html', rows=rows, message=message)























# 回复 帖子                 请求的路由（示例）
# @app.route('/replyRequest/<int:request_id>', methods=['GET', 'POST'])
# def replyRequest(request_id):
#     if request.method == 'POST':
#         # 这里应该处理回复逻辑，比如保存回复到数据库   假设有一个replies表用来保存回复
#         reply_content = request.form['reply']
#         responderName = session['username']
#         # 只有当reply_content不为空时，才处理回复逻辑
#         if reply_content:  # 检查reply_content  不是空
#             with sqlite3.connect("database.db") as con:
#                 cur = con.cursor()
#                 # 向replies表中插入数据：request_id, reply_content, 和 answerName
#                 cur.execute("INSERT INTO replies (request_id, reply_content, answerName) VALUES (?, ?, ?)",
#                             (request_id, reply_content, responderName))
#                 con.commit()
#             return redirect(url_for('findRequest'))
#         else:
#             # reply_content为空  重新渲染回复表单的页面   可以选择传递一个错误消息到页面，告知用户需要输入回复内容   这里埋了雷
#             return render_template('findRequest.html', request_id=request_id, error="回复内容不能为空。")
#     else:
#         # 啥也没有回复     对于GET请求，渲染回复表单的页面
#         return render_template('findRequest.html', request_id=request_id)

# 这个reply   还不完善
@app.route('/replyRequest', methods=['GET', 'POST'])
def replyRequest():
    if request.method == 'POST':
        reply_content = request.form['reply']
        responderName = session['username']
        # 假设 'search_queryFR' 是表单字段，用户提交的是请求的标题
        request_title = request.form.get('search_queryFR')

        if reply_content:
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                # 首先根据标题找到请求的 ID
                # cur.execute("SELECT id FROM requests WHERE title = ?", (request_title,))   这是完全匹配   不完善
                cur.execute("SELECT id FROM requests WHERE title LIKE ?", ('%' + request_title + '%',))
                result = cur.fetchone()  #  没有回复   是none

                # 检查是否找到了对应的请求
                if result:
                    request_id = result[0]

                    # 然后像之前一样处理回复逻辑
                    cur.execute("INSERT INTO replies (request_id, reply_content, answerName) VALUES (?, ?, ?)",
                                (request_id, reply_content, responderName))
                    con.commit()

                    return redirect(url_for('findRequest'))
                else:
                    # 如果根据标题找不到请求，返回错误消息
                    return render_template('findRequest.html', error="未找到指定的请求，请检查标题是否正确。")
        else:
            return render_template('findRequest.html', error="回复内容不能为空。")
    else:
        # 对于 GET 请求，从 URL 参数中获取标题
        # 注意：这里的参数名应该与POST请求中表单字段的名称保持一致
        request_title = request.args.get('search_queryFR')
        return render_template('findRequest.html', request_title=request_title)




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

# @app.route('/requests')
# def show_requests():
#     # 连接数据库
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row  # 这样可以让我们通过列名称访问数据
#     cur = conn.cursor()
    
#     # 查询所有请求
#     cur.execute('SELECT * FROM requests')
#     rows = cur.fetchall()

#     # 对于每个请求，查询其所有回答
#     for row in rows:
#         request_id = row['id']
#         cur.execute('SELECT * FROM replies WHERE request_id=?', (request_id,))
#         replies = cur.fetchall()
#         # 将回答列表添加到请求对象中
#         row['replies'] = replies
    
#     # 关闭数据库连接
#     conn.close()

#     # 将请求和它们的回答传递给模板
#     return render_template('requests.html', rows=rows)



if __name__ == "__main__":
    # print(app.url_map)     这是一个测试     打印出来  app.url_map  print(app.url_map+'999')
    app.run(debug=True)
