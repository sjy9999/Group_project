import sqlite3
# 创建新表
# 运行test.py可以发现在项目目录中创建了一个名为database的数据库
conn = sqlite3.connect('database.db')  #建立database.db数据库连接
# this is ori
# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)') #执行单条sql语句


# 具体   sql
conn.execute('''
CREATE TABLE IF NOT EXISTS students (
    name TEXT,
    addr TEXT,
    city TEXT,
    pin TEXT
)
''') #执行单条sql语句



# 具体   sql
# 多个table  表格
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    name TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE CHECK(email LIKE '%@%.%')
)
''') #执行单条sql语句



conn.execute('''
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    username TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(username) REFERENCES users(name)
)
''') #执行单条sql语句



# request_id    reply_content   回答者
conn.execute('''
CREATE TABLE IF NOT EXISTS replies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT NOT NULL,
    reply_content TEXT,
    answerName TEXT
)
''') #执行单条sql语句



conn.close()       #关闭连接













# SQLite 提供了一个命令行工具，称为 sqlite3，可以用来与 SQLite 数据库交互。使用这个工具，您可以执行 SQL 命令来查询和管理数据库。
# 例如，要查看所有的表，您可以使用 .tables 命令。如果您想看到某个表的结构，可以使用 .schema 表名 命令。
# 打开终端或命令提示符，然后键入以下命令
# sqlite3 database.db
# .tables
# .schema students
# .quit

# 删除一个表
# DROP TABLE IF EXISTS requests;





# 我想查看数据   方式1
# sqlite3 database.db
# SELECT * FROM users;
# .exit

# 显示列名
# .headers on
# .mode column
# SELECT * FROM users;
# ;不能少了

# 我想查看数据   方式2
# import sqlite3
# # 连接到数据库
# conn = sqlite3.connect('database.db')
# # 创建游标对象
# cursor = conn.cursor()
# # 查询 user 表
# cursor.execute('SELECT * FROM user')
# # 获取所有数据
# users = cursor.fetchall()
# # 打印数据
# for user in users:
#     print(user)
# # 关闭连接
# conn.close()







# 我目前使用   这些表          users  requests        students




# requests表 
# id  title  description  username  created_at
# --  -----  -----------  --------  -------------------
# 1   1      1                      2024-03-26 11:37:10
# 2   1      1                      2024-03-26 11:40:37



# replies表
# id是主键
# id  request_id  reply_content  answerName
# --  ----------  -------------  ----------
# 1   1           aaa            1
# 2   4           bbb            1















# sqlite> SELECT * FROM requests;
# 1|1|1||2024-03-26 11:37:10
# 2|1|1||2024-03-26 11:40:37
# 3|1|11111||2024-03-26 11:41:20
# 4|2|2|1|2024-04-09 11:15:02
# 5|9|9|1|2024-04-10 13:24:54
# 6|bad teacher uwa|java|1|2024-04-19 03:21:27

# sqlite> SELECT * FROM replies;  
# 1|1|aaa|1
# 2|4|bbb|1
# 3|5|99|1
# 4|5|oo|1
# 5|5|oooo|1
# 6|1|bbb|1
# 7|1|quandi|1