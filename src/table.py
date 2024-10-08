from .import rules
from .import utils
from .column import Column
from sortedcontainers import SortedDict
from typing import Dict, List, Optional, Union, TYPE_CHECKING



if TYPE_CHECKING:
    from column import Column

class Table:
    def __init__(self, **columns: Dict[str, int]):
        """
        Initialize the table with specified columns and their maximum lengths.
        """
        self.data: List[List[str]] = []
        self.columns: Dict[str, 'Column'] = {}
        self.field_indexes: Dict[str, int] = {}
        self.mapped_columns: Dict[str, Dict[str, List[int]]] = SortedDict()
        self.defaults: Dict[str, str] = {}
        self.row_count: int = 0
        self.columnNames: List[str] = []

        for field, length in columns.items():
            self.add_column(field, length)

    def indexCollumn(self, field: str) -> None:
        """
        Prepare a column for mapping by its values.
        """
        column = self.columns.get(field)
        if not column:  
            raise ValueError(f"Column '{field}' does not exist")

        column.index()

    def add_row(self, **fields: Dict[str, str]) -> None:
        """
        Insert a new row of data into the table.
        """
        for field, value in fields.items():
            if field not in self.columns:
                raise ValueError(f"Column '{field}' does not exist")
            if len(value) > self.columns[field].length:
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
        

        if name in self.columns:
            raise ValueError(f"Column '{name}' already exists")
        
        self.field_indexes[name] = len(self.columns)
        self.columns[name] = Column(name, length, self)
        self.columnNames.append(name)

    def display(self) -> None:
        """
        Print the table's content to the console.
        """
        # Print column headers
        for field, column in self.columns.items():
            print(field.center(column.length), end=" ")
        print()
        # Print rows
        for row in self.data:
            for i, value in enumerate(row):
                print(value.center(self.columns[self.columnNames[i]].length), end=" ")
            print()


    def findValidRows(self, conditions: Dict[str, str]) -> List[tuple[str]]:
        for field in conditions:
            if not field in self.columns:
                raise ValueError(f"Column '{field}' does not exist")
            
        """we set selecting_from to self.data but then we see if\n
        we can find a field that can be used to narrow down the search"""

        
        selecting_from = self.data
        if self.mapped_columns:
            first_search_field_candidates: List[str] = [
                field for field in conditions
                if field in self.mapped_columns and utils.indexable(conditions[field])
            ]

            def find_length(field: str) -> int:
                condition = conditions[field]
                return len(self.mapped_columns[field].get(condition, []))

            if first_search_field_candidates:
                best_first_search_field = min(first_search_field_candidates, key=find_length)
                selecting_from = self.mapped_columns[best_first_search_field][conditions[best_first_search_field]]
                # becuase we're allready using it to validate
                del conditions[best_first_search_field]

        ids_of_return_rows: List[int] = []

        for row in selecting_from:
            row: List[str]
            shouldAdd = True
            for field in conditions:
                cellValue = row[self.field_indexes[field]]
                condition: str = conditions[field]
                if not utils.validate(condition, cellValue):
                    shouldAdd = False
                    break
            if shouldAdd:
                ids_of_return_rows.append(selecting_from.index(row))

        return ids_of_return_rows
    def select(self, *fields: str, **conditions: str) -> List[List[str]]:
        """
        Retrieve rows matching specified criteria and optional ordering.
        """
        for field in fields:
            if not field in self.columns:
                raise ValueError(f"Column '{field}' does not exist")

        

        ids_of_return_rows: List[int] = self.findValidRows(conditions)
        return_value: List[List[str]] = []


        for row_id in ids_of_return_rows:
            return_value.append([self.data[row_id][self.field_indexes[field]] for field in fields])

        return return_value

    def update(self, updates: Dict[str, str], **conditions: str) -> int:
        """
        Modify existing rows based on specified conditions.
        """

        ids_of_update_rows: List[int] = self.findValidRows(conditions)

        for row_id in ids_of_update_rows:
            for field, new_value in updates.items():
                self.data[row_id][self.field_indexes[field]] = new_value

        return len(ids_of_update_rows)