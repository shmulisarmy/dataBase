def debug(**kwargs):
    print("**debug**")
    for key, value in kwargs.items():
        print(f"{key}: {value}")



def between(fieldValue: str, bothCompareValues: str):
    """eg '10 and 20'"""
    a, _, b = bothCompareValues.split(" ")
    return int(fieldValue) >= int(a) and int(fieldValue) <= int(b)




evaluators = {
        ">": lambda x, y:int(x) > int(y),
        "<": lambda x, y: int(x) < int(y),
        "=": lambda x, y: int(x) == int(y),
        "!": lambda x, y: int(x) != int(y),
        "#": lambda x, y: x in y,
        "==": lambda x, y: x == y,
        "><": between
}


def valid_field(validation_string: str, value: str) -> bool:
    """
    Validate a value against a given condition.
    """
    operator, compare_value = validation_string.split(" ", 1)
    evaluator = evaluators.get(operator)
    if not evaluator:
        raise ValueError(f"Invalid operator '{operator}'")
        
    return evaluator(value, compare_value)