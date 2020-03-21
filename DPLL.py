import time
import copy
import random

class DPLL:
    # Constructor
    def __init__(self, cnf):
        """
        int time
        List<List<int>> cnf
        List<int> model2
        Dictionary<string, boolean> model
        int number_of_decisions
        int number_of_steps_of_unit_propagation
        """
        
        self.__time = None
        self.__cnf = cnf
        self.__model2 = []
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

        start = time.time()
        is_satisfiable = self.__DPLL_recursive()
        end = time.time()

        self.__time = (end - start)

        # CNF is unsatisfiable
        if (not is_satisfiable):
            self.__model = None
            return None

        assignment = copy.deepcopy(self.__cnf.partial_assignment)
        assignment.sort(key=abs) 
        self.__model2 = copy.deepcopy(assignment)

        for l in assignment:
            variable_name = self.__cnf.original_variable_name(l)
            if (variable_name is None):
                variable_name = str(abs(l))
            else:
                variable_name += " (" + str(abs(l)) + ")"

            self.__model[variable_name] = (l > 0)

        return self.__model2

    def __DPLL_recursive(self):
        before_partial_assignment = copy.deepcopy(self.__cnf.partial_assignment)

        # Unit propagation
        is_unsatisfied = self.__cnf.unit_propagation_adjacency_list()
        
        after_partial_assignment = self.__cnf.partial_assignment
        self.__increment_number_of_steps_of_unit_propagation(len(after_partial_assignment) - len(before_partial_assignment))

        remove_literal_list = list(filter(lambda x: x not in before_partial_assignment, after_partial_assignment))

        if (is_unsatisfied):
            for l in remove_literal_list:
                self.__cnf.remove_literal_from_partial_assignment(l)

            return False

        undefined_variables_list = self.__cnf.undefined_variables()

        # CNF is satisfied
        if (not undefined_variables_list):
            return True

        variable = random.choice(undefined_variables_list)

        # +variable
        self.__cnf.add_literal_to_partial_assignment(variable)
        self.__increment_number_of_decisions()
        result = self.__DPLL_recursive()
        if (result):
            return True

        self.__cnf.remove_literal_from_partial_assignment(variable)

        # -variable
        self.__cnf.add_literal_to_partial_assignment(-variable)
        self.__increment_number_of_decisions()
        result = self.__DPLL_recursive()
        if (result):
            return True
        
        self.__cnf.remove_literal_from_partial_assignment(-variable)

        for l in remove_literal_list:
            self.__cnf.remove_literal_from_partial_assignment(l)

        return False

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

    @property
    def time(self):
        """
        time getter
        """

        return self.__time