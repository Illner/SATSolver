
import copy
import MyException

class CNF:
    """
    CNF formula representation
    """

    # Constructor
    def __init__(self, DIMACS_format, original_variable_dictionary = {}):
        """
        List<List<int>> cnf
        int number_of_clauses
        int number_of_variables
        List<int> literal_list
        List<int> variable_list
        List<int> partial_assignment_list
        List<int> unit_clause_list
        Dictionary<int, int> counter_dictionary
        List<int> contradiction_clause_list
        Dictionary<int, string> original_variable_dictionary
        Dictionary<int, List<int>> adjacency_list_dictionary
        """

        self.__cnf = []
        self.__number_of_clauses = 0
        self.__number_of_variables = 0
        self.__partial_assignment = []
        self.__unit_clause_list = []
        self.__counter_dictionary = {}
        self.__contradiction_clause_list = []
        self.__adjacency_list_dictionary = {}
        self.__original_variable_dictionary = copy.deepcopy(original_variable_dictionary)

        self.__create_cnf(DIMACS_format)

        self.__variable_list = list(range(1, self.__number_of_variables + 1))
        self.__literal_list = list(range(-self.__number_of_variables, self.__number_of_variables + 1))
        self.__literal_list.remove(0)

    # Method
    def __create_cnf(self, DIMACS_format):
        clause_id = 0
        for line in DIMACS_format.splitlines():
            # Comment line
            if (line.startswith("c")):
                continue

            # ?? end of file ??
            if (line.startswith("%")):
                break;

            # P line
            elif (line.startswith("p")):
                temp_array = line.split()
                if (len(temp_array) != 4):
                    raise MyException.InvalidDIMACSFormatException("Invalid p line")

                try:
                    self.__number_of_variables = int(temp_array[2])
                    self.__number_of_clauses = int(temp_array[3])
                except ValueError:
                    raise MyException.InvalidDIMACSFormatException("Invalid number of clauses or number of variables")

            # Clause line
            else:
                temp_array = line.split()
                if (temp_array[-1] != "0"):
                    raise MyException.InvalidDIMACSFormatException("Clause is not ending with 0")
                
                temp_array.pop()
                clause = []
                try:
                    for x in temp_array:
                        x = int(x)
                        clause.append(x)

                        # Set adjacency list
                        self.__update_adjacency_list(x, clause_id)
                except ValueError:
                    raise MyException.InvalidDIMACSFormatException("Invalid clause line")

                self.__cnf.append(clause)
                clause_id += 1

                # Set counter
                self.__counter_dictionary[clause_id] = len(clause)
                if (len(clause) == 1):
                    self.__unit_clause_list.append(clause_id)
    
    def __update_adjacency_list(self, variable, clause_id):
        variable = abs(variable)

        # Variable exists in the adjacency list
        if (variable in self.__adjacency_list_dictionary):
            if (not(clause_id in self.__adjacency_list_dictionary[variable])):
                self.__adjacency_list_dictionary[variable].append(clause_id)

        # Variable does not exist in the adjacency list
        else:
            self.__adjacency_list_dictionary[variable] = [clause_id]

    def __check_partial_assignment(self):
        """
        Returns True if the partial assignment is valid otherwise False
        """

        # Check if all literals in the partial assignment exist in the formula
        if(not(all(x in self.__literal_list for x in self.__partial_assignment))):
            return False

        # Check if the partial assignment does not contain a contradiction
        if(not(all(-x not in self.__partial_assignment for x in self.__partial_assignment))):
            return False

        return True

    def undefined_variables(self):
        """
        Returns a list of variables which are undefinied in the partial assignment
        """
        if (not(self.__check_partial_assignment())):
            raise MyException.InvalidLiteralInPartialAssignmentCnfException(str(self.__partial_assignment))

        return list(filter(lambda x: (x not in self.__partial_assignment) and (-x not in self.__partial_assignment), self.__variable_list))

    def unit_propagation_adjacency_list(self):
        """
        Do unit propagation
        Uses counter-model adjacency list
        """

        while (self.__unit_clause_list):
            clause_id = self.__unit_clause_list.pop()
            clause = self.__cnf[clause_id]
            undefinied_literal_list = self.__undefinied_literal_list_for_clause(clause_id)

            l = undefinied_literal_list.pop()
            self.add_literal_to_partial_assignment(l)

        return (len(self.__contradiction_clause_list) != 0)

    def add_literal_to_partial_assignment(self, literal):
        self.__partial_assignment.append(literal)

        if (not(self.__check_partial_assignment())):
            raise MyException.InvalidLiteralInPartialAssignmentCnfException(str(self.__partial_assignment))

        self.__update_counter(literal)

    def remove_literal_from_partial_assignment(self, literal):
        # Check if the literal exists in the partial assignment
        if (literal not in self.__partial_assignment):
            raise MyException.InvalidLiteralInPartialAssignmentCnfException("Literal '{0}' is not in '{1}'".format(literal, self.__partial_assignment))

        self.__partial_assignment.remove(literal)

        self.__update_counter(literal)

    def __update_counter(self, literal):
        for clause_id in self.__adjacency_list_dictionary[abs(literal)]:
            if (clause_id in self.__contradiction_clause_list):
                self.__contradiction_clause_list.remove(clause_id)

            if (clause_id in self.__unit_clause_list):
                self.__unit_clause_list.remove(clause_id)

            is_satisfied = self.__is_clause_satisfied(clause_id)

            # Clause is satisfied
            if (is_satisfied):
                self.__counter_dictionary[clause_id] = 0
            else:
                undefinied_literal_list = self.__undefinied_literal_list_for_clause(clause_id)
                # Clause is unsatisfied
                if (len(undefinied_literal_list) == 0):
                    self.__counter_dictionary[clause_id] = 0
                    self.__contradiction_clause_list.append(clause_id)
                # Unit clause
                elif (len(undefinied_literal_list) == 1):
                    self.__counter_dictionary[clause_id] = 1
                    self.__unit_clause_list.append(clause_id)
                else:
                    self.__counter_dictionary[clause_id] = len(undefinied_literal_list)

    def __is_clause_satisfied(self, clause_id):
        clause = self.__cnf[clause_id]
        return any(x in self.__partial_assignment for x in clause)
    
    def __undefinied_literal_list_for_clause(self, clause_id):
        clause = self.__cnf[clause_id]
        return list(filter(lambda x: (x not in self.__partial_assignment) and (-x not in self.__partial_assignment), clause))

    def original_variable_name(self, variable):
        """
        Returns an original name of variable
        If variable does not have an original name, returns None
        """

        variable = abs(variable)

        if (variable in self.__original_variable_dictionary):
            return self.__original_variable_dictionary[variable]

        return None

    # Property
    @property
    def cnf(self):
        """
        cnf getter
        """

        return self.__cnf

    @property
    def number_of_variables(self):
        """
        number_of_variables getter
        """

        return self.__number_of_variables

    @property
    def number_of_clauses(self):
        """
        number_of_clauses getter
        """

        return self.__number_of_clauses

    @property
    def variable_list(self):
        """
        variable_list getter
        """

        return self.__variable_list

    @property
    def literal_list(self):
        """
        literal_list getter
        """

        return self.__literal_list

    @property
    def partial_assignment(self):
        """
        partial_assignment getter
        """

        return self.__partial_assignment