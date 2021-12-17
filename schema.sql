DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS products;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name varchar(50) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  Status BOOLEAN NOT NULL
);

insert into [user]
  (username,password) 
values  
  ('ivan','Besiat')
  ,('baptiste','Ivaldi')
  ,('anny','Barrero');