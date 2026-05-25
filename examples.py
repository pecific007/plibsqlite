#!/usr/bin/env python3

import plibsqlite as sql


def print_select_statements(data) -> None:
    for d in data:
        print(d)
    return


db = sql.Database("database.db")


def get_schema() -> None:
    db.schema()
    return


def example__create_table(name: str) -> None:
    # Creating table
    print("Create table")
    db.create_table(
        name,
        id="INTEGER PRIMARY KEY",
        name="TEXT NOT NULL",
        desc="TEXT NOT NULL",
    )
    return


def example__insert_values(name: str) -> None:
    # Adding values to table
    print("Insert values")
    values = {
        "Cooler": "For summer",
        "Table": "Wooden and used",
        "GNU/Linux": "Operating System",
        "Niri": "Scrolling Window Manager",
        "Wallpaper": "Earth",
    }
    for k in values:
        db.insert(name, name=k, desc=values[k]).exec()
    return


def example__select_values(name: str) -> None:
    # Selecting from table
    print("Select from table")
    table_data = db.select("name", name).exec()
    print("Table data:")
    print_select_statements(table_data)
    return


def example__select_with_where_condition(name: str) -> None:
    # Selecting from table with WHERE condition
    print("Selecting with WHERE condition")
    table_data = db.select("*", name).where("=", vals={"name": "Table"}).exec()
    print("Table data:")
    print_select_statements(table_data)
    return


def example__select_with_order_by_and_limit(name: str) -> None:
    # Selecting from table with 'LIMIT' AND 'ORDER'
    print("Selecting with ORDER BY and LIMIT")
    table_data = db.select("*", name).order_by({"id": "DESC"}).limit(2).exec()
    print("Table data:")
    print_select_statements(table_data)
    return


def example__update_table(name: str) -> None:
    print("Updating columns")
    db.update(name, "=", vals={"name": "Wood Table"}, where={"id": 2}).exec()
    table_data = db.select("*", name).where("=", {"name": "Wood Table"}).exec()
    print("Table data:")
    print_select_statements(table_data)
    return


def example__join_tables(table1: str, table2: str) -> None:
    # Selecting from multiple tables using join
    print("Joining tables")
    table_data = (
        db.select("*", table1)
        .join(table2, operators="=", on={f"{table1}.id": f"{table2}.id"})
        .exec()
    )
    print("Table data:")
    print_select_statements(table_data)
    return


def example__select_using_condition_method(name: str) -> None:
    # Selecting from table using condition method
    print("Selecting using Condition")
    table_data = (
        db.select("*", name)
        .where("=", {"id": 1})
        .condition("AND", "=", {"name": "Cooler"})
    ).exec()
    print("Table data:")
    print_select_statements(table_data)
    return


def example__select_with_where_in_condition(table1: str, table2: str) -> None:
    # Selecting from tables using WHERE col IN (SELECT ...)
    print("Selecting using WHERE _ IN")
    table_data = (
        db.select("name", table1).where("IN", "id").select("id", table2).out()
    ).exec()
    print("Table data:")
    print_select_statements(table_data)
    return


def example__delete_from_table(name: str) -> None:
    print("Deleting from table")
    db.delete(name, "=", vals={"id": 2}).exec()
    return


def example__drop_table(name: str) -> None:
    print("Dropping table")
    db.drop(name)
    return


if __name__ == "__main__":
    get_schema()
    example__create_table("first")
    example__insert_values("first")
    example__select_values("first")
    example__select_with_where_condition("first")
    example__select_with_order_by_and_limit("first")
    example__create_table("second")
    example__insert_values("second")
    example__select_with_where_in_condition("first", "second")
    example__select_using_condition_method("second")
    example__join_tables("first", "second")
    example__update_table("second")
    example__delete_from_table("second")
    example__drop_table("second")
    example__drop_table("first")
