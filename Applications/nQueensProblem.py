from EncodeNQueensProblem import EncodeNQueensProblem

import sys
sys.path.insert(0, '../')

import MyException

# Variable
size_of_board = None
output_path = None

try:
    # Read arguments
    if (len(sys.argv) > 3 or len(sys.argv) == 1):
        raise MyException.InvalidArgumentsNQueensProblemException()

    for i in range(1, len(sys.argv)):
        if (size_of_board is None):
            size_of_board = int(sys.argv[i])
        else:
            output_path = sys.argv[i]

    n_queens_problem = EncodeNQueensProblem(size_of_board)

    # Write formula in DIMACS format to console
    if (output_path is None):
        print(n_queens_problem.DIMACS_format)
    # Write formula in DIMACS format to file
    else:
        n_queens_problem.save_to_file(output_path)

except (MyException.InvalidRowOrColumnEncodeNQueensProblemException, MyException.InvalidSizeOfBoardEncodeNQueensProblemException, MyException.PropositionalVariableDoesNotExistEncodeNQueensProblemException) as e:
    print(e)
except ValueError:
    print("Size of board is not a number!")
except Exception as e:
    print("Something wrong")
    print(e)