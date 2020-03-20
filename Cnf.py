import copy
import MyException

class Cnf:
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
        Dictionary<int, string> original_variable_dictionary
        Dictionary<int, List<int>> adjacency_list_dictionary
        """

        self.__cnf = []
        self.__number_of_clauses = 0
        self.__number_of_variables = 0
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
    
    def __update_adjacency_list(self, variable, clause_id):
        variable = abs(variable)

        # Variable exists in the adjacency list
        if (variable in self.__adjacency_list_dictionary):
            if (not(clause_id in self.__adjacency_list_dictionary[variable])):
                self.__adjacency_list_dictionary[variable].append(clause_id)

        # Variable does not exist in the adjacency list
        else:
            self.__adjacency_list_dictionary[variable] = [clause_id]

    def __check_partial_assignment(self, partial_assignment):
        """
        Returns True if the partial assignment is valid otherwise False
        """

        # Check if all literals in the partial assignment exist in the formula
        if(not(all(x in self.__literal_list for x in partial_assignment))):
            return False

        # Check if the partial assignment does not contain a contradiction
        if(not(all(-x not in partial_assignment for x in partial_assignment))):
            return False

        return True

    def undefined_variables(self, partial_assignment, check_partial_assignment = True):
        """
        Returns a list of variables which are undefinied in the partial assignment
        """
        if (check_partial_assignment and not(self.__check_partial_assignment(partial_assignment))):
            raise MyException.InvalidLiteralInPartialAssignmentCnfException(str(partial_assignment))

        return list(filter(lambda x: (x not in partial_assignment) and (-x not in partial_assignment), self.__variable_list))

    def unit_propagation_adjacency_list(self, partial_assignment, check_partial_assignment = True):
        if (check_partial_assignment and not(self.__check_partial_assignment(partial_assignment))):
            raise MyException.InvalidLiteralInPartialAssignmentCnfException(str(partial_assignment))

        # Variable
        unit_clause_list = []
        counter_dictionary = {}
        contradiction_clause_list = []

        # Initialize lists
        for (clause_id, clause) in enumerate(self.__cnf):
             is_satisfied = self.__is_clause_satisfied(clause_id, partial_assignment)

             # Clause is satisfied
             if (is_satisfied):
                 counter_dictionary[clause_id] = 0
             else:
                undefinied_literal_list = self.__undefinied_literal_list_for_clause(clause_id, partial_assignment)
                # Clause is unsatisfied
                if (len(undefinied_literal_list) == 0):
                    counter_dictionary[clause_id] = 0
                    contradiction_clause_list.append(clause_id)
                # Unit clause
                elif (len(undefinied_literal_list) == 1):
                    counter_dictionary[clause_id] = 1
                    unit_clause_list.append(clause_id)
                else:
                    counter_dictionary[clause_id] = len(undefinied_literal_list)

        while (unit_clause_list):
            clause_id = unit_clause_list.pop()
            clause = self.__cnf[clause_id]
            undefinied_literal_list = self.__undefinied_literal_list_for_clause(clause_id, partial_assignment)

            l = undefinied_literal_list.pop()
            partial_assignment.append(l)

            for i in self.__adjacency_list_dictionary[abs(l)]:
                temp_counter = counter_dictionary[i]

                # Clause is already satisfied or unsatisfied
                if (temp_counter == 0):
                    continue

                # Clause is now satisfied
                if (self.__is_clause_satisfied(i, partial_assignment)):
                    counter_dictionary[i] = 0
                    if (i in unit_clause_list):
                        unit_clause_list.remove(i)
                    continue

                # temp_counter -= 1
                temp_counter -= self.__cnf[i].count(-l)
                counter_dictionary[i] = temp_counter 

                # Clause is now unsatisfied
                if (temp_counter == 0):
                    contradiction_clause_list.append(i)
                    if (i in unit_clause_list):
                        unit_clause_list.remove(i)

                # Unit clause
                if (temp_counter == 1):
                    unit_clause_list.append(i)

        return (len(contradiction_clause_list) != 0)

    def __is_clause_satisfied(self, clause_id, partial_assignment):
        clause = self.__cnf[clause_id]
        return any(x in partial_assignment for x in clause)
    
    def __undefinied_literal_list_for_clause(self, clause_id, partial_assignment):
        clause = self.__cnf[clause_id]
        return list(filter(lambda x: (x not in partial_assignment) and (-x not in partial_assignment), clause))

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
    def original_variable_name(self, variable):
        """
        Returns an original name of variable
        If variable does not have an original name, returns None
        """

        variable = abs(variable)

        if (variable in self.__original_variable_dictionary):
            return self.__original_variable_dictionary[variable]

        return None