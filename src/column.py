from . import table 
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from table import Table




class Column:
    def __init__(self, name: str, length: int, parentTable: 'Table'):
        self.name: str = name
        self.length: int = length
        self.isIndexed: bool = False
        self.isIndexingMap = None
        self.defualt = None
        self.parentTable = parentTable


    def setDefault(self, value: str):
        self.defualt = value


    def index(self):
        if self.isIndexed:
            raise ValueError(f"Column '{self.name}' is already indexed")
        self.isIndexed = True
        self.isIndexingMap = {}

    def __str__(self):
        
        return f"{self.name}: {self.length}"
    

    def __repr__(self):
        return self.__str__()
    

    