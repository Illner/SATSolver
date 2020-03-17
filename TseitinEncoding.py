import MyException
from DerivationTree import DerivationTree
from LogicalSignEnum import LogicalSignEnum

class TseitinEncoding:
    """
    Convert generic formula (represented by derivation tree) to CNF formula using Tseitin encoding
    """

    # Constructor
    def __init__(self, derivation_tree, one_sided = False):
        """
        NodeTree root
        boolean one_sided
        Dictionary<int, (int, string)> variable_dictionary
        Dictionary<int, string> original_variable_dictionary
        int number_of_clauses
        string DIMACS_format
        int id
        """

        self.__root = derivation_tree.root
        self.__one_sided = one_sided
        self.__variable_dictionary = {}
        self.__original_variable_dictionary = {}
        self.__number_of_clauses = 0
        self.__DIMACS_format = ""
        self.__id = 0

        l = self.__get_fresh_variable_of_node(self.root)
        DIMACS_format = "{0} 0\n".format(l)
        self.__increment_number_of_clauses(1)

        DIMACS_format += self.__convert_to_DIMACS_format(self.root)

        original_variable = "c original variables: "
        fresh_variable = "c fresh variables: "
        for key in self.__variable_dictionary:
            (value_1, value_2) = self.__variable_dictionary[key]
            # Fresh variable
            if (value_2 == ""):
                fresh_variable += str(value_1) + " "
            # Original variable
            else:
                original_variable += value_2 + "-" + str(value_1) + " "
                self.__original_variable_dictionary[value_1] = value_2

        self.__DIMACS_format = "c root: {0}".format(l) + "\n"
        self.__DIMACS_format += original_variable + "\n"
        self.__DIMACS_format += fresh_variable + "\n"
        self.__DIMACS_format += "p cnf {0} {1}".format(self.number_of_variables(), self.number_of_clauses) + "\n"
        self.__DIMACS_format += DIMACS_format

    # Method
    def __convert_to_DIMACS_format(self, node):
        # base case
        if (node.is_leaf()):
            return ""

        DIMACS_format = ""

        # AND operator
        if (node.value == LogicalSignEnum.AND.name):
            l = self.__get_fresh_variable_of_node(node)
            l_1 = self.__get_fresh_variable_of_node(node.left_node)
            l_2 = self.__get_fresh_variable_of_node(node.right_node)

            if (not(self.one_sided)):
                DIMACS_format += "-{0} {1} 0\n-{0} {2} 0\n-{1} -{2} {0} 0\n".format(l, l_1, l_2)
                self.__increment_number_of_clauses(3)
            else:
                DIMACS_format += "-{0} {1} 0\n-{0} {2} 0\n".format(l, l_1, l_2)
                self.__increment_number_of_clauses(2)
        # OR operator
        elif (node.value == LogicalSignEnum.OR.name):
            l = self.__get_fresh_variable_of_node(node)
            l_1 = self.__get_fresh_variable_of_node(node.left_node)
            l_2 = self.__get_fresh_variable_of_node(node.right_node)

            if (not(self.one_sided)):
                DIMACS_format += "-{0} {1} {2} 0\n-{1} {0} 0\n-{2} {0} 0\n".format(l, l_1, l_2)
                self.__increment_number_of_clauses(3)
            else:
                DIMACS_format += "-{0} {1} {2} 0\n".format(l, l_1, l_2)
                self.__increment_number_of_clauses(1)
        # NOT operator
        elif (node.value == LogicalSignEnum.NOT.name):
            l = self.__get_fresh_variable_of_node(node)
            l_1 = self.__get_fresh_variable_of_node(node.left_node)

            if (not(self.one_sided)):
                DIMACS_format += "-{0} -{1} 0\n{1} {0} 0\n".format(l, l_1)
                self.__increment_number_of_clauses(2)
            else:
                DIMACS_format += "-{0} -{1} 0\n".format(l, l_1)
                self.__increment_number_of_clauses(1)
        # Invalid operator
        else:
            raise MyException.InvalidOperatorTseitinEncodingException(node.value)

        if (node.has_left_node):
            DIMACS_format += self.__convert_to_DIMACS_format(node.left_node)

        if (node.has_right_node):
            DIMACS_format += self.__convert_to_DIMACS_format(node.right_node)

        return DIMACS_format

    def __get_fresh_variable_of_node(self, node):
        """
        Returns a value (only id - first item in tuple) of the dictionary for the node
        """

        # We have already visited the node and created fresh variable
        if (node.id in self.__variable_dictionary):
            return  self.__variable_dictionary[node.id][0]

        l = 0

        # Node contains an operator
        if (node.value in LogicalSignEnum._member_names_):
            l = self.__get_id()
            self.__variable_dictionary[node.id] = (l, "")
        # Node contains an operand
        else:
            l = self.__get_id()
            self.__variable_dictionary[node.id] = (l, node.value)

        return l

    def __increment_number_of_clauses(self, number = 1):
        self.__number_of_clauses += number

    def __get_id(self):
        self.__id += 1
        return self.__id

    def number_of_variables(self):
        return len(self.__variable_dictionary)

    def __str__(self):
        return self.__DIMACS_format

    # Property
    @property
    def one_sided(self):
        """
        one_sided getter
        """

        return self.__one_sided

    @property
    def root(self):
        """
        root getter
        """

        return self.__root

    @property
    def number_of_clauses(self):
        """
        number_of_clauses getter
        """

        return self.__number_of_clauses

    @property
    def original_variable_dictionary(self):
        """
        original_variable_dictionary getter
        """

        return self.__original_variable_dictionary