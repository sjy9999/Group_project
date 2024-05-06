


CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    addr TEXT NOT NULL,
    city TEXT NOT NULL,
    pin TEXT NOT NULL
);



-- user  table
CREATE TABLE IF NOT EXISTS user (
    name TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE CHECK(email LIKE '%@%.%'), -- 简单的格式校验和唯一性约束
    ALTER TABLE users ADD COLUMN avatar_url TEXT;

);

