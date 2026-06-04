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
users = db.select("*", "users").where("=", {"is_active": 1}).exec()
print(users)
```
> Output:
> ```
> Executing:  SELECT name FROM "sqlite_master" WHERE type = ? ['table']
> Executing:  PRAGMA table_info('users') []
> Executing:  SELECT * FROM "users" WHERE is_active = ? [1]
> <sqlite3.Cursor object at 0x7fc85c1bcbc0>
> ```
