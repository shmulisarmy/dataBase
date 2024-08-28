import utils
from sortedcontainers import SortedDict
from typing import Dict, List, Optional, Union
from search_tree_data_structure import SearchTree



class Table:
    def __init__(self, **columns: Dict[str, int]):
        """
        Initialize the table with specified columns and their maximum lengths.
        """
        self.data: List[List[str]] = []
        self.columns: Dict[str, Dict[str, int]] = {}
        self.column_lengths: List[int] = []
        self.field_indexes: Dict[str, int] = {}
        self.mapped_columns: Dict[str, Dict[str, List[int]]] = SortedDict()
        self.defaults: Dict[str, str] = {}
        self.row_count: int = 0

        for field, length in columns.items():
            self.add_column(field, length)

    def is_field_allowed(self, field: str) -> bool:
        """
        Check if a field name is valid in the table.
        """
        if self.is_expression(field):
            _, field = field.split(" ", 1)
        return field in self.columns

    def map_column(self, field: str) -> None:
        """
        Prepare a column for mapping by its values.
        """
        if field not in self.mapped_columns:
            self.mapped_columns[field] = {}

    def add_row(self, **fields: Dict[str, str]) -> None:
        """
        Insert a new row of data into the table.
        """
        for field, value in fields.items():
            if field not in self.columns:
                raise ValueError(f"Column '{field}' does not exist")
            if len(value) > self.columns[field]["length"]:
                raise ValueError(f"Value for column '{field}' is too long")

        for field in self.columns:
            if field not in fields:
                if field not in self.defaults:
                    raise ValueError(f"Column '{field}' does not exist")
                fields[field] = self.defaults[field]

        self.row_count += 1
        row_id = self.row_count

        for field, value in fields.items():
            if field in self.mapped_columns:
                value = str(value)
                if value not in self.mapped_columns[field]:
                    self.mapped_columns[field][value] = []
                self.mapped_columns[field][value].append(row_id)

        self.data.append(list(fields.values()))

    def add_column(self, name: str, length: int) -> None:
        """
        Add a new column with a specified maximum length.
        """
        if name == "orderBy":
            raise ValueError("Column name 'orderBy' is reserved")
        self.field_indexes[name] = len(self.columns)
        self.column_lengths.append(length)
        self.columns[name] = {"length": length}

    def display(self) -> None:
        """
        Print the table's content to the console.
        """
        # Print column headers
        for field, column in self.columns.items():
            print(field.center(column['length']), end=" ")
        print()
        # Print rows
        for row in self.data:
            for i, value in enumerate(row):
                print(value.center(self.column_lengths[i]), end=" ")
            print()

    @staticmethod
    def is_expression(expression: str) -> bool:
        """
        Determine if a string is an expression operator, becuase if so, then it will need to be evaluated when selecting from or updating the table.
        """
        return expression[0] in [">", "<", "=", "!"]

    @staticmethod
    def valid_field(validation_string: str, value: str) -> bool:
        """
        Validate a value against a given condition.
        """
        if not Table.is_expression(validation_string):
            return validation_string == value

        operator, compare_value = validation_string.split(" ", 1)
        func = utils.evaluators.get(operator)
        if func:
            return func(value, compare_value)
        return False

    def select(self, *fields: str, order_by: Optional[str] = None, **conditions: str) -> List[List[str]]:
        """
        Retrieve rows matching specified criteria and optional ordering.
        """
        for field in fields:
            if not self.is_field_allowed(field):
                raise ValueError(f"Column '{field}' does not exist")

        for field in conditions:
            if not self.is_field_allowed(field):
                raise ValueError(f"Column '{field}' does not exist")

        selecting_from = self.data
        if self.mapped_columns:
            first_search_field_candidates = [
                field for field in conditions
                if field in self.mapped_columns and not self.is_expression(conditions[field])
            ]

            def find_length(field: str) -> int:
                value = conditions[field]
                return len(self.mapped_columns[field].get(value, []))

            if first_search_field_candidates:
                best_first_search_field = min(first_search_field_candidates, key=find_length)
                selecting_from = self.mapped_columns[best_first_search_field][conditions[best_first_search_field]]

        ids_of_return_rows: List[int] = []
        return_value: List[List[str]] = []

        for row in selecting_from:
            if all(self.valid_field(conditions[field], row[self.field_indexes[field]]) for field in conditions):
                ids_of_return_rows.append(selecting_from.index(row))

        for row_id in ids_of_return_rows:
            return_value.append([selecting_from[row_id][self.field_indexes[field]] for field in fields])

        return return_value

    def update(self, updates: Dict[str, str], **conditions: str) -> int:
        """
        Modify existing rows based on specified conditions.
        """
        for field in updates:
            if not self.is_field_allowed(field):
                raise ValueError(f"Column '{field}' does not exist")

        for field in conditions:
            if not self.is_field_allowed(field):
                raise ValueError(f"Column '{field}' does not exist")

        selecting_from = self.data
        if self.mapped_columns:
            first_search_field_candidates = [
                field for field in conditions
                if field in self.mapped_columns and not self.is_expression(conditions[field])
            ]

            def find_length(field: str) -> int:
                value = conditions[field]
                return len(self.mapped_columns[field].get(value, []))

            if first_search_field_candidates:
                best_first_search_field = min(first_search_field_candidates, key=find_length)
                selecting_from = self.mapped_columns[best_first_search_field][conditions[best_first_search_field]]

        ids_of_update_rows: List[int] = []

        for row in selecting_from:
            if all(self.valid_field(conditions[field], row[self.field_indexes[field]]) for field in conditions):
                ids_of_update_rows.append(selecting_from.index(row))

        for row_id in ids_of_update_rows:
            for field, new_value in updates.items():
                self.data[row_id][self.field_indexes[field]] = new_value

        return len(ids_of_update_rows)


# Example usage
parties = Table(name=10, people_in_party=3)
users = Table(name=10, age=3, email=30, city=20, country=20, worth=10, __part__id=3)
users.defaults = {"age": "0", "worth": "0", "__part__id": "1"}
users.map_column("name")
users.map_column("age")
users.map_column("worth")

users.add_row(name="John", age="25", email="VrXrL@example.com", city="New York", country="USA", worth="1000000")
users.add_row(name="Jane", age="25", email="Xqg5v@example.com", city="London", country="UK", worth="300")
users.add_row(name="Bob", age="40", email="Xqg5v@example.com", city="Paris", country="France", worth="230000")

users.update({"age": "30000"}, worth="> 3000")

print(users.select("name", "age", worth="> 3000", order_by="worth"))
