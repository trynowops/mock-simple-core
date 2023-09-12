import os
import sqlite3
from sqlite3 import Error as SqliteError

from typing import Union
from fastapi import FastAPI, HTTPException, Request

CORE_API_KEY = os.environ["CORE_API_KEY"]

app = FastAPI()

create_table_sql = """
CREATE TABLE IF NOT EXISTS platforms (
    id integer PRIMARY KEY,
    domain text NOT NULL
)
"""

insert_platform_sql = """
INSERT INTO platforms (domain)
VALUES  ('trynowtest.com'),
        ('trynow-dev-test.shop.com'),
        ('douberley.me'),
        ('testdomain1.com'),
        ('maksym-trynow-store.myshopify.com'),
        ('trynow-development.myshopify.com'),
        ('scio-mart.myshopify.com'),
        ('trynow-qa-store.myshopify.com'),
        ('trynow-mart.myshopify.com'),
        ('motest-trynow.myshopify.com'),
        ('scio-apparel.myshopify.com'),
        ('dribbble.com'),
        ('jsonpath.com'),
        ('www.trynow.io'),
        ('www.testdev.com'),
        ('sviat-trynow-store0.myshopify.com'),
        ('sviatcheckoutpreview.myshopify.com'),
        ('sviat-test-store.myshopify.com'),
        ('jons-real-test-store.myshopify.com'),
        ('qa-trynow-teststore1.myshopify.com'),
        ('qa-trynow-teststore2.myshopify.com'),
        ('qa-test-store-m.myshopify.com'),
        ('qa-test-store-mo.myshopify.com'),
        ('qa-trynow-teststore8.myshopify.com'),
        ('qa-trynow-teststore7.myshopify.com');
"""


def execute_sql(conn: sqlite3.Connection, sql: str) -> None:
    """
    Execute a SQL statement
    :param conn: Connection object
    :param sql: a SQL statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except SqliteError as e:
        print(e)


def select_all_platforms(conn: sqlite3.Connection) -> list:
    """
    Query all domains in the platforms table
    :param conn: the Connection object
    :return: list of tuples
    """
    cur = conn.cursor()
    cur.execute("SELECT domain FROM platforms")
    return cur.fetchall()


def create_connection() -> Union[sqlite3.Connection, None]:
    """
    Create a database connection to a SQLite in-memory database
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(":memory:")
        return conn
    except SqliteError as e:
        print(e)
    return None


@app.get("/")
def read_root() -> dict:
    """
    Default route
    :return:
    """
    return {}


@app.get("/platforms")
def read_platforms(request: Request) -> dict:
    """
    Get all platforms from the database
    :param request: Request from the client
    :return: dict of platforms
    """
    content_type = request.headers.get("content-type", None)

    if content_type != "application/json":
        raise HTTPException(status_code=400, detail="Invalid Content-Type")

    api_key_header = request.headers.get("core-api-key", None)

    if api_key_header != CORE_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    conn = create_connection()

    if conn is not None:
        execute_sql(conn, create_table_sql)
        execute_sql(conn, insert_platform_sql)
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return {"platforms": select_all_platforms(conn)}
