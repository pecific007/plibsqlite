#!/usr/bin/env python3

import plibsqlite as sql


def print_select_statements(data):
    for d in data:
        print(d)


db = sql.Database("database.db")


def test__create_table(name: str) -> None:
    # Creating table
    print("Create table")
    db.create_table(
        name,
        id="INTEGER PRIMARY KEY",
        name="TEXT NOT NULL",
        desc="TEXT NOT NULL",
    ).exec()


def test__insert_values(name: str):
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
        db.insert(name, name=k, desc=values[k]).exec()


def test__select_values(name: str):
    # Selecting from table
    print("Select from table")
    table_data = db.select(name, "name").exec()
    print("Table data:")
    print_select_statements(table_data)


def test__select_with_where_condition(name: str):
    # Selecting from table with WHERE condition
    print("Selecting with WHERE condition")
    table_data = db.select(name, "*").where("=", vals={"name": "Table"}).exec()
    print("Table data:")
    print_select_statements(table_data)


def test__select_with_order_by_and_limit(name: str):
    # Selecting from table with 'LIMIT' AND 'ORDER'
    print("Selecting with WHERE condition")
    table_data = db.select(name, "*", limit=2, order_by={"ID": "DESC"}).exec()
    print("Table data:")
    print_select_statements(table_data)


def test__update_table(name: str):
    print("Updating columns")
    db.update(name, "=", vals={"name": "Wood Table"}, where={"id": 2}).exec()
    table_data = db.select(name, "*").where("=", {"name": "Wood Table"}).exec()
    print("Table data:")
    print_select_statements(table_data)


def test__join_tables(table1: str, table2: str):
    # Selecting from multiple tables using join
    table_data = (
        db.select(table1, "*")
        .join(table2, operators="=", on={f"{table1}.id": f"{table2}.id"})
        .exec()
    )
    print("Table data:")
    print_select_statements(table_data)


def test__delete_from_table(name: str):
    db.delete(name, "=", vals={"id": 2}).exec()


def test__drop_table(name: str):
    db.drop(name)


if __name__ == "__main__":
    test__create_table("first")
    test__insert_values("first")
    test__select_values("first")
    test__select_with_where_condition("first")
    test__select_with_order_by_and_limit("first")
    test__create_table("second")
    test__insert_values("second")
    test__join_tables("first", "second")
    test__update_table("second")
    test__delete_from_table("second")
    test__drop_table("second")
