#!/usr/bin/env python3

import plibsqlite as sql


def print_select_statements(data):
    for d in data:
        print(d)


db = sql.Database("database.db")


def test__create_table() -> None:
    # Creating table
    print("Create table")
    db.create_table(
        "things",
        ID="INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT",
        THING_NAME="TEXT NOT NULL",
        THING_DESC="TEXT NOT NULL",
    ).exec()


def test__insert_values():
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
        db.insert("things", THING_NAME=k, THING_DESC=values[k]).exec()


def test__select_values():
    # Selecting from table
    print("Select from table")
    table_data = db.select("things", "THING_NAME").exec()
    print_select_statements(table_data)
    print("Table data:")


def test__select_with_where_condition():
    # Selecting from table with WHERE condition
    print("Selecting with WHERE condition")
    table_data = db.select("things", "*").where("=", THING_NAME="Table").exec()
    print("Table data:")
    print_select_statements(table_data)


def test__select_with_order_by_and_limit():
    # Selecting from table with WHERE condition AND 'LIMIT' AND 'ORDER'
    print("Selecting with WHERE condition")
    table_data = db.select("things", "*", limit=2, order_by={"ID": "DESC"}).exec()
    print("Table data:")
    print_select_statements(table_data)


if __name__ == "__main__":
    test__create_table()
    test__insert_values()
    test__select_values()
    test__select_with_where_condition()
    test__select_with_order_by_and_limit()
