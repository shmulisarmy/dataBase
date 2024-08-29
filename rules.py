def is_valid_expression(expression: str) -> bool:
    """
    Determine if a string is an expression operator, becuase if so, then it will need to be evaluated when selecting from or updating the table.
    """
    return expression[0] in [">", "<", "=", "!", "#", "=="]
