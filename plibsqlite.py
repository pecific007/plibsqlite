import sqlite3
from typing import Any, Self

###########################################################
"                                                         "
""" THIS MODULE PROVIDES BASIC C.U.R.D. FUNCTIONALITIES """
"                                                         "
###########################################################


class Table:
    name: str
    fields: dict

    def __init__(self, name: str, fields: dict) -> None:
        self.name = name
        self.fields = fields


class Database:
    stmt: str  # The statement
    params: list[Any]  # Parameters
    tables: dict[str, Table]  # The names of tables
    database_name: str  # The name of the database
    con: sqlite3.Connection  # Connection with the database

    def __init__(self, database_name) -> None:
        self.database_name = database_name
        self.tables = {}
        self.stmt = ""
        self.params = []
        self.con = sqlite3.connect(self.database_name)
        self.sync()

    def __del__(self):
        self.disconnect()

    def disconnect(self) -> None:
        """This method is used to disconnect from the database"""
        self.con.close()

    def sync(self) -> None:
        tables_full = (
            self.select("name", "sqlite_master")
            .where("=", vals={"type": "table"})
            .exec()
        )
        tables = tables_full.fetchall()
        for t in tables:
            td = (self.exec(f"PRAGMA table_info('{t[0]}')")).fetchall()
            new_table_fields = {
                d[1]: f"{d[2]} PRIMARY KEY"
                if d[5] == 1
                else d[2]
                if d[3] == 0
                else f"{d[2]} NOT NULL"
                for d in td
            }
            new_table = Table(t[0], new_table_fields)
            self.tables[t[0]] = new_table
        return

    def schema(self) -> None:
        print("Schema:")
        for t in self.tables:
            print(self.tables[t].name, self.tables[t].fields)

    def create_table(self, table_name: str, **kwargs: Any) -> Self:
        """This method will create a table in the database"""
        """ Unlike other methods, this will by default execute statements """
        table = Table(table_name, kwargs)
        stmt = []
        stmt.append(f"CREATE TABLE IF NOT EXISTS {table_name}(")
        for f in kwargs:
            stmt.append(f"{f} {kwargs[f]}")
            stmt.append(",")
        stmt.pop()
        stmt.append(")")
        self.__add_to_stmt(stmt)
        self.exec(self.stmt)
        self.tables[table_name] = table
        return self

    def exec(
        self, stmt: str = "", params: list[Any] | tuple[Any] = []
    ) -> sqlite3.Cursor:
        """This method is used to execute the built query"""
        if len(stmt) > 0:
            self.stmt = ""
            self.params = []
            print("Executing: ", stmt, params)
            return self.con.execute(stmt, params)
        stmt = self.stmt
        params = self.params
        self.stmt = ""
        self.params = []
        print("Executing: ", stmt, params)
        cursor = self.con.execute(stmt, params)
        self.con.commit()
        return cursor

    def insert(self, table_name: str, **kwargs: Any) -> Self:
        """This method will insert values in the table"""
        stmt = []
        params = []
        stmt.append(f'INSERT INTO "{table_name}" (')
        for k in kwargs:
            stmt.append(f'"{k}"')
            stmt.append(",")
        stmt.pop()
        stmt.append(") VALUES (")
        for k in kwargs:
            stmt.append("?")
            stmt.append(",")
            params.append(kwargs[k])
        stmt.pop()
        stmt.append(")")
        self.__add_to_stmt(stmt)
        self.__add_to_params(params)
        return self

    def select(
        self,
        columns: list[Any] | str,
        table_name: str,
    ) -> Self:
        """This method will return data from the server"""
        stmt = []
        stmt.append("SELECT")
        if isinstance(columns, str):
            stmt.append(columns)
        elif isinstance(columns, list):
            for c in columns:
                stmt.append(f'"{c}"')
                stmt.append(",")
            stmt.pop()
        stmt.append(f'FROM "{table_name}"')
        self.__add_to_stmt(stmt)
        return self

    def order_by(self, by: str | dict[Any, Any]) -> Self:
        stmt = []
        stmt.append("ORDER BY")
        if isinstance(by, str):
            stmt.append(by)
        else:
            for b in by:
                stmt.append(f"{b} {by[b]}")
                stmt.append(",")
            stmt.pop()
        self.__add_to_stmt(stmt)
        return self

    def limit(self, limit: Any) -> Self:
        self.stmt += f" LIMIT {limit}"
        return self

    def where(self, operators: str | list[Any], vals: str | dict[Any, Any]) -> Self:
        """This method will add a where condition to the statement"""
        self.stmt += " WHERE"
        self.__condition_logic(operators, vals)
        return self

    def condition(
        self, type_of: str, operators: str | list[Any], vals: str | dict[Any, Any]
    ) -> Self:
        """This method will add a specified type condition to the statement"""
        self.stmt += f" {type_of}"
        self.__condition_logic(operators, vals)
        return self

    def out(self) -> Self:
        self.stmt += " )"
        return self

    def join(self, table_name: str, operators: str | list, on: dict) -> Self:
        """This method is used to join tables"""
        stmt = []
        stmt.append(f'JOIN "{table_name}" ON')
        i = 0
        if isinstance(operators, str):
            for o in on:
                stmt.append(f"{o} {operators} {on[o]}")
        elif isinstance(operators, list):
            for o in on:
                stmt.append(f"{o} {operators[i]} {on[o]}")
                i += 0
        self.__add_to_stmt(stmt)
        return self

    def update(
        self, table_name: str, operators: str | list, vals: dict, where: dict
    ) -> Self:
        """This method is used to update any values in a table"""
        stmt = []
        params = []
        stmt.append(f'UPDATE "{table_name}" SET')
        i = 0
        if isinstance(operators, str):
            for v in vals:
                stmt.append(f"{v} {operators} ?")
                stmt.append(",")
                params.append(vals[v])
        elif isinstance(operators, list):
            for v in vals:
                stmt.append(f"{v} {operators[i]} ?")
                stmt.append(",")
                params.append(vals[v])
                i += 0
        stmt.pop()
        self.__add_to_stmt(stmt)
        self.__add_to_params(params)
        self.where(operators, where)
        return self

    def delete(
        self,
        table_name: str,
        operators: str | list,
        vals: dict[Any, Any],
    ) -> Self:
        """This method will delete a row from the table"""
        stmt = []
        stmt.append(f"DELETE FROM {table_name}")
        self.__add_to_stmt(stmt)
        self.where(operators, vals)
        return self

    def drop(self, table_name: str) -> Self:
        """Unlike other methods, this will just execute the statement"""
        self.exec(f"DROP TABLE {table_name}")
        return self

    """
    Helper Functions:
    """

    def __add_to_stmt(self, pre_stmt: list) -> None:
        if len(self.stmt) > 0:
            self.stmt += " "
        self.stmt += " ".join(pre_stmt)
        return

    def __add_to_params(self, params: list) -> None:
        for p in params:
            self.params.append(p)
        return

    def __condition_logic(
        self, operators: str | list[Any], vals: str | dict[Any, Any]
    ) -> None:
        stmt = []
        params = []
        if isinstance(vals, str):
            stmt.append(f" {vals} IN (")
        else:
            i = 0
            for v in vals:
                stmt.append(v)
                stmt.append(operators if isinstance(operators, str) else operators[i])
                stmt.append("?")
                stmt.append("AND")
                params.append(vals[v])
                i += 0
            stmt.pop()
        self.__add_to_stmt(stmt)
        self.__add_to_params(params)
        return
