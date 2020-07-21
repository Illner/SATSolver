import copy
import math
import numpy as np
from io import StringIO
    
import sys
sys.path.insert(0, '../')

import MyException

class EncodeNQueensProblem:
    """
    Encode N-queens problem in a SAT problem (DIMACS format)
    """

    MIN_SIZE_OF_BOARD = 1
    MAX_SIZE_OF_BOARD = 1000

    # Constructor
    def __init__(self, size_of_board):
        """
        int size_of_board
        int number_of_clauses
        StringIO DIMACS_format
        int number_of_propositional_variables
        int[] map_propositional_variable_to_board
        int[][] map_board_to_propositional_variable
        """

        # size_of_board is not a number
        if (not isinstance(size_of_board, int)):
            raise MyException.InvalidSizeOfBoardEncodeNQueensProblemException("\"" + str(size_of_board) + "\"" + " is not a number")

        if (size_of_board < self.MIN_SIZE_OF_BOARD or size_of_board > self.MAX_SIZE_OF_BOARD):
            raise MyException.InvalidSizeOfBoardEncodeNQueensProblemException("{0} (MinValue: {1}, MaxValue: {2})".format(size_of_board, self.MIN_SIZE_OF_BOARD, self.MAX_SIZE_OF_BOARD))

        self.__size_of_board = size_of_board
        self.__number_of_clauses = None
        self.__DIMACS_format = StringIO()
        self.__map_board_to_propositional_variable = []
        self.__map_propositional_variable_to_board = []

        # Initialize propositional variables
        propositional_variable = 0
        self.__map_propositional_variable_to_board.append(None)
        for r in range(self.__size_of_board):
            self.__map_board_to_propositional_variable.append([])
            for c in range(self.__size_of_board):
                propositional_variable += 1
                self.__map_board_to_propositional_variable[r].append(propositional_variable)
                self.__map_propositional_variable_to_board.append((r, c))

        self.__number_of_propositional_variables = propositional_variable

        self.__encode()

    # Method
    def __is_valid_row_or_column(self, row_or_column):
        """
        Return True if row (column) is valid, otherwise False
        """

        if (row_or_column < 0 or row_or_column >= self.__size_of_board):
            return False

        return True

    def __get_propositional_variable(self, row, column):
        if (not self.__is_valid_row_or_column(row) or not self.__is_valid_row_or_column(column)):
            raise MyException.InvalidRowOrColumnEncodeNQueensProblemException("row: {0}, column: {1}".format(row, column))

        return self.__map_board_to_propositional_variable[row][column]

    def __get_board_coordinate(self, propositional_variable):
        if (propositional_variable <= 0 or propositional_variable > self.__number_of_propositional_variables):
            raise MyException.PropositionalVariableDoesNotExistEncodeNQueensProblemException(str(propositional_variable))

        return self.__map_propositional_variable_to_board[propositional_variable]

    def draw_propositional_variables_in_board(self):
        string = StringIO()

        for r in range(self.__size_of_board):
            for c in range(self.__size_of_board):
                string.write("({0}, {1}): {2}\t".format(r, c, self.__get_propositional_variable(r, c)))
            string.write("\n")

        return string.getvalue()

    def save_to_file(self, file_path):
        try:
            with open(file_path, "w") as file:
                file.write(self.__DIMACS_format.getvalue())
        except Exception as e:
            print("Something wrong")
            print(e)

    def __encode(self):
        # Comments
        if (self.__size_of_board == 1):
            self.__write("c {0}-queen problem".format(self.__size_of_board))
        else:
            self.__write("c {0}-queens problem".format(self.__size_of_board))
        self.__new_line()

        self.__write("c \t")
        for i in range(self.__size_of_board):
            self.__write("\t {0}.col".format(i + 1))
        self.__new_line()

        for r in range(self.__size_of_board):
            self.__write("c {0}. row: ".format(r + 1))
            for column in self.__map_board_to_propositional_variable[r]:
                self.__write("\t {0}".format(column))
            self.__new_line()
        
        # P
        temp_list = [self.__comb(n, 2) for n in range(2, self.__size_of_board + 1)]
        temp_sum = 2 * (2 * sum(temp_list) - self.__comb(self.__size_of_board, 2))
        self.__number_of_clauses = self.__size_of_board + self.__size_of_board + self.__size_of_board * (self.__size_of_board * (self.__size_of_board + 1) - 2 * self.__size_of_board) + temp_sum

        self.__write("p cnf {0} {1}".format(self.__number_of_propositional_variables, self.__number_of_clauses))
        self.__new_line()

        # Clauses
        # Each row contains a queen
        for r in range(self.__size_of_board):
            for c in range(self.__size_of_board):
                self.__write("{0} ".format(self.__get_propositional_variable(r, c)))
            self.__write(" 0")
            self.__new_line()

        # Each column contains a queen
        for c in range(self.__size_of_board):
            for r in range(self.__size_of_board):
                self.__write("{0} ".format(self.__get_propositional_variable(r, c)))
            self.__write(" 0")
            self.__new_line()

        # Conflict clauses
        # Row
        for r in range(self.__size_of_board):
            for i in range(self.__size_of_board - 1):
                for j in range(i + 1, self.__size_of_board):
                    self.__write("-{0} -{1} 0".format(self.__get_propositional_variable(r, i), self.__get_propositional_variable(r, j)))
                    self.__new_line()

        # Column
        for c in range(self.__size_of_board):
            for i in range(self.__size_of_board - 1):
                for j in range(i + 1, self.__size_of_board):
                    self.__write("-{0} -{1} 0".format(self.__get_propositional_variable(i, c), self.__get_propositional_variable(j, c)))
                    self.__new_line()

        # Diagonal
        temp_array = np.array(self.__map_board_to_propositional_variable)
        diagonal_list = [temp_array[::-1,:].diagonal(i) for i in range(-temp_array.shape[0] + 1,temp_array.shape[1])]
        diagonal_list.extend(temp_array.diagonal(i) for i in range(temp_array.shape[1] - 1,-temp_array.shape[0],-1))

        for diagonal in diagonal_list:
            if (len(diagonal) < 2):
                continue

            for i in range(len(diagonal) - 1):
                for j in range(i + 1, len(diagonal)):
                    self.__write("-{0} -{1} 0".format(diagonal[i], diagonal[j]))
                    self.__new_line()

    def __comb(self, n, k):
        if n < k:
            return 0
        
        return int((math.factorial(n)) / (math.factorial(k) * math.factorial(n - k)))

    def __write(self, string):
        self.__DIMACS_format.write(string)

    def __new_line(self):
        self.__DIMACS_format.write("\n")

    def __str__(self):
        return self.__DIMACS_format.getvalue()

    @property
    def size_of_board(self):
        """
        size_of_board getter
        """

        return self.__size_of_board
        
    @property
    def DIMACS_format(self):
        """
        DIMACS_format getter
        """

        return self.__DIMACS_format.getvalue()
    
    @property
    def map_board_to_propositional_variable(self):
        """
        map_board_to_propositional_variable getter
        """

        return copy.deepcopy(self.__map_board_to_propositional_variable)

    @property
    def map_propositional_variable_to_board(self):
        """
        map_propositional_variable_to_board getter
        """

        return copy.deepcopy(self.__map_propositional_variable_to_board)

    @property
    def number_of_propositional_variables(self):
        """
        number_of_propositional_variables getter
        """

        return self.__number_of_propositional_variables

    @property
    def number_of_clauses(self):
        """
        number_of_clauses getter
        """

        return self.__number_of_clauses
