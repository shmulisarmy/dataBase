from .import rules
from .import utils
from sortedcontainers import SortedDict
from typing import Dict, List, Optional, Union

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

    def select(self, *fields: str, order_by: Optional[str] = None, **conditions: str) -> List[List[str]]:
        """
        Retrieve rows matching specified criteria and optional ordering.
        """
        for field in fields:
            if not field in self.columns:
                raise ValueError(f"Column '{field}' does not exist")

        for field in conditions:
            if not field in self.columns:
                raise ValueError(f"Column '{field}' does not exist")

        selecting_from = self.data
        if self.mapped_columns:
            first_search_field_candidates = [
                field for field in conditions
                if field in self.mapped_columns and not rules.is_valid_expression(conditions[field])
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
            if all(utils.valid_field(conditions[field], row[self.field_indexes[field]]) for field in conditions):
                ids_of_return_rows.append(selecting_from.index(row))

        for row_id in ids_of_return_rows:
            return_value.append([selecting_from[row_id][self.field_indexes[field]] for field in fields])

        return return_value

    def update(self, updates: Dict[str, str], **conditions: str) -> int:
        """
        Modify existing rows based on specified conditions.
        """
        for field in updates:
            if not field in self.columns:
                raise ValueError(f"Column '{field}' does not exist")

        for field in conditions:
            if not field in self.columns:
                raise ValueError(f"Column '{field}' does not exist")

        selecting_from = self.data
        if self.mapped_columns:
            first_search_field_candidates = [
                field for field in conditions
                if field in self.mapped_columns and not rules.is_valid_expression(conditions[field])
            ]

            def find_length(field: str) -> int:
                value = conditions[field]
                return len(self.mapped_columns[field].get(value, []))

            if first_search_field_candidates:
                best_first_search_field = min(first_search_field_candidates, key=find_length)
                selecting_from = self.mapped_columns[best_first_search_field][conditions[best_first_search_field]]

        ids_of_update_rows: List[int] = []

        for row in selecting_from:
            if all(utils.valid_field(conditions[field], row[self.field_indexes[field]]) for field in conditions):
                ids_of_update_rows.append(selecting_from.index(row))

        for row_id in ids_of_update_rows:
            for field, new_value in updates.items():
                self.data[row_id][self.field_indexes[field]] = new_value

        return len(ids_of_update_rows)