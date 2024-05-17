# At the beginning of the project, we tested connecting to the database directly. 
# Later, we changed to using SQLAlchemy. This needs to be clarified. 
# However, SQLite3 can also be used in this project, despite some drawbacks of SQLite3, such as security vulnerabilities.

import sqlite3

conn = sqlite3.connect('database.db')  #db link

conn.execute('''
CREATE TABLE IF NOT EXISTS students (
    name TEXT,
    addr TEXT,
    city TEXT,
    pin TEXT
)
''') 

conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    name TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE CHECK(email LIKE '%@%.%')
)
''') 

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
''') 




conn.execute('''
CREATE TABLE IF NOT EXISTS replies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT NOT NULL,
    reply_content TEXT,
    answerName TEXT
)
''') 



conn.close()    
