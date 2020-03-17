import sys
import MyException
from DerivationTree import DerivationTree
from TseitinEncoding import TseitinEncoding

# Variable
input_path = None
input_formula = ""
output_path = None
output_formula = ""
one_sided = False

try:
    # Read arguments
    if (len(sys.argv) > 4):
        raise MyException.InvalidArgumentsFormula2CNFException("Invalid number of arguments")

    for i in range(len(sys.argv)):
        # First argument = program path
        if (i == 0):
            continue

        if (sys.argv[i] == "-one_sided"):
            one_sided = True
        elif (input_path is None):
            input_path = sys.argv[i]
        elif (output_path is None):
            output_path = sys.argv[i]
        else:
            raise MyException.InvalidArgumentsFormula2CNFException()
        
    # Read formula from console
    if (input_path is None):
        input_formula = input("Formula in prefix form: ")
    # Read from file
    else:
        with open(input_path, "r") as input_file:
            input_formula = input_file.read()

    derivationTree = DerivationTree(input_formula)
    tseitinEncoding = TseitinEncoding(derivationTree, one_sided)
    output_formula = str(tseitinEncoding)

    # Write formula in DIMACS format to console
    if (output_path is None):
        print(output_formula)
    # Write formula in DIMACS format to file
    else:
        with open(output_path, "w") as output_file:
            output_file.write(output_formula)

except (MyException.InvalidArgumentsFormula2CNFException, MyException.MissingOperandDerivationTreeException, MyException.MissingOperatorDerivationTreeException) as e:
    print(e)
except FileNotFoundError:
    print("Input file does not exist")
except Exception as e:
    print("Something wrong")
    print(e)