#!/usr/bin/env python3

import sqlite3

"""

THIS MODULE PROVIDES BASIC C.U.R.D. FUNCTIONALITIES

"""


class Database:
    def __init__(self, database_name: str, name: str, fields: dict):
        """This will initialise the table name and the columns/fields of a table."""
        self.name = name
        self.fields = fields
        self.con = sqlite3.connect(database_name)

    def __del__(self):
        """This is a destructor that will close the connection (for now)"""
        self.con.close()

    def create_table(self):
        """This function is used to create table with the name"""
        stmt = []
        stmt.append(f"CREATE TABLE IF NOT EXISTS {self.name}(")
        for f in self.fields:
            stmt += f"{f} {self.fields[f]}"
            stmt.append(",")

        # All the pops are mostly to remove the "," at the last element Otherwise it thorws an error
        stmt.pop()
        stmt.append(")")
        sql_query = "".join(stmt)
        print("Executing: ", sql_query)
        self.con.execute(sql_query)

    def prep_where_statement(self, vals: dict):
        stmt = []
        data = []
        stmt.append(" WHERE ")
        i = 0
        for k in vals:
            # print(k)
            stmt.append(f"{k} = ? ")
            # print(stmt)
            data.append(vals[k])
            stmt.append(" AND ")
            i += 1
        if stmt[(len(stmt) - 1)] == " AND ":
            stmt.pop()
        where_stmt = "".join(stmt)
        # print("where data: ", where_stmt)
        return where_stmt, data

    def insert_into_table(self, values: dict):
        stmt = []  # This is the sql query statement -- easy to prepare this way
        data = []  # This to store data
        stmt.append(f"INSERT INTO {self.name}(")
        for f in values:  # This to get all the column names
            stmt.append(f"{f}")
            stmt.append(",")
        stmt.pop()
        stmt.append(")")

        stmt.append(" VALUES(")
        for k in values:  # This to get the values
            stmt.append("?")
            stmt.append(",")
            data.append(values[k])
        stmt.pop()
        stmt.append(")")
        sql_query = "".join(stmt)
        print("Executing: ", sql_query)
        self.con.execute(sql_query, data)
        self.con.commit()

    def select_from_table(self, columns: list = [], where: str = "", data: list = []):
        stmt = []
        stmt.append("SELECT ")
        # This for selecting all values
        if len(columns) == 0:
            print(
                "Getting all the rows: Providing empty value for columns will by default select *"
            )
            stmt.append(f" * FROM {self.name}")
            if len(where) != 0:
                stmt.append(where)
            sql_query = "".join(stmt)
            print("Executing: ", sql_query)
            row = self.con.execute(sql_query, data)
            return row
        # This for selecting values from columns
        for k in columns:
            stmt.append(k)
            stmt.append(",")

        stmt.pop()
        stmt.append(f" FROM {self.name}")
        if len(where) != 0:
            stmt.append(where)
        sql_query = "".join(stmt)
        print("Executing: ", sql_query)
        return self.con.execute(sql_query, data)

    def delete_from_table(self, where_stmt: str = "", where_data: list = []):
        """This function will delete from table."""
        # Empty where statement (i.e. where = "") it will drop table
        if len(where_stmt) == 0:
            stmt = f"DROP TABLE {self.name}"
            self.con.execute(stmt)
            self.con.commit()
            return

        stmt = f"DELETE FROM {self.name} {where_stmt}"
        print("Executing: ", stmt)
        self.con.execute(stmt, where_data)
        self.con.commit()

    def update_column_table(self, columns: dict, where: str = "", data: list = []):
        """Updating a column, WHERE statement is necessary"""
        stmt = []
        stmt.append(f"UPDATE {self.name} SET ")
        for k in columns:
            stmt.append(f"{k} = ?")
            stmt.append(",")
            data.append(columns[k])
        stmt.pop()
        stmt.append(where)
        sql_query = "".join(stmt)
        print("Executing: ", sql_query)
        self.con.execute(sql_query, data)
        self.con.commit()


def example():
    # Creating table
    db = Database(
        "database.db",
        "things",
        {
            "ID": "INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT",
            "THING_NAME": "TEXT NOT NULL",
            "THING_DESC": "TEXT NOT NULL",
        },
    )
    print("Create table")
    db.create_table()

    # Adding values to table
    print("Insert values")
    insert_values = {"THING_NAME": "Air cooler", "THING_DESC": "For summers"}
    db.insert_into_table(insert_values)
    insert_values = {"THING_NAME": "Table", "THING_DESC": "Wooden, used"}
    db.insert_into_table(insert_values)

    # Selecting from table
    print("Select from table")
    table_data = db.select_from_table(["THING_NAME"])
    print("Table data: ", table_data.fetchall())

    # Updating values from table
    print("Update table")
    update_value = {"THING_NAME": "Wood Table"}
    where_stmt, where_data = db.prep_where_statement({"ID": 1})
    db.update_column_table(update_value, where_stmt, where_data)

    # Selecting from table with WHERE condition
    print("Selecting with WHERE condition")
    where_stmt, where_data = db.prep_where_statement({"THING_NAME": "Wood Table"})
    # print("exmple:", where_stmt, where_data)
    table_data = db.select_from_table([], where_stmt, where_data)
    print("Table data: ", table_data.fetchall())

    # Deleting from table
    print("Deleting from table")
    where_stmt, where_data = db.prep_where_statement({"ID": "2"})
    db.delete_from_table(where_stmt, where_data)
    table_data = db.select_from_table([])
    print("Table data: ", table_data.fetchall())

    # Dropping the table
    print("Dropping table")
    db.delete_from_table("")
    db.__del__()


if __name__ == "__main__":
    example()
