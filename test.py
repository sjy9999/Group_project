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

# 为用户表添加 avatar_url 列
conn.execute('''
ALTER TABLE users ADD COLUMN avatar_url TEXT;
''')



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



# 改!!!!!!!!!!!!       sqlite3 instance/database.db

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

# users 表
# 1|1|395615470@qq.com
# 2|2|39561547@qq.com
# 3|1|1@qq.com


# 3|9|scrypt:32768:8:1$ZRsgz0Cd5NCxRbs0$af5092f37d940fb3d702a214968024ee9b7654d48e78fd569217029abc96112844caf3f550cc02b592a2c957bba45f2c00b54642aa56245758ca9477a78e01b1|395615470@qq.com
# 5|3|scrypt:32768:8:1$a2lRRzOvYTItyu92$23d446d5aaa699ec11b8131af3183ddabf2522eca5e632fee583be37674b77d488f9011a5f3770827aeed1e42082167a023ae118c452b04109fee82803730a3f|3@qq.com