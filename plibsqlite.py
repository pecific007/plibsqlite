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
    def __init__(self, database_name: str):
        """This will initialise the table name and the columns/fields of a table."""
        self.tables = {}
        self.con = sqlite3.connect(database_name)

    def __del__(self):
        """This is a destructor that will close the connection (for now)"""
        self.con.close()

    def create_table(self, name: str, **kwargs):
        """This function is used to create table with the name"""
        table = Table(name, kwargs)
        stmt = []
        stmt.append(f"CREATE TABLE IF NOT EXISTS {name}(")
        for f in kwargs:
            stmt += f"{f} {kwargs[f]}"
            stmt.append(",")

        # All the pops are mostly to remove the "," at the last element Otherwise it thorws an error
        stmt.pop()
        stmt.append(")")
        sql_query = "".join(stmt)
        print("Executing: ", sql_query)
        self.con.execute(sql_query)
        self.tables[name] = table

    def prep_where_statement(self, **kwargs):
        stmt = []
        data = []
        stmt.append(" WHERE ")
        i = 0
        for k in kwargs:
            stmt.append(f"{k} = ? ")
            data.append(kwargs[k])
            stmt.append(" AND ")
            i += 1
        if stmt[(len(stmt) - 1)] == " AND ":
            stmt.pop()
        where_stmt = "".join(stmt)
        return where_stmt, data

    def insert_into_table(self, table_name: str, **kwargs):
        stmt = []  # This is the sql query statement -- easy to prepare this way
        data = []  # This to store data
        stmt.append(f"INSERT INTO {table_name}(")
        for f in kwargs:  # This to get all the column names
            stmt.append(f"{f}")
            stmt.append(",")
        stmt.pop()
        stmt.append(")")

        stmt.append(" VALUES(")
        for k in kwargs:  # This to get the values
            stmt.append("?")
            stmt.append(",")
            data.append(kwargs[k])
        stmt.pop()
        stmt.append(")")
        sql_query = "".join(stmt)
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
    ):
        table = self.tables[table_name]
        stmt = []
        stmt.append("SELECT ")
        # This for selecting all values
        if isinstance(columns, str) or len(columns) == 0:
            if columns == "*":
                print(
                    "Getting all the rows: Providing empty value for columns will by default select *"
                )
                stmt.append(f" * FROM {table_name}")
                if len(where) != 0:
                    stmt.append(where)
                sql_query = "".join(stmt)
            else:
                assert columns in table.fields
                stmt.append(columns)
                stmt.append(f" FROM {table_name}")
                if len(where) != 0:
                    stmt.append(where)
            if len(order_by) > 0:
                for k in order_by:
                    stmt.append(f" ORDER BY {k} {order_by[k]}")
            if limit != 0:
                stmt.append(f"LIMIT {limit}")
            sql_query = " ".join(stmt)
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
        print("Executing: ", sql_query, data)
        return self.con.execute(sql_query, data)

    def delete_from_table(self, table_name: str, where: str = "", data: list = []):
        """This function will delete from table."""
        # Empty where statement (i.e. where = "") it will drop table
        if len(where) == 0:
            stmt = f"DROP TABLE {table_name}"
            self.con.execute(stmt)
            self.con.commit()
            return

        stmt = f"DELETE FROM {table_name} {where}"
        print("Executing: ", stmt, data)
        self.con.execute(stmt, data)
        self.con.commit()

    def update_column_table(self, table_name: str, where: str, data: list, **kwargs):
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
        print("Executing: ", sql_query, data)
        self.con.execute(sql_query, data)
        self.con.commit()
