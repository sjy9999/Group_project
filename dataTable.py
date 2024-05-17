# At the beginning of the project, we tested connecting to the database directly. 
# Later, we changed to using SQLAlchemy. This needs to be clarified. 
# However, SQLite3 can also be used in this project, despite some drawbacks of SQLite3, such as security vulnerabilities.


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
