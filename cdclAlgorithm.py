import sys
import MyException
from CNF import CNF
from CDCL import CDCL
from DerivationTree import DerivationTree
from TseitinEncoding import TseitinEncoding
from ClauseLearningEnum import ClauseLearningEnum
from RestartStrategyEnum import RestartStrategyEnum
from UnitPropagationEnum import UnitPropagationEnum
from DecisionHeuristicEnum import DecisionHeuristicEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionHowHeuristicEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionWhenHeuristicEnum

# Variable
cnf = None
assumptions = []
input_path = None
DIMACS_format = None

unit_propagation = UnitPropagationEnum.WatchedLiterals
clause_learning = ClauseLearningEnum.StopAtTheFirstUIP
restart_strategy = RestartStrategyEnum.LubyStrategy
clause_deletion_when_heuristic = ClauseDeletionWhenHeuristicEnum.Restart
clause_deletion_how_heuristic = ClauseDeletionHowHeuristicEnum.KeepActiveClauses
decision_heuristic = DecisionHeuristicEnum.eVSIDS

def is_valid_parameter(x, lower_bound = 1, upper_bound = 2):
    """
    Return None if x is not a number or is not in <lower_bound, upper_bound>, otherwise return x
    """
    
    # x is not a number
    if (not x.isnumeric()):
        return None

    number = int(x)
    # x is not in <lower_bound, upper_bound>
    if (number < lower_bound or number > upper_bound):
        return None

    return number

def parse_assumptions(text):
    """
    Return a list of literals
    If text is invalid return None
    """

    if (not text.startswith("[") and not text.endswith("]")):
        return None

    # Remove brackets
    text = text[1:-1]
    
    text = text.replace(" ", "")

    # No assumption
    if (not len(text)):
        return []

    text = text.split(",")
    temp_list = []

    for literal in text:
        try:
            temp_list.append(int(literal))
        except ValueError:
            return None
        
    return temp_list

try:
    # Read arguments
    if ((len(sys.argv) == 1) or (len(sys.argv) > 10)):
        raise MyException.InvalidArgumentsCDCLException("Invalid number of arguments")

    for i in range(1, len(sys.argv)):
        # Type
        if (sys.argv[i] == "-DIMACS"):
            DIMACS_format = True
        elif (sys.argv[i] == "-SMT-LIB"):
            DIMACS_format = False
        # Unit propagation
        elif (sys.argv[i] == "-WatchedLiterals"):
            unit_propagation = UnitPropagationEnum.WatchedLiterals
        elif (sys.argv[i] == "-AdjacencyList"):
            unit_propagation = UnitPropagationEnum.AdjacencyList
        # ClauseLearning
        elif (sys.argv[i].startswith("-ClauseLearning=")):
            number = is_valid_parameter(sys.argv[i][len("-ClauseLearning="):])
            if (number is None):
                raise MyException.InvalidArgumentsCDCLException("ClauseLearning")
            if (number == 1):
                clause_learning = ClauseLearningEnum.StopAtTheFirstUIP
            else:
                clause_learning = ClauseLearningEnum.StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent
        # RestartStrategy
        elif (sys.argv[i].startswith("-RestartStrategy=")):
            number = is_valid_parameter(sys.argv[i][len("-RestartStrategy="):])
            if (number is None):
                raise MyException.InvalidArgumentsCDCLException("RestartStrategy")
            if (number == 1):
                restart_strategy = RestartStrategyEnum.LubyStrategy
            else:
                restart_strategy = RestartStrategyEnum.GeometricStrategy
        # ClauseDeletionWhenHeuristic
        elif (sys.argv[i].startswith("-ClauseDeletionWhenHeuristic=")):
            number = is_valid_parameter(sys.argv[i][len("-ClauseDeletionWhenHeuristic="):])
            if (number is None):
                raise MyException.InvalidArgumentsCDCLException("ClauseDeletionWhenHeuristic")
            if (number == 1):
                clause_deletion_when_heuristic = ClauseDeletionWhenHeuristicEnum.Restart
            else:
                clause_deletion_when_heuristic = ClauseDeletionWhenHeuristicEnum.CacheFull
        # DecisionHeuristic
        elif (sys.argv[i].startswith("-DecisionHeuristic=")):
            number = is_valid_parameter(sys.argv[i][len("-DecisionHeuristic="):], upper_bound=8)
            if (number is None):
                raise MyException.InvalidArgumentsCDCLException("DecisionHeuristic")
            if (number == 1):
                decision_heuristic = DecisionHeuristicEnum.Greedy
            elif (number == 2):
                decision_heuristic = DecisionHeuristicEnum.Random
            elif (number == 3):
                decision_heuristic = DecisionHeuristicEnum.JeroslowWangOneSided
            elif (number == 4):
                decision_heuristic = DecisionHeuristicEnum.JeroslowWangOneSidedDynamic
            elif (number == 5):
                decision_heuristic = DecisionHeuristicEnum.JeroslowWangTwoSided
            elif (number == 6):
                decision_heuristic = DecisionHeuristicEnum.JeroslowWangTwoSidedDynamic
            elif (number == 7):
                decision_heuristic = DecisionHeuristicEnum.VSIDS
            else:
                decision_heuristic = DecisionHeuristicEnum.eVSIDS
        # ClauseDeletionHowHeuristic
        elif (sys.argv[i].startswith("-ClauseDeletionHowHeuristic=")):
            number = is_valid_parameter(sys.argv[i][len("-ClauseDeletionHowHeuristic="):], upper_bound=5)
            if (number is None):
                raise MyException.InvalidArgumentsCDCLException("ClauseDeletionHowHeuristic")
            if (number == 1):
                clause_deletion_how_heuristic = ClauseDeletionHowHeuristicEnum.RemoveSubsumedClauses
            elif (number == 2):
                clause_deletion_how_heuristic = ClauseDeletionHowHeuristicEnum.KeepShortClauses
            elif (number == 3):
                clause_deletion_how_heuristic = ClauseDeletionHowHeuristicEnum.KeepShortClausesAndRemoveSubsumedClauses
            elif (number == 4):
                clause_deletion_how_heuristic = ClauseDeletionHowHeuristicEnum.KeepActiveClauses
            else:
                clause_deletion_how_heuristic = ClauseDeletionHowHeuristicEnum.KeepActiveClausesAndRemoveSubsumedClauses
        # Assumptions
        elif (sys.argv[i].startswith("-Assumptions=")):
            temp = parse_assumptions(sys.argv[i][len("-Assumptions="):])
            if (temp is None):
                raise MyException.InvalidArgumentsCDCLException("Invalid assumptions!")

            assumptions = temp
        else:
            if (input_path is not None):
                raise MyException.InvalidArgumentsCDCLException()
            else:
                input_path = sys.argv[i]
        
    # File format was not implicitly mentioned
    if (DIMACS_format is None):
        temp = input_path.split('.')
        # File does not have any extension
        if (len(temp) == 1):
            raise FileExistsError("Invalid file extension")
        if (temp[-1] == "cnf"):
            DIMACS_format = True
        elif (temp[-1] == "sat"):
            DIMACS_format = False
        else:
            raise FileExistsError("Invalid file extension")

    # Read from file
    with open(input_path, "r") as input_file:
        input_formula = input_file.read()

    if (not DIMACS_format):
        derivationTree = DerivationTree(input_formula)
        tseitinEncoding = TseitinEncoding(derivationTree)
        cnf = CNF(str(tseitinEncoding), tseitinEncoding.original_variable_dictionary, 
                  unit_propagation_enum=unit_propagation,
                  decision_heuristic_enum=decision_heuristic,
                  clause_learning_enum=clause_learning, 
                  clause_deletion_how_heuristic_enum=clause_deletion_how_heuristic, 
                  clause_deletion_when_heuristic_enum=clause_deletion_when_heuristic,
                  restart_strategy_enum=restart_strategy)
    else:
        cnf = CNF(input_formula, 
                  unit_propagation_enum=unit_propagation,
                  decision_heuristic_enum=decision_heuristic,
                  clause_learning_enum=clause_learning, 
                  clause_deletion_how_heuristic_enum=clause_deletion_how_heuristic,
                  clause_deletion_when_heuristic_enum=clause_deletion_when_heuristic,
                  restart_strategy_enum=restart_strategy)
        
    cdcl = CDCL(cnf, assumptions=assumptions)
    result = cdcl.CDCL()

    print("Total CPU time: " + str(cdcl.time) + "s")
    print("Number of decisions: " + str(cdcl.number_of_decisions))
    print("Number of steps of unit propagation: " + str(cdcl.number_of_steps_of_unit_propagation))
    print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))
    print("Number of deleted learned clauses: " + str(cnf.number_of_deleted_learned_clauses))
    print("Number of clause deletions: " + str(cnf.number_of_clause_deletions))
    print("Number of contradictions: " + str(cnf.number_of_contradictions))
    print("Number of contradictions caused by learned clauses: " + str(cnf.number_of_contradictions_caused_by_learned_clauses))
    print("Number of unit propagations: " + str(cnf.number_of_unit_propagations))
    print("Number of unit propagations caused by learned clauses: " + str(cnf.number_of_unit_propagations_caused_by_learned_clauses))
    print("Number of restarts: " + str(cnf.number_of_restarts))

    if (result is None):
        print("-----")
        print("UNSAT")
        print("-----")
    else:
        print("---")
        print("SAT")
        print("---")
        print(result)

    if (not cnf.verify(result)):
        raise MyException.SomethingWrongException("Invalid model")

except (MyException.InvalidArgumentsCDCLException, 
        MyException.MissingOperandDerivationTreeException, 
        MyException.MissingOperatorDerivationTreeException, 
        MyException.InvalidDIMACSFormatException,
        MyException.UndefinedUnitPropagationCnfException,
        FileExistsError) as e:
    print(e)
except FileNotFoundError:
    print("Input file does not exist")