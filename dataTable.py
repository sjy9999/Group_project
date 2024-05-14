import sqlite3

# link to database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# drop requests
cursor.execute('DROP TABLE IF EXISTS requests')

# create requests 
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

# commit
conn.commit()

# close
conn.close()
