def debug(**kwargs):
    print("**debug**")
    for key, value in kwargs.items():
        print(f"{key}: {value}")



def between(fieldValue: str, bothCompareValues: str):
    """eg '10 and 20'"""
    a, _, b = bothCompareValues.split(" ")
    return int(fieldValue) >= int(a) and int(fieldValue) <= int(b)


switch = {
            ">": lambda x, y:int(x) > int(y),
            "<": lambda x, y: int(x) < int(y),
            "=": lambda x, y: int(x) == int(y),
            "!": lambda x, y: int(x) != int(y),
            "><": between
        }