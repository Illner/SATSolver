import sys
import MyException
from CNF import CNF
from CDCL import CDCL
from DerivationTree import DerivationTree
from TseitinEncoding import TseitinEncoding
from ClauseLearningEnum import ClauseLearningEnum
from UnitPropagationEnum import UnitPropagationEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionHowHeuristicEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionWhenHeuristicEnum

# Variable
cnf = None
input_path = None
DIMACS_format = None

try:
    # Read arguments
    if ((len(sys.argv) == 1) or (len(sys.argv) > 3)):
        raise MyException.InvalidArgumentsDPLLTaskException("Invalid number of arguments")

    for i in range(1, len(sys.argv)):
        if (sys.argv[i] == "-DIMACS"):
            DIMACS_format = True
        elif (sys.argv[i] == "-SMT-LIB"):
            DIMACS_format = False
        else:
            if (input_path is not None):
                raise MyException.InvalidArgumentsDPLLTaskException()
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
        cnf = CNF(str(tseitinEncoding), tseitinEncoding.original_variable_dictionary, unit_propagation_enum=UnitPropagationEnum.AdjacencyList, clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClausesAndRemoveSubsumedClauses)
    else:
        cnf = CNF(input_formula, unit_propagation_enum=UnitPropagationEnum.AdjacencyList, clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClausesAndRemoveSubsumedClauses)
        
    cdcl = CDCL(cnf)
    result = cdcl.CDCL()

    print("Total CPU time: " + str(cdcl.time) + "s")
    print("Number of decisions: " + str(cdcl.number_of_decisions))
    print("Number of steps of unit propagation: " + str(cdcl.number_of_steps_of_unit_propagation))
    print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))

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

except (MyException.InvalidArgumentsDPLLTaskException, 
        MyException.MissingOperandDerivationTreeException, 
        MyException.MissingOperatorDerivationTreeException, 
        MyException.InvalidDIMACSFormatException,
        MyException.UndefinedUnitPropagationCnfException,
        FileExistsError) as e:
    print(e)
except FileNotFoundError:
    print("Input file does not exist")