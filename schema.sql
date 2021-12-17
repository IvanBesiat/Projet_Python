DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS products;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Name varchar NOT NULL,
  Status varchar NOT NULL
);

insert into user
  (username,password) 
values  
  ('ivan','pbkdf2:sha256:260000$Gh6GXZRDHjTkKeMN$8fb822cb35750ea19fe225dfa2854249355ad552f637d18b7e096acd8aa36bf0')
  ,('baptiste','pbkdf2:sha256:260000$W1RYIEGeVdUihzdb$6192298fb5fb3174ac6ce93bf93f0b1347b97bb8f038991c732be9fb51323ce7')
  ,('anny','pbkdf2:sha256:260000$elKoe3GB3E2L4AJt$31af904e5244231e893733c4d29c18ab26386a8268465d5e0fabcdd8d7ed3c2c');

insert into products
  (Name,Status)
values
  ("rose","En Stock")
  ,("Tulipe","Pas en Stock")
  ,("Lys","Pas en Stock")
  ,("Ortensia","En Stock")
  ,("Glaïeul","En Stock")
  