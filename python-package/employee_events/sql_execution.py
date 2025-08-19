# python-package/employee_events/sql_execution.py
from __future__ import annotations
from pathlib import Path
import sqlite3
from sqlite3 import connect  # needed by the "leave this code unchanged" block
from functools import wraps
from typing import Iterable, Optional, Any, Tuple, Union
import pandas as pd

# Required by the template (lowercase!): absolute path to the SQLite file
db_path = Path(__file__).resolve().with_name("employee_events.db")


def sql_query(fn):
    """
    Decorator for query methods that should return a pandas.DataFrame.
    The wrapped function returns either:
      - sql string, or
      - (sql string, params_iterable)
    """
    @wraps(fn)
    def wrapper(self, *args, **kwargs) -> pd.DataFrame:
        result: Union[str, Tuple[str, Iterable[Any]]] = fn(self, *args, **kwargs)
        if isinstance(result, tuple):
            sql, params = result
        else:
            sql, params = result, ()
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description] if cur.description else []
        return pd.DataFrame(rows, columns=cols)
    return wrapper


class SQLExecutionMixin:
    """
    Optional mixin if you want a helper method instead of using @sql_query.
    """
    _db_path = db_path

    def run_sql(self, sql: str, params: Optional[Iterable[Any]] = None) -> pd.DataFrame:
        with sqlite3.connect(self._db_path) as con:
            cur = con.cursor()
            cur.execute(sql, params or ())
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description] if cur.description else []
        return pd.DataFrame(rows, columns=cols)


# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:

    # Returns a pandas DataFrame for the given SQL
    def pandas_query(self, sql: str, params: Optional[Iterable[Any]] = None) -> pd.DataFrame:
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            cur.execute(sql, params or ())
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description] if cur.description else []
        return pd.DataFrame(rows, columns=cols)

    # Returns a list of tuples for the given SQL (cursor.fetchall())
    def query(self, sql: str, params: Optional[Iterable[Any]] = None):
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            cur.execute(sql, params or ())
            return cur.fetchall()


# ---- Leave this code unchanged ----
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """
    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    return run_query
