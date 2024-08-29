from table import Table


class DataBase:
    def __init__(self, name: str):
        self.name: str = name
        self.tables: dict[Table] = {}
    
    
    def createTable(self, table_name: str, **columns: dict) -> Table:
        self.tables[table_name] = Table(**columns)
        return self.tables[table_name]