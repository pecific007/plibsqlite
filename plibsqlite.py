#!/usr/bin/env python3

import sqlite3

"""

THIS MODULE PROVIDES BASIC C.U.R.D. FUNCTIONALITIES

"""


class Table:
    def __init__(self, name: str, fields: dict) -> None:
        self.name = name
        self.fields = fields


class Database:
    def __init__(self, database_name: str) -> None:
        """This will initialise the table name and the columns/fields of a table."""
        self.tables = {}
        self.con = sqlite3.connect(database_name)
        self.IN_KEYWORD = "FOUND 'IN' OPERATOR"
        self.sync_with_database()

    def __del__(self) -> None:
        """This is a destructor that will close the connection (for now)"""
        self.con.close()

    def exec(self, stmt: str, params: list = []) -> sqlite3.Cursor:
        print("Executing: ", stmt, params)
        return self.con.execute(stmt, params)

    def sync_with_database(self) -> None:
        where_stmt, where_data = self.prep_where_statement("=", type="table")
        tables_full = self.select_from_table(
            "sqlite_master", "name", where_stmt, where_data
        )
        tables = tables_full.fetchall()
        # print(tables)
        for t in tables:
            td = (self.con.execute(f"PRAGMA table_info('{t[0]}')")).fetchall()
            # for d in td:
            #     print(d)
            new_table_fields = {
                d[1]: f"{d[2]} PRIMARY KEY"
                if d[5] == 1
                else d[2]
                if d[3] == 0
                else f"{d[2]} NOT NULL"
                for d in td
            }
            # print(new_table_fields)
            new_table = Table(t[0], new_table_fields)
            self.tables[t[0]] = new_table

    def create_table(self, name: str, ret_stmt: bool = False, **kwargs) -> None | str:
        """This function is used to create table with the name"""
        table = Table(name, kwargs)
        stmt = []
        stmt.append(f'CREATE TABLE IF NOT EXISTS "{name}"(')
        for f in kwargs:
            stmt += f'"{f}" "{kwargs[f]}"'
            stmt.append(",")

        # All the pops are mostly to remove the "," at the last element Otherwise it thorws an error
        stmt.pop()
        stmt.append(")")
        sql_query = "".join(stmt)
        if ret_stmt:
            return sql_query
        print("Executing: ", sql_query)
        self.con.execute(sql_query)
        self.tables[name] = table

    def prep_where_statement(self, operator: str, **kwargs):
        possible_operators = [
            "=",
            "!=",
            ">",
            ">=",
            "<",
            "<=",
            "LIKE",
            "like",
            "IN",
            "in",
        ]
        if operator not in possible_operators:
            print("Please provide a valid operator!")
            return "", []
        stmt = []
        data = []
        if operator == "IN" or operator == "in":
            data.append(self.IN_KEYWORD)
        stmt.append(" WHERE ")
        for k in kwargs:
            stmt.append(f'"{k}" {operator} (?) ')
            data.append(kwargs[k])
            stmt.append(" AND ")
        if stmt[(len(stmt) - 1)] == " AND ":
            stmt.pop()
        where_stmt = "".join(stmt)
        return where_stmt, data

    def insert_into_table(
        self, table_name: str, ret_stmt: bool = False, **kwargs
    ) -> None | str:
        stmt = []  # This is the sql query statement -- easy to prepare this way
        data = []  # This to store data
        stmt.append(f'INSERT INTO "{table_name}"(')
        for f in kwargs:  # This to get all the column names
            stmt.append(f'"{f}"')
            stmt.append(",")
        stmt.pop()
        stmt.append(")")

        stmt.append(" VALUES(")
        for k in kwargs:  # This to get the values
            stmt.append("(?)")
            stmt.append(",")
            data.append(kwargs[k])
        stmt.pop()
        stmt.append(")")
        sql_query = "".join(stmt)
        if ret_stmt:
            return sql_query
        print("Executing: ", sql_query, data)
        self.con.execute(sql_query, data)
        self.con.commit()

    def select_from_table(
        self,
        table_name: str,
        columns: list | str,
        where: str = "",
        data: list = [],
        limit: int = 0,
        order_by: dict = {},
        ret_stmt: bool = False,
    ):
        stmt = []
        if data:
            if data[0] == self.IN_KEYWORD:
                data = data[1:]
                data = data[0]
        stmt.append("SELECT ")
        # This for selecting all values
        if isinstance(columns, str) or len(columns) == 0:
            stmt.append(columns)
            stmt.append(f' FROM "{table_name}"')
            if len(where) != 0:
                stmt.append(where)
            if len(order_by) > 0:
                stmt.append(" ORDER BY ")
                for k in order_by:
                    stmt.append(f"{k} {order_by[k]}")
                    stmt.append(",")
                stmt.pop()
            if limit != 0:
                stmt.append(f"LIMIT {limit}")
            sql_query = " ".join(stmt)
            if ret_stmt:
                return sql_query
            print("Executing: ", sql_query, data)
            return self.con.execute(sql_query, data)

        # This for selecting values from columns
        for k in columns:
            stmt.append(k)
            stmt.append(",")

        stmt.pop()
        stmt.append(f" FROM {table_name}")
        if len(where) != 0:
            stmt.append(where)
        sql_query = "".join(stmt)
        if ret_stmt:
            return sql_query
        print("Executing: ", sql_query, data)
        return self.con.execute(sql_query, data)

    def delete_from_table(
        self, table_name: str, where: str = "", data: list = [], ret_stmt: bool = False
    ):
        """This function will delete from table."""
        # Empty where statement (i.e. where = "") it will drop table
        if len(where) == 0:
            stmt = f"DROP TABLE {table_name}"
            if ret_stmt:
                return stmt
            print("Executing: ", stmt)
            self.con.execute(stmt)
            self.con.commit()
            return

        stmt = f'DELETE FROM "{table_name}" {where}'
        if ret_stmt:
            return stmt
        print("Executing: ", stmt, data)
        self.con.execute(stmt, data)
        self.con.commit()

    def update_column_table(
        self, table_name: str, where: str, data: list, ret_stmt: bool = False, **kwargs
    ):
        """Updating a column, WHERE statement is necessary"""
        stmt = []
        cols = []
        stmt.append(f"UPDATE {table_name} SET ")
        for k in kwargs:
            stmt.append(f"{k} = ?")
            stmt.append(",")
            cols.append(kwargs[k])
        i = 0
        for c in cols:
            data.insert(i, c)
        stmt.pop()
        stmt.append(where)
        sql_query = "".join(stmt)
        if ret_stmt:
            return stmt
        print("Executing: ", sql_query, data)
        self.con.execute(sql_query, data)
        self.con.commit()

    def replace_placeholder(self, stmt: str, *args):
        data = ""
        new_stmt = ""
        if self.IN_KEYWORD == args[0][0]:
            data = args[0][1:]
        else:
            data = args[0]
        i = 0
        for s in stmt:
            if s == "?":
                s = data[i]
                i += 1
            new_stmt += f"{s}"
        return new_stmt
