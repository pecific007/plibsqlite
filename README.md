# Plibsqlite

- Plibsqlite is a wrapper of a subset of python's sqlite3 library.
- This can perform basic C.U.R.D with some convenient functions.
- It is possible to make some advance statements.
- I made this to use this on my small scale projects.
- It can complete CS50's SQLite problemsets.

## Example

Here is a quick example of how to use this library. The usage of all the functions is shown in the [`examples.py`](./examples.py)

``` python
from plibsqlite import Database

db = Database("database.db")
db.create_table("users", id="INTEGER PRIMARY KEY", username="TEXT NOT NULL", password="TEXT NOT NULL", is_active="BOOLEAN NOT NULL")
db.insert("users", username="first", password="1234", is_active=True).exec()
db.insert("users", username="second", password="5678", is_active=True).exec()
users = db.select("*", "users").where("=", {"is_active": True}).exec()
print(users)
```
> Output:
> ```
> Executing:  SELECT name FROM "sqlite_master" WHERE type = ? ['table']
> Executing:  PRAGMA table_info('users') []
> Executing:  CREATE TABLE IF NOT EXISTS users( id INTEGER PRIMARY KEY , username TEXT NOT NULL , password TEXT NOT NULL , is_active BOOLEAN NOT NULL ) []
> Executing:  INSERT INTO "users" ( "username" , "password" , "is_active" ) VALUES ( ? , ? , ? ) ['first', '1234', True]
> Executing:  INSERT INTO "users" ( "username" , "password" , "is_active" ) VALUES ( ? , ? , ? ) ['second', '5678', True]
> Executing:  SELECT  * FROM "users" WHERE is_active = ? [True]
> <sqlite3.Cursor object at 0x7fc85c1bcbc0>
> ```
