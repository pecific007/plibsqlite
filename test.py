#!/usr/bin/env python3

import plibsqlite as sql


def print_select_statements(data):
    for d in data:
        print(d)


db = sql.Database("database.db")


class test_with_one_table:
    def __init__(self) -> None:
        self.test__create_table()
        self.test__insert_values()
        self.test__select_values()
        self.test__update_values()
        self.test__select_with_where_condition()
        self.test__select_with_order_by_and_limit()
        self.test__deleting_values()
        self.test__dropping_table()

    def test__create_table(self) -> None:
        # Creating table
        print("Create table")
        db.create_table(
            "things",
            ID="INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT",
            THING_NAME="TEXT NOT NULL",
            THING_DESC="TEXT NOT NULL",
        )

    def test__insert_values(self):
        # Adding values to table
        print("Insert values")
        values = {
            "Air cooler": "For summer",
            "Table": "Wooden and used",
            "GNU/Linux": "Operating System",
            "Niri": "Scrolling Window Manager",
            "Wallpaper": "Earth",
        }
        for k in values:
            db.insert_into_table("things", THING_NAME=k, THING_DESC=values[k])

    def test__select_values(self):
        # Selecting from table
        print("Select from table")
        table_data = db.select_from_table("things", "THING_NAME")
        print_select_statements(table_data)
        print("Table data:")

    def test__update_values(self):
        # Updating values from table
        print("Update table")
        where_stmt, where_data = db.prep_where_statement("=", ID=2)
        db.update_column_table(
            "things", where_stmt, where_data, THING_NAME="Wood Table"
        )

    def test__select_with_where_condition(self):
        # Selecting from table with WHERE condition
        print("Selecting with WHERE condition")
        where_stmt, where_data = db.prep_where_statement("=", THING_NAME="Wood Table")
        table_data = db.select_from_table("things", "*", where_stmt, where_data)
        print("Table data:")
        print_select_statements(table_data)

    def test__select_with_order_by_and_limit(self):
        # Selecting from table with WHERE condition AND 'LIMIT' AND 'ORDER'
        print("Selecting with WHERE condition")
        table_data = db.select_from_table(
            "things", "*", limit=2, order_by={"ID": "DESC"}
        )
        print("Table data:")
        print_select_statements(table_data)

    def test__deleting_values(self):
        # Deleting from table
        print("Deleting from table")
        where_stmt, where_data = db.prep_where_statement("=", ID=2)
        db.delete_from_table("things", where_stmt, where_data)
        table_data = db.select_from_table("things", "*")
        print("Table data:")
        print_select_statements(table_data)

    def test__dropping_table(self):
        # Dropping the table
        print("Dropping table")
        db.delete_from_table("things")
        db.__del__()


if __name__ == "__main__":
    obj = test_with_one_table()
    if obj:
        print("\n\nTest Passed!\n\n")
