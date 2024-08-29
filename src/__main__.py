from typing import TYPE_CHECKING
from .dataBase import DataBase
# from search_tree_data_structure import SearchTree


if TYPE_CHECKING:
    from table import Table

db = DataBase("test")


# Example usage
parties: 'Table' = db.createTable("parties", name=10, people_in_party=3)
users: 'Table' = db.createTable("users", name=10, age=3, email=30, city=20, country=20, worth=10, __part__id=3)
users.defaults = {"age": "0", "worth": "0", "__part__id": "1"}
users.map_column("name")
users.map_column("age")
users.map_column("worth")

users.add_row(name="John", age="25", email="VrXrL@example.com", city="New York", country="USA", worth="1000000")
users.add_row(name="Jane", age="25", email="Xqg5v@example.com", city="London", country="UK", worth="300")
users.add_row(name="Bob", age="40", email="Xqg5v@example.com", city="Paris", country="France", worth="230000")

users.update({"age": "30000"}, worth="> 3000")

print(users.select("name", "age", worth="> 3000", order_by="worth"))
