class MissingOperandDerivationTreeException(Exception):
    """
    An operand is missing in the prefix expression
    """

    # Constructor
    def __init__(self, message):
        super().__init__(message)

    def __init__(self):
        super().__init__("An operand is missing in the prefix expression")

class MissingOperatorDerivationTreeException(Exception):
    """
    An operator is missing in the prefix expression
    """

    # Constructor
    def __init__(self, message):
        super().__init__(message)

    def __init__(self):
        super().__init__("An operator is missing in the prefix expression")

class InvalidOperatorTseitinEncodingException(Exception):
    """
    Invalid operator in derivative tree
    """

    def __init__(self, message):
        super().__init__("Invalid operator: " + message)

    def __init__(self):
        super().__init__("Invalid operator")