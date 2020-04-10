import copy
import MyException
from UnitPropagationEnum import UnitPropagationEnum

class CNF:
    """
    CNF formula representation
    """

    # Constructor
    def __init__(self, DIMACS_format, original_variable_dictionary = {}, unit_propagation_enum = UnitPropagationEnum.AdjacencyList):
        """
        List<List<int>> cnf
        int number_of_clauses
        int number_of_variables
        int number_of_checked_clauses
        int actual_level
        List<int> literal_list
        List<int> variable_list
        List<Tuple<int, int>> partial_assignment_list
        HashSet<int> partial_assignment_only_literals_hashset
        List<int> unit_clause_list
        List<int> contradiction_clause_list
        List<int> counter_list
        List<Tuple<int, int>> clause_watched_literals_list
        Dictionary<int, Tuple<HashSet<int>, HashSet<int>>> variable_watched_literals_dictionary
        UnitPropagationEnum unit_propagation_enum
        Dictionary<int, string> original_variable_dictionary
        Dictionary<int, List<int>> adjacency_list_dictionary
        List<Tuple<int, int>> watched_literals_list
        HashSet<int> undefined_literals_hashset
        """

        self.__cnf = []
        self.__actual_level = 0
        self.__number_of_clauses = 0
        self.__number_of_variables = 0
        self.__number_of_checked_clauses = 0
        self.__partial_assignment_list = []
        self.__unit_propagation_enum = unit_propagation_enum
        self.__partial_assignment_only_literals_hashset = set()
        self.__original_variable_dictionary = copy.deepcopy(original_variable_dictionary)

        if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
            self.__counter_list = []
            self.__adjacency_list_dictionary = {}
            self.__unit_clause_list = []
            self.__contradiction_clause_list = []

        if (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
            self.__clause_watched_literals_list = []
            self.__variable_watched_literals_dictionary = {}

        self.__create_cnf(DIMACS_format)

        self.__variable_list = list(range(1, self.__number_of_variables + 1))
        self.__literal_list = list(range(-self.__number_of_variables, self.__number_of_variables + 1))
        self.__literal_list.remove(0)
        self.__undefined_literals_hashset = set(self.__literal_list)

        # Complete the variable watched literals list
        if (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
            for variable in self.__variable_list:
                if (variable not in self.__variable_watched_literals_dictionary):
                    self.__variable_watched_literals_dictionary[variable] = (set(), set())

    # Method
    def __create_cnf(self, DIMACS_format):
        clause_id = 0
        for line in DIMACS_format.splitlines():
            # Comment line
            if (line.startswith("c")):
                continue

            # End of file (optional)
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

                        # (x v x) => (x)
                        if (x in clause):
                            continue

                        clause.append(x)

                        # Set adjacency list
                        if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
                            self.__update_adjacency_list(x, clause_id)
                except ValueError:
                    raise MyException.InvalidDIMACSFormatException("Invalid clause line")

                self.__cnf.append(clause)

                # Set counter
                if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
                    self.__counter_list.append(len(clause))
                    # Unit clause
                    if (len(clause) == 1):
                        self.__unit_clause_list.append(clause_id)

                # Set watched literals list
                if (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
                    # Unit clause
                    if (len(clause) == 1):
                        self.__clause_watched_literals_list.append((clause[0], None))
                        self.__update_watched_list(clause[0], clause_id)
                    else:
                        self.__clause_watched_literals_list.append((clause[0], clause[1]))
                        self.__update_watched_list(clause[0], clause_id)
                        self.__update_watched_list(clause[1], clause_id)

                clause_id += 1
           
    def __update_adjacency_list(self, literal, clause_id):
        variable = abs(literal)

        # Variable exists in the adjacency list
        if (variable in self.__adjacency_list_dictionary):
            if (not(clause_id in self.__adjacency_list_dictionary[variable])):
                self.__adjacency_list_dictionary[variable].append(clause_id)

        # Variable does not exist in the adjacency list
        else:
            self.__adjacency_list_dictionary[variable] = [clause_id]

    def __update_watched_list(self, literal, clause_id):
        variable = abs(literal)

        # Variable does not exist in the watched literals list
        if (variable not in self.__variable_watched_literals_dictionary):
            self.__variable_watched_literals_dictionary[variable] = (set(), set())

        # Positive literal
        if (literal > 0):
            self.__variable_watched_literals_dictionary[variable][0].add(clause_id)
        # Negative literal
        else:
            self.__variable_watched_literals_dictionary[variable][1].add(clause_id)

    def level_in_partial_assignment_for_literal(self, literal):
        """
        Return level for the literal, if the literal is not in the partial assignment returns None
        """

        for (x, l) in self.__partial_assignment_list:
            if (x == literal):
                return l

        return None

    def __check_partial_assignment(self):
        """
        Returns True if the partial assignment is valid otherwise False
        """

        # Check if all literals in the partial assignment exist in the formula
        if(not(all(x in self.__literal_list for (x, _) in self.__partial_assignment_list))):
            return False

        # Check if the partial assignment does not contain a contradiction
        if(not(all(-x not in self.__partial_assignment_only_literals_hashset for (x, _) in self.__partial_assignment_list))):
            return False

        return True

    def undefined_variables(self, check_partial_assignment = False):
        """
        Returns a list of variables which are undefined in the partial assignment
        """

        if (check_partial_assignment and not(self.__check_partial_assignment())):
            raise MyException.InvalidLiteralInPartialAssignmentCnfException(str(self.__partial_assignment_list))

        return list(filter(lambda x: (x not in self.__partial_assignment_only_literals_hashset) and (-x not in self.__partial_assignment_only_literals_hashset), self.__variable_list))

    def unit_propagation(self):
        if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
            return self.__unit_propagation_adjacency_list()
        elif (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
            return self.__unit_propagation_watched_literals()
        else:
            raise MyException.UndefinedUnitPropagationCnfException(str(self.__unit_propagation_enum))

    def __unit_propagation_adjacency_list(self):
        while (self.__unit_clause_list):
            clause_id = self.__unit_clause_list.pop()

            self.__increment_number_of_checked_clauses()
            undefined_literal_list = self.__undefined_literal_list_for_clause(clause_id)

            l = undefined_literal_list.pop()
            self.add_literal_to_partial_assignment(l)

            if (len(self.__contradiction_clause_list) != 0):
                return True
        
        # return (len(self.__contradiction_clause_list) != 0)
        return False

    def __unit_propagation_watched_literals(self):
        end = False
        unit_clause_literal_list = []
        # contradiction_clause_list = []

        while (not end):
            end = True
            for (clause_id, (w_l_1, w_l_2)) in enumerate(self.__clause_watched_literals_list):
                is_w_l_1_defined = w_l_1 not in self.__undefined_literals_hashset
                is_w_l_2_defined = w_l_2 not in self.__undefined_literals_hashset

                # Both watched literals are undefined
                if ((not is_w_l_1_defined) and (not is_w_l_2_defined)):
                    continue

                is_w_l_1_satisfied = w_l_1 in self.__partial_assignment_only_literals_hashset
                is_w_l_2_satisfied = w_l_2 in self.__partial_assignment_only_literals_hashset

                # At least one watched literal is satisfied
                if (is_w_l_1_satisfied or is_w_l_2_satisfied):
                    continue

                # Clause contains only one literal which is not satisfied
                if (((w_l_1 is None) and (is_w_l_2_defined)) or ((w_l_2 is None) and (is_w_l_1_defined))):
                    # contradiction_clause_list.append(clause_id)
                    return True

                # Contradiction
                if (is_w_l_1_defined and is_w_l_2_defined):
                    # contradiction_clause_list.append(clause_id)
                    return True

                # First watched literal is undefined, the second one is unsatisfied
                if (not is_w_l_1_defined):
                    unit_clause_literal_list.append(w_l_1)
                    continue

                # Second watched literal is undefined, the first one is unsatisfied
                if (not is_w_l_2_defined):
                    unit_clause_literal_list.append(w_l_2)
                    continue
                
            # Get rid of redundancy
            unit_clause_literal_list = list(set(unit_clause_literal_list))

            # Unit clauses cause a contradiction
            if (not all(-x not in unit_clause_literal_list for x in unit_clause_literal_list)):
                return True

            while (unit_clause_literal_list):
                end = False
                x = unit_clause_literal_list.pop()
                self.add_literal_to_partial_assignment(x)
                
        # return (len(contradiction_clause_list) != 0)
        return False

    def add_literal_to_partial_assignment(self, literal, check_partial_assignment = False):
        self.__partial_assignment_list.append([literal, self.__actual_level])
        self.__partial_assignment_only_literals_hashset.add(literal)

        self.__undefined_literals_hashset.remove(literal)
        self.__undefined_literals_hashset.remove(-literal)

        # Check if the partial assignment is valid
        if (check_partial_assignment and not(self.__check_partial_assignment())):
            raise MyException.InvalidLiteralInPartialAssignmentCnfException(str(self.__partial_assignment_list))

        if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
            self.__update_counter(literal)
        elif (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
            self.__update_watched_literals(literal)
        else:
            raise MyException.UndefinedUnitPropagationCnfException(str(self.__unit_propagation_enum))

    def remove_literal_from_partial_assignment(self, literal):
        # Check if the literal exists in the partial assignment
        if (literal not in self.__partial_assignment_only_literals_hashset):
            raise MyException.InvalidLiteralInPartialAssignmentCnfException("Literal '{0}' is not in the partial assignment: '{1}'".format(literal, self.__partial_assignment_list))

        level = self.level_in_partial_assignment_for_literal(literal)

        self.__partial_assignment_list.remove([literal, level])
        self.__partial_assignment_only_literals_hashset.remove(literal)

        self.__undefined_literals_hashset.add(literal)
        self.__undefined_literals_hashset.add(-literal)

        if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
            self.__update_counter(literal)
        elif (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
            pass;
        else:
            raise MyException.UndefinedUnitPropagationCnfException(str(self.__unit_propagation_enum))

    def __update_counter(self, literal):
        for clause_id in self.__adjacency_list_dictionary[abs(literal)]:
            if (clause_id in self.__contradiction_clause_list):
                self.__contradiction_clause_list.remove(clause_id)

            if (clause_id in self.__unit_clause_list):
                self.__unit_clause_list.remove(clause_id)
                
            self.__increment_number_of_checked_clauses()
            is_satisfied = self.__is_clause_satisfied(clause_id)

            # Clause is satisfied
            if (is_satisfied):
                self.__counter_list[clause_id] = 0
            else:
                undefined_literal_list = self.__undefined_literal_list_for_clause(clause_id)
                # Clause is unsatisfied
                if (len(undefined_literal_list) == 0):
                    self.__counter_list[clause_id] = 0
                    self.__contradiction_clause_list.append(clause_id)
                # Unit clause
                elif (len(undefined_literal_list) == 1):
                    self.__counter_list[clause_id] = 1
                    self.__unit_clause_list.append(clause_id)
                else:
                    self.__counter_list[clause_id] = len(undefined_literal_list)

    def __update_watched_literals(self, literal):
        variable = abs(literal)
        clauses_to_delete_list = []

        for clause_id in self.__variable_watched_literals_dictionary[variable][int (literal > 0)]:
            w_l_1 = -literal
            w_l_2 = self.__clause_watched_literals_list[clause_id][0] if (self.__clause_watched_literals_list[clause_id][0] != w_l_1) else self.__clause_watched_literals_list[clause_id][1]
            
            self.__increment_number_of_checked_clauses()
            valid_value_for_w_l_1_iterator = filter(lambda x: (-x not in self.__partial_assignment_only_literals_hashset) and (x != w_l_2), self.__cnf[clause_id])

            w_l_1 = next(valid_value_for_w_l_1_iterator, None)

            if (w_l_1 is not None):
                clauses_to_delete_list.append(clause_id)
                self.__variable_watched_literals_dictionary[abs(w_l_1)][int (-w_l_1 > 0)].add(clause_id)
                self.__clause_watched_literals_list[clause_id] = (w_l_1, w_l_2)

        for clause_id in clauses_to_delete_list:
            self.__variable_watched_literals_dictionary[variable][int (literal > 0)].remove(clause_id)

    def __is_clause_satisfied(self, clause_id):
        clause = self.__cnf[clause_id]
        return any(x in self.__partial_assignment_only_literals_hashset for x in clause)
    
    def __undefined_literal_list_for_clause(self, clause_id):
        clause = self.__cnf[clause_id]
        return (list(filter(lambda x: (x not in self.__partial_assignment_only_literals_hashset) and (-x not in self.__partial_assignment_only_literals_hashset), clause)))

    def original_variable_name(self, variable):
        """
        Returns an original name of variable
        If variable does not have an original name, returns None
        """

        variable = abs(variable)

        if (variable in self.__original_variable_dictionary):
            return self.__original_variable_dictionary[variable]

        return None

    def verify(self, assignment):
        if (assignment is None):
            return True

        return (all(any(x in assignment for x in clause) for clause in self.__cnf))

    def __increment_number_of_checked_clauses(self, number = 1):
        self.__number_of_checked_clauses += number

    def increment_actual_level(self):
        self.__actual_level += 1

    def decrement_actual_level(self):
        self.__actual_level -= 1

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
        partial_assignment_only_literals_hashset getter
        """

        return list(self.__partial_assignment_only_literals_hashset)

    @property
    def partial_assignment_with_levels(self):
        """
        partial_assignment getter
        """

        return self.__partial_assignment_list

    @property
    def number_of_checked_clauses(self):
        """
        number_of_checked_clauses getter
        """

        return self.__number_of_checked_clauses

    @property
    def actual_level(self):
        """
        actual_level getter
        """

        return self.__actual_level