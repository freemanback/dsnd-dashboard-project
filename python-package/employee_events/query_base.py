# python-package/employee_events/query_base.py

# Import any dependencies needed to execute sql queries
from __future__ import annotations
from .sql_execution import sql_query  # decorator that executes SQL and returns a DataFrame


# Define a class called QueryBase
# Use inheritance to add methods
# for querying the employee_events database.
class QueryBase:
    # Create a class attribute called `name`
    # set the attribute to an empty string
    name: str = ""   # subclasses must set to "employee" or "team"

    def _id_col(self) -> str:
        if not self.name:
            raise ValueError("Subclass must set `name` to 'employee' or 'team'.")
        return f"{self.name}_id"

    # Define a `names` method that receives
    # no passed arguments
    def names(self):
        # Return an empty list
        return []

    # Define an `event_counts` method
    # that receives an `id` argument
    # This method should return a pandas dataframe
    @sql_query
    def event_counts(self, id: int):
        # QUERY 1
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set the FROM {table}
        # to the `name` class attribute
        # Use f-string formatting to set the name
        # of id columns used for joining
        # order by the event_date column
        id_col = self._id_col()
        sql = f"""
        SELECT
            ev.event_date,
            SUM(ev.positive_events) AS positive_events,
            SUM(ev.negative_events) AS negative_events,
            SUM(ev.positive_events - ev.negative_events) AS net_events
        FROM {self.name} AS t
        JOIN employee_events AS ev
            ON ev.{id_col} = t.{id_col}
        WHERE t.{id_col} = ?
        GROUP BY ev.event_date
        ORDER BY ev.event_date
        """
        return sql, (id,)

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    @sql_query
    def notes(self, id: int):
        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        id_col = self._id_col()
        sql = f"""
        SELECT
            n.note_date,
            n.note
        FROM {self.name} AS t
        JOIN notes AS n
            ON n.{id_col} = t.{id_col}
        WHERE t.{id_col} = ?
        ORDER BY n.note_date DESC
        """
        return sql, (id,)
