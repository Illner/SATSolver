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
    Invalid arguments - dpllAlgorithm.py
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Invalid arguments\ndpllAlgorithm.py [-DIMACS | -SMT-LIB] input_path")
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

class UndefinedDecisionHeuristicCnfException(Exception):
    """
    Undefined decision heuristic
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Undefined decision heuristic")
        else:
            super().__init__("Undefined decision heuristic: " + message)

class UndefinedRestartStrategyCnfException(Exception):
    """
    Undefined restart strategy
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Undefined restart strategy")
        else:
            super().__init__("Undefined restart strategy: " + message)

class AttemptToDeleteActiveLearnedClauseCnfException(Exception):
    """
    Attempt to delete active learned clause
    """

    def __init__(self):
        super().__init__()

class UndefinedClauseDeletionHowHeuristicCnfException(Exception):
    """
    Undefined clause deletion (how) heuristic
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Undefined clause deletion (how) heuristic")
        else:
            super().__init__("Undefined clause deletion (how) heuristic: " + message)

class UndefinedClauseDeletionWhenHeuristicCnfException(Exception):
    """
    Undefined clause deletion (when) heuristic
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Undefined clause deletion (when) heuristic")
        else:
            super().__init__("Undefined clause deletion (when) heuristic: " + message)

class InvalidArgumentsCDCLException(Exception):
    """
    Invalid arguments - cdclAlgorithm.py
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("cdclAlgorithm.py [-ClauseLearning=X] [-RestartStrategy=X] [-ClauseDeletionWhenHeuristic=X] [-ClauseDeletionHowHeuristic=X] [-DecisionHeuristic=X] [-WatchedLiterals | -AdjacencyList [-DIMACS | -SMT-LIB] input_path")
        else: 
            super().__init__("Invalid argument " + message)

class UndefinedDecisionHeuristicCnfException(Exception):
    """
    Undefined decision heuristic
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Undefined decision heuristic")
        else:
            super().__init__("Undefined decision heuristic: " + message)

class VariableDoesNotExistCnfException(Exception):
    """
    Variable does not exist
    """

    def __init__(self, message):
        super().__init__("Variable does not exist: " + message)

class ClauseDoesNotCauseAContradictionCnfException(Exception):
    """
    Clause does not cause a contradiction
    """

    def __init__(self, message = ""):
        if (message == ""):
            super().__init__("Clause does not cause a contradiction!")
        else:
            super().__init__("Clause does not cause a contradiction: " + message) 