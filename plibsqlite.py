import sqlite3
from typing import Any, Self

###############################################################
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""" #
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""" #
# "                                                         " #
""""" THIS MODULE PROVIDES BASIC C.U.R.D. FUNCTIONALITIES """ ""
# "                                                         " #
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""" #
# """"""""""""""""""""""""""""""""""""""""""""""""""""""""""" #
###############################################################


class Table:
    def __init__(self, name: str, fields: dict) -> None:
        self.name = name
        self.fields = fields


class Database:
    stmt: str  # The statement
    params: list  # Parameters
    tables: dict[str, object]  # The name of table
    con: sqlite3.Connection  # Connectino with the database

    def __init__(self, database_name) -> None:
        global connection
        self.database_name = database_name
        self.tables = {}
        self.stmt = ""
        self.params = []
        self.con = sqlite3.connect(self.database_name)
        # self.sync_with_database()

    def __del__(self):
        self.disconnect()

    def disconnect(self) -> None:
        """This method is used to disconnect from the database"""
        self.con.close()

    def create_table(self, table_name: str, **kwargs: Any) -> Self:
        """This method will create a table in the database"""
        table = Table(table_name, kwargs)
        stmt = []
        stmt.append(f'CREATE TABLE IF NOT EXISTS "{table_name}"(')
        for f in kwargs:
            stmt.append(f'"{f}" {kwargs[f]}')
            stmt.append(",")
        stmt.pop()
        stmt.append(")")
        self.stmt += "".join(stmt)
        self.tables[table_name] = table
        return self

    def exec(self) -> sqlite3.Cursor:
        """This method is used to execute the built query"""
        stmt = self.stmt
        params = self.params
        self.stmt = ""
        self.params = []
        print("Executing: ", stmt, params)
        return self.con.execute(stmt, params)

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
        self.add_to_stmt(stmt)
        self.add_to_params(params)
        return self

    def select(
        self,
        table_name: str,
        columns: list | str,
        order_by: dict = {},
        limit: str | int = "",
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
        if order_by:
            stmt.append("ORDER BY")
            for o in order_by:
                stmt.append(f"{o} {order_by[o]}")
                stmt.append(",")
            stmt.pop()
        if limit:
            stmt.append(f"LIMIT {limit}")
        self.add_to_stmt(stmt)
        return self

    def where(self, operators: str | list, vals: dict[Any, Any]) -> Self:
        """This method will add a where condition to the statement"""
        stmt = []
        params = []
        stmt.append("WHERE")
        if isinstance(operators, str):
            for v in vals:
                stmt.append(f"{v} {operators} ?")
                stmt.append("AND")
                params.append(vals[v])
            stmt.pop()
        elif isinstance(operators, list):
            i = 0
            for v in vals:
                stmt.append(f"{v} {operators[i]} ?")
                params.append(vals[v])
                i += 0
        self.add_to_stmt(stmt)
        self.add_to_params(params)
        return self

    def join(self, table_name: str, operators: str | list, on: dict) -> Self:
        stmt = []
        stmt.append(f'JOIN "{table_name}" ON')
        i = 0
        if isinstance(operators, str):
            for o in on:
                stmt.append(f"{o} {operators} {on[o]}")
        if isinstance(operators, list):
            for o in on:
                stmt.append(f"{o} {operators[i]} {on[o]}")
                i += 0

        self.add_to_stmt(stmt)
        return self

    """
    Helper Functions:
    """

    def add_to_stmt(self, pre_stmt: list) -> None:
        self.stmt += " "
        self.stmt += " ".join(pre_stmt)

    def add_to_params(self, params: list) -> None:
        for p in params:
            self.params.append(p)
