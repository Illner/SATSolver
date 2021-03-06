import time
import copy
import random
import MyException

class CDCL:
    # Constructor
    def __init__(self, cnf, assumptions = []):
        """
        int time
        List<List<int>> cnf
        List<int> model2
        Dictionary<string, boolean> model
        List<int> assumptions
        int number_of_decisions
        int number_of_steps_of_unit_propagation
        """
        
        self.__time = None
        self.__cnf = cnf
        self.__model2 = []
        self.__model = {}
        self.__assumptions = assumptions
        self.__number_of_decisions = 0
        self.__number_of_steps_of_unit_propagation = 0

        if (self.__cnf.learned_clauses is None):
            raise MyException.LearnedClausesAreNeededCDCLException()

    # Method
    def CDCL(self):
        """
        Returns a model of CNF
        If CNF is unsatisfiable returns None
        """

        # CDCL was already executed
        if (self.__model != {}):
            return self.__model

        start = time.time()
        is_satisfiable = self.__CDCL()
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

    def __CDCL(self):
        # Assumptions
        if (self.__assumptions):
            self.__cnf.current_decision_level = -1

            for assumption in self.__assumptions:
                # Contradiction in assumptions
                if (-assumption in self.__cnf.partial_assignment):
                    return None

                # Duplication
                if (assumption in self.__cnf.partial_assignment):
                    continue

                # Literal is valid
                if (assumption in self.__cnf.literal_list):
                    self.__cnf.add_literal_to_partial_assignment(assumption)

            self.__cnf.current_decision_level = 0

        # Main loop
        while(True):
            number_of_assigned_literals_before_unit_propagation = len(self.__cnf.partial_assignment)

            # Unit propagation
            contradiction_clause = self.__cnf.unit_propagation()
            self.__increment_number_of_steps_of_unit_propagation(len(self.__cnf.partial_assignment) - number_of_assigned_literals_before_unit_propagation)

            # CNF is unsatisfied
            if (contradiction_clause is not None and self.__cnf.current_decision_level == 0):
                return False

            # Contradiction occurs
            if (contradiction_clause is not None):
                level = self.__cnf.conflict_analysis(contradiction_clause)
                self.__cnf.backtrack_to_decision_level(level)
                self.__cnf.current_decision_level = level
                continue

            # CNF is satisfied
            if (not self.__cnf.exists_undefined_variable()):
                return True

            variable = self.__cnf.decision_literal()

            self.__cnf.increment_current_decision_level()
            self.__cnf.add_literal_to_partial_assignment(variable)
            self.__increment_number_of_decisions()

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

    @property
    def assumptions(self):
        """
        assumptions getter
        """

        return self.__assumptions