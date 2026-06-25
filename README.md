# Plibsqlite

- Plibsqlite is a wrapper of a subset of python's sqlite3 library.
- This can perform basic C.U.R.D with some convenient functions.
- It is possible to make some advance statements.
- I made this to use this on my small scale projects.
- It can complete CS50's SQLite problemsets.

## Example

Here is a quick example of how to use this library. The usage of all the functions is shown in the [`examples.py`](./examples.py)

``` python
from plibsqlite import Database, col, data_type

db = Database("database.db")
db.create_table("users", columns = [
    col("id", data_type.INTEGER, pk=True, null=False),
    col("username", data_type.TEXT, null=False),
    col("is_active", data_type.BOOL, null=False),
])
db.insert("users", username="first", is_active=True).exec()
db.insert("users", username="second", is_active=False).exec()
users = db.select("*", "users").where("=", {"is_active": True}).exec()
print(users.fetchall())
```
> Output:
> ```
> Executing:  SELECT  name FROM "sqlite_master" WHERE type = ? ['table']
> Executing:  PRAGMA table_info('sqlite_sequence') []
> Executing:  CREATE TABLE IF NOT EXISTS users( id INTEGER PRIMARY KEY NOT NULL , username TEXT  NOT NULL , is_active BOOLEAN  NOT NULL ) []
> Executing:  INSERT INTO "users" ( "username" , "is_active" ) VALUES ( ? , ? ) ['first', True]
> Executing:  INSERT INTO "users" ( "username" , "is_active" ) VALUES ( ? , ? ) ['second', False]
> Executing:  SELECT  * FROM "users" WHERE is_active = ? [True]
> [(1, 'first', 1)]
> ```
