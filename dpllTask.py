import sys
import MyException
from CNF import CNF
from DPLL import DPLL
from DerivationTree import DerivationTree
from TseitinEncoding import TseitinEncoding
from UnitPropagationEnum import UnitPropagationEnum

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
        cnf = CNF(str(tseitinEncoding), tseitinEncoding.original_variable_dictionary)
    else:
        cnf = CNF(input_formula, unit_propagation_enum=UnitPropagationEnum.AdjacencyList)

    dpll = DPLL(cnf)
    result = dpll.DPLL()

    print("Total CPU time: " + str(dpll.time) + "s")
    print("Number of decisions: " + str(dpll.number_of_decisions))
    print("Number of steps of unit propagation: " + str(dpll.number_of_steps_of_unit_propagation))

    if (result is None):
        print("-----")
        print("UNSAT")
        print("-----")
    else:
        print("---")
        print("SAT")
        print("---")
        print(result)

except (MyException.InvalidArgumentsDPLLTaskException, 
        MyException.MissingOperandDerivationTreeException, 
        MyException.MissingOperatorDerivationTreeException, 
        MyException.InvalidDIMACSFormatException,
        MyException.UndefinedUnitPropagationCnfException,
        FileExistsError) as e:
    print(e)
except FileNotFoundError:
    print("Input file does not exist")