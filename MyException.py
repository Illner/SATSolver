class MissingOperandDerivationTreeException(Exception):
    """
    An operand is missing in the prefix expression
    """

    # Constructor
    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("An operand is missing in the prefix expression")
        else:
            super().__init__(message)

class MissingOperatorDerivationTreeException(Exception):
    """
    An operator is missing in the prefix expression
    """

    # Constructor
    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("An operator is missing in the prefix expression")
        else:
            super().__init__(message)

class InvalidOperatorTseitinEncodingException(Exception):
    """
    Invalid operator in derivation tree
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Invalid operator")
        else:
            super().__init__("Invalid operator: " + message)

class InvalidArgumentsFormula2CNFException(Exception):
    """
    Invalid arguments - formula2cnf.py
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Invalid arguments\nformula2cnf.py [-one_sided] [input_path [output_path]]")
        else: 
            super().__init__(message)

class InvalidDIMACSFormatException(Exception):
    """
    Invalid DIMCAS format
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Invalid DIMACS format")
        else:
            super().__init__("Invalid DIMACS format\n" + message)

class InvalidLiteralInPartialAssignmentCnfException(Exception):
    """
    Invalid literal in the partial assignment
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Invalid literal in the partial assignment")
        else:
            super().__init__("Invalid literal in the partial assignment\n" + message)

class UndefinedUnitPropagationCnfException(Exception):
    """
    Undefined unit propagation
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Undefined unit propagation")
        else:
            super().__init__("Undefined unit propagation: " + message)

class SomethingWrongException(Exception):
    """
    Something wrong
    """

    def __init__(self, message):
        if (message == ""):
            super().__init__(message)

class InvalidArgumentsDPLLTaskException(Exception):
    """
    Invalid arguments - dpllTask.py
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Invalid arguments\ndpllTask.py [-DIMACS | -SMT-LIB] input_path")
        else: 
            super().__init__(message)

class InvalidLiteralInLearnedClauseCnfException(Exception):
    """
    Invalid literal in learned clause
    """

    def __init__(self, message):
        super().__init__(message)

class LearnedClauseIdDoesNotExistCnfException(Exception):
    """
    Learned clause ID does not exist
    """

    def __init__(self, message):
        super().__init__(message)

class ClausesDoNotContainLiteralResolutionCnfException(Exception):
    """
    Clauses do not contain literal
    """

    def __init__(self, message):
        super().__init__(message)

class InvalidParametersCnfException(Exception):
    """
    Invalid parameters
    """

    def __init__(self, message):
        super().__init__("Invalid parameters!\n" + message)

class InvalidDecisionLevelCnfException(Exception):
    """
    Invalid decision level
    """

    def __init__(self, message):
        super().__init__("Invalid decision level!\n" + message)

class UndefinedClauseLearningCnfException(Exception):
    """
    Undefined clause learning
    """

    def __init__(self, message):
        super().__init__(message)