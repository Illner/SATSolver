import copy
import random

class DPLL:
    # Constructor
    def __init__(self, cnf):
        """
        List<List<int>> cnf
        Dictionary<string, boolean> model
        int number_of_decisions
        int number_of_steps_of_unit_propagation
        """

        self.__cnf = cnf
        self.__model = {}
        self.__number_of_decisions = 0
        self.__number_of_steps_of_unit_propagation = 0

    # Method
    def DPLL(self):
        """
        Returns a model of CNF
        If CNF is unsatisfiable returns None
        """

        # DPLL was already executed
        if (self.__model != {}):
            return self.__model

        assignment = self.__DPLL_recursive([])

        # CNF is unsatisfiable
        if (assignment == None):
            self.__model = None
            return None

        assignment.sort(key=abs) 

        for l in assignment:
            variable_name = self.__cnf.original_variable_name(l)
            if (variable_name is None):
                variable_name = str(abs(l))
            else:
                variable_name += " (" + str(l) + ")"

            self.__model[variable_name] = (l > 0)

        return self.__model

    def __DPLL_recursive(self, partial_assignment):
        partial_assignment_copy = copy.deepcopy(partial_assignment)

        # Unit propagation
        is_unsatisfied = self.__cnf.unit_propagation_adjacency_list(partial_assignment_copy)
        self.__increment_number_of_steps_of_unit_propagation(len(partial_assignment_copy) - len(partial_assignment))

        if (is_unsatisfied):
            return None

        undefined_variables_list = self.__cnf.undefined_variables(partial_assignment_copy)

        # CNF is satisfied
        if (not undefined_variables_list):
            return partial_assignment_copy

        variable = random.choice(undefined_variables_list)

        # +variable
        partial_assignment_copy.append(variable)
        self.__increment_number_of_decisions()
        result = self.__DPLL_recursive(partial_assignment_copy)
        if (result is not None):
            return result

        partial_assignment_copy.remove(variable)

        # -variable
        partial_assignment_copy.append(-variable)
        self.__increment_number_of_decisions()
        result = self.__DPLL_recursive(partial_assignment_copy)
        if (result is not None):
            return result

        return None

    def __increment_number_of_decisions(self):
        self.__number_of_decisions += 1

    def __increment_number_of_steps_of_unit_propagation(self, number):
        self.__number_of_steps_of_unit_propagation += number

    # Property
    @property
    def number_of_decisions(self):
        """
        number_of_decision getter
        """

        return self.__number_of_decisions

    @property
    def number_of_steps_of_unit_propagation(self):
        """
        number_of_steps_of_unit_propagation getter
        """

        return self.__number_of_steps_of_unit_propagation