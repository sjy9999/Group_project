import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 删除旧的 requests 表（警告：这将移除表及其所有数据）
cursor.execute('DROP TABLE IF EXISTS requests')

# 根据新的结构创建 requests 表，其中 username 字段可以为空
cursor.execute('''
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    username TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(username) REFERENCES users(name)
)
''')

# 提交事务
conn.commit()

# 关闭连接
conn.close()
