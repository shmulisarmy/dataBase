import utils
from sortedcontainers import SortedDict


class table:
    def __init__(self, **columns: dict[str, int]):
        self.data: list[list] = []
        self.columns: dict[str, int] = {}
        self.columnsLengthList: list[int] = []
        self.fieldIdexs: dict[str, int] = {}
        self.indexedColumns: dict[int, str] = {}
        self.mappedColumns: dict[str, dict[str, list[int]]] = SortedDict()
        self.rowCount: int = 0
        for field in columns:
            self.add_column(field, columns[field])
            

    def allowedField(self, field: str) -> bool:
        if table.isExpression(field):
            operator, field = field.split(" ")

        return field in self.columns
    
    def mapColumn(self, field: str) -> list[int]:
        if self.mappedColumns.get(field):
            return
        self.mappedColumns[field] = {}

    def add_row(self, **fields: dict[str, str]):
        for field in fields:
            if field not in self.columns:
                raise Exception(f"Column {field} does not exist")
            if len(fields[field]) > self.columns[field]["length"]:
                raise Exception(f"Column {field} is too long")
            
        for field in self.columns:
            if field not in fields:
                raise Exception(f"Column {field} does not exist")
            
        self.rowCount += 1
        id = self.rowCount

        for field in self.mappedColumns:
            value = str(fields[field])
            # if field not in self.mappedColumns[field]:
            #     self.mappedColumns[field] = {}
            if not self.mappedColumns[field].get(value):
                self.mappedColumns[field][value] = []
            self.mappedColumns[field][value].append(id)

        self.data.append(list(fields.values()))

    def add_column(self, name: str, length: int):
        if name == "orderBy":
            raise Exception("Column name 'orderBy' is reserved")
        self.fieldIdexs[name] = len(self.columns)
        self.columnsLengthList.append(length)
        self.columns[name] = {}
        self.columns[name]["length"] = length

    def display(self):
        for field in self.columns:
            print(field.center(self.columns[field]['length']), end=" ")
        print()
        for row in self.data:
            for i in range(len(row)):
               print(row[i].center(self.columnsLengthList[i]), end=" ")
            print()

    @staticmethod
    def isExpression(expression: str) -> bool:
        return expression[0] in [">", "<", "=", "!"]
        

    @staticmethod
    def validField(validationString: str, value: str) -> bool:
        if not table.isExpression(validationString):
            return validationString == value
        
        operator, compareValue = validationString.split(" ", maxsplit=1)
        func = utils.switch[operator]
        return func(value, compareValue)
        

    def select(self, *searchingFor: list[str], orderBy = None, **wheres: dict[str, str]) -> list[list[str]]:
        for field in searchingFor:
            field: str
            if not self.allowedField(field):
                raise Exception(f"Column {field} does not exist")

        for field in wheres:
            if not self.allowedField(field):
                raise Exception(f"Column {field} does not exist")
            


        
        if self.mappedColumns:
            #the smaller we can reduce the amount of data we need to search the better
            FirstSearchFieldCanidates = filter(lambda x: x in wheres and not table.isExpression(wheres[field]), self.mappedColumns.keys())
            FirstSearchFieldCanidates = list(FirstSearchFieldCanidates)
            def findLength(x):
                Map = self.mappedColumns[x]
                value = wheres[x]
                f = Map[value]
                return len(f)
            if not FirstSearchFieldCanidates:
                selectingFrom = self.data
            else:
                bestFirstSearchField = min(FirstSearchFieldCanidates, key=findLength)
                selectingFrom = self.mappedColumns[bestFirstSearchField][wheres[bestFirstSearchField]]        
        
        
        idsOfreturnRows: list[int] = []
        returnValue: list[list[str]] = []

        for row in selectingFrom:
            if all(table.validField(wheres[field], row[self.fieldIdexs[field]]) for field in wheres):
                idsOfreturnRows.append(selectingFrom.index(row))

        for id in idsOfreturnRows:
            returnValue.append([])
            for field in searchingFor:
                returnValue[-1].append(selectingFrom[id][self.fieldIdexs[field]])

        return returnValue
        
users = table(name = 10, age = 3, email = 30, city = 20, country = 20, worth = 10)
users.mapColumn("name")
users.mapColumn("age")
users.mapColumn("worth")

users.add_row(name = "John", age = "25", email = "VrXrL@example.com", city = "New York", country = "USA", worth = "1000000")
users.add_row(name = "Jane", age = "25", email = "Xqg5v@example.com", city = "London", country = "UK", worth = "300")
users.add_row(name = "Bob", age = "40", email = "Xqg5v@example.com", city = "Paris", country = "France", worth = "230000")




print(users.select("name", "age", age = ">< 10 and 300", worth = "> 3000", orderBy="worth"))
