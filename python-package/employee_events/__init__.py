# python-package/employee_events/__init__.py

from .employee import Employee
from .team import Team
from .query_base import QueryBase
from .sql_execution import *  # exposes: sql_query, query, SQLExecutionMixin, QueryMixin, db_path (etc.)

# (Optional but recommended) limit what the package exports:
__all__ = [
    "Employee",
    "Team",
    "QueryBase",
    # from sql_execution:
    "sql_query",
    "query",
    "SQLExecutionMixin",
    "QueryMixin",
    "db_path",
]
