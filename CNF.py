import sys
import copy
import heapq
import random
import operator
import MyException
from itertools import chain
from ClauseLearningEnum import ClauseLearningEnum
from RestartStrategyEnum import RestartStrategyEnum
from UnitPropagationEnum import UnitPropagationEnum
from DecisionHeuristicEnum import DecisionHeuristicEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionHowHeuristicEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionWhenHeuristicEnum

class CNF:
    """
    CNF formula representation
    """

    # Constructor
    def __init__(self, DIMACS_format, original_variable_dictionary = {}, 
                 unit_propagation_enum = UnitPropagationEnum.AdjacencyList,
                 clause_learning_enum = ClauseLearningEnum.none,
                 decision_heuristic_enum = DecisionHeuristicEnum.Greedy,
                 decay_constant_VSIDS_decision_heuristic = 2, # Decision heuristic - VSIDS
                 decay_period_VSIDS_decision_heuristic = 255, # Decision heuristic - VSIDS
                 clause_deletion_how_heuristic_enum = ClauseDeletionHowHeuristicEnum.none,
                 bound_keep_short_clauses_heuristic = 2, # Clause deletion - keep short clauses heuristic
                 ratio_keep_active_clauses_heuristic = 0.5, # Clause deletion - keep active clauses heuristic
                 clause_deletion_when_heuristic_enum = ClauseDeletionWhenHeuristicEnum.none, 
                 first_term_geometric_cache_clause_deletion = 100, # Clause deletion - cache (geometric)
                 common_ratio_geometric_cache_clause_deletion = 1.5, # Clause deletion - cache (geometric)
                 restart_strategy_enum = RestartStrategyEnum.none,
                 first_term_geometric_restart_strategy = 100, # Restart - GeometricStrategy
                 common_ratio_geometric_restart_strategy = 1.5 # Restart - GeometricStrategy
                 ):
        """
        List<List<int>> cnf
        int number_of_clauses
        int number_of_variables
        int current_decision_level
        int number_of_checked_clauses
        boolean use_learned_clauses
        List<int> literal_list
        List<int> variable_list
        List<Tuple<int, int>> partial_assignment_list
        HashSet<int> partial_assignment_only_literals_hashset
        UnitPropagationEnum unit_propagation_enum
        DecisionHeuristicEnum decision_heuristic_enum
        ClauseDeletionHowHeuristicEnum clause_deletion_how_heuristic_enum
        ClauseDeletionWhenHeuristicEnum clause_deletion_when_heuristic_enum
        ClauseLearningEnum clause_learning_enum
        RestartStrategyEnum restart_strategy_enum
        Dictionary<int, string> original_variable_dictionary
        HashSet<int> undefined_literals_hashset
        Dictionary<int, int> variable_level_dictionary

        List<int> unit_clause_list
        List<int> contradiction_clause_list
        List<int> counter_list
        Dictionary<int, List<int>> adjacency_list_dictionary

        List<Tuple<int, int>> clause_watched_literals_list
        Dictionary<int, Tuple<HashSet<int>, HashSet<int>>> variable_watched_literals_dictionary

        List<List<int>> learned_clauses
        int number_of_learned_clauses
        Dictionary<int, Tuple<int, boolean>> antecedent_dictionary
        HashSet<int> active_learned_clause_hashset
        Dictionary<int, int> active_counter_learned_clause_dictionary

        int number_of_restarts
        int number_of_conflicts
        int max_number_of_conflicts
        int first_term_geometric_restart_strategy
        double common_ratio_geometric_restart_strategy
        int unit_luby_restart_strategy
        Iterator restart_strategy_iterator

        int number_of_clause_deletions
        int number_of_deleted_learned_clauses
        int bound_keep_short_clauses_heuristic
        int ratio_keep_active_clauses_heuristic

        int first_term_geometric_cache_clause_deletion
        int common_ratio_geometric_cache_clause_deletion
        Iterator clause_deletion_when_heuristic_iterator
        int max_size_of_cache

        List<int> unit_learned_clause_list
        List<int> contradiction_learned_clause_list
        List<int> counter_learned_clause_list
        Dictionary<int, HashSet<int>> adjacency_list_learned_clause_dictionary

        List<Tuple<int, int>> learned_clause_watched_literals_list
        Dictionary<int, Tuple<HashSet<int>, HashSet<int>>> variable_watched_literals_learned_clause_dictionary

        Dictionary<int, int> score_Jeroslow_Wang_dictionary
        Heap<Tuple<int, int>> score_Jeroslow_Wang_heap

        int number_of_decay
        int number_of_conflicts_VSIDS_decision_heuristic
        int decay_constant_VSIDS_decision_heuristic
        int decay_period_VSIDS_decision_heuristic
        Dictionary<int, int> score_VSIDS_dictionary
        Heap<Tuple<int, int>> score_VSIDS_heap
        """

        # CNF
        self.__cnf = []
        self.__number_of_clauses = 0
        self.__number_of_variables = 0
        self.__current_decision_level = 0
        self.__number_of_checked_clauses = 0
        self.__partial_assignment_list = []
        self.__variable_level_dictionary = {}
        self.__unit_propagation_enum = unit_propagation_enum
        self.__partial_assignment_only_literals_hashset = set()
        self.__decision_heuristic_enum = decision_heuristic_enum
        self.__original_variable_dictionary = copy.deepcopy(original_variable_dictionary)

        self.__number_of_contradictions = 0
        self.__number_of_unit_propagations = 0

        # Learned clauses
        self.__use_learned_clauses = False if (clause_learning_enum == ClauseLearningEnum.none) else True
        self.__clause_learning_enum = clause_learning_enum
        self.__restart_strategy_enum = restart_strategy_enum
        self.__clause_deletion_how_heuristic_enum = clause_deletion_how_heuristic_enum
        self.__clause_deletion_when_heuristic_enum = clause_deletion_when_heuristic_enum
        self.__number_of_contradictions_caused_by_learned_clauses = 0
        self.__number_of_unit_propagations_caused_by_learned_clauses = 0
        if (self.__use_learned_clauses):
            self.__learned_clauses = []
            self.__number_of_learned_clauses = 0
            self.__antecedent_dictionary = {}
            self.__active_learned_clause_hashset = set()
            # Keep active
            if (self.__is_keep_active_clauses_heuristic()):
                self.__active_counter_learned_clause_dictionary = {}

            # Restart
            if (self.__has_restart()):
                self.__number_of_restarts = 0
                self.__number_of_conflicts = 0

                # Geometric strategy
                if (self.__restart_strategy_enum == RestartStrategyEnum.GeometricStrategy):
                    # first_term_geometric_restart_strategy is not a number
                    if (not isinstance(first_term_geometric_restart_strategy, int)):
                        raise MyException.InvalidParametersCnfException("first_term_geometric_restart_strategy ({0}) is not a number".format(first_term_geometric_restart_strategy))
                    # first_term_geometric_restart_strategy is invalid
                    if (first_term_geometric_restart_strategy < 0):
                        raise MyException.InvalidParametersCnfException("first_term_geometric_restart_strategy ({0}) is less than 0".format(first_term_geometric_restart_strategy))

                    self.__first_term_geometric_restart_strategy = first_term_geometric_restart_strategy

                    # common_ratio_geometric_restart_strategy is not a number
                    if (not isinstance(common_ratio_geometric_restart_strategy, float) and not isinstance(common_ratio_geometric_restart_strategy, int)):
                        raise MyException.InvalidParametersCnfException("common_ratio_geometric_restart_strategy ({0}) is not a number".format(common_ratio_geometric_restart_strategy))
                    # common_ratio_geometric_restart_strategy is invalid
                    if (common_ratio_geometric_restart_strategy <= 1):
                        raise MyException.InvalidParametersCnfException("common_ratio_geometric_restart_strategy ({0}) is not greater than 1".format(common_ratio_geometric_restart_strategy))

                    self.__common_ratio_geometric_restart_strategy = common_ratio_geometric_restart_strategy
                # Luby strategy
                if (self.__restart_strategy_enum == RestartStrategyEnum.LubyStrategy):
                    self.__unit_luby_restart_strategy = 100

                self.__restart_strategy_iterator = self.__get_restart_strategy_iterator()
                self.__max_number_of_conflicts = next(self.__restart_strategy_iterator)

            # Clause deletion (how)
            if (self.__clause_deletion_how_heuristic_enum != ClauseDeletionHowHeuristicEnum.none):
                self.__number_of_clause_deletions = 0
                self.__number_of_deleted_learned_clauses = 0
            # Keep short clauses
            if (self.__is_keep_short_clauses_heuristic()):
                # bound_keep_short_clauses_heuristic is not a number
                if (not isinstance(bound_keep_short_clauses_heuristic, int)):
                    raise MyException.InvalidParametersCnfException("bound_keep_short_clauses_heuristic ({0}) is not a number".format(bound_keep_short_clauses_heuristic))
                # bound_keep_short_clauses_heuristic is invalid
                if (bound_keep_short_clauses_heuristic < 0):
                    raise MyException.InvalidParametersCnfException("bound_keep_short_clauses_heuristic ({0}) is less than 0".format(bound_keep_short_clauses_heuristic))

                self.__bound_keep_short_clauses_heuristic = bound_keep_short_clauses_heuristic
            if (self.__is_keep_active_clauses_heuristic()):
                # ratio_keep_active_clauses_heuristic is not a number
                if (not isinstance(ratio_keep_active_clauses_heuristic, float) and not isinstance(ratio_keep_active_clauses_heuristic, int)):
                    raise MyException.InvalidParametersCnfException("ratio_keep_active_clauses_heuristic ({0}) is not a number".format(ratio_keep_active_clauses_heuristic))
                # ratio_keep_active_clauses_heuristic is invalid
                if (ratio_keep_active_clauses_heuristic < 0 or ratio_keep_active_clauses_heuristic > 1):
                    raise MyException.InvalidParametersCnfException("ratio_keep_active_clauses_heuristic ({0}) is not in <0; 1>".format(ratio_keep_active_clauses_heuristic))

                self.__ratio_keep_active_clauses_heuristic = ratio_keep_active_clauses_heuristic

            # Clause deletion (when) - cache
            if (self.__clause_deletion_when_heuristic_enum == ClauseDeletionWhenHeuristicEnum.CacheFull):
                # first_term_geometric_cache_clause_deletion is not a number
                if (not isinstance(first_term_geometric_cache_clause_deletion, int)):
                    raise MyException.InvalidParametersCnfException("first_term_geometric_cache_clause_deletion ({0}) is not a number".format(first_term_geometric_cache_clause_deletion))
                # first_term_geometric_cache_clause_deletion is invalid
                if (first_term_geometric_cache_clause_deletion < 0):
                    raise MyException.InvalidParametersCnfException("first_term_geometric_cache_clause_deletion ({0}) is less than 0".format(first_term_geometric_cache_clause_deletion))

                self.__first_term_geometric_cache_clause_deletion = first_term_geometric_cache_clause_deletion

                # common_ratio_geometric_cache_clause_deletion is not a number
                if (not isinstance(common_ratio_geometric_cache_clause_deletion, float) and not isinstance(common_ratio_geometric_cache_clause_deletion, int)):
                    raise MyException.InvalidParametersCnfException("common_ratio_geometric_cache_clause_deletion ({0}) is not a number".format(common_ratio_geometric_cache_clause_deletion))
                # common_ratio_geometric_cache_clause_deletion is invalid
                if (common_ratio_geometric_cache_clause_deletion <= 1):
                    raise MyException.InvalidParametersCnfException("common_ratio_geometric_cache_clause_deletion ({0}) is not greater than 1".format(common_ratio_geometric_cache_clause_deletion))

                self.__common_ratio_geometric_cache_clause_deletion = common_ratio_geometric_cache_clause_deletion
            # Clause deletion (when)
            if (self.__has_clause_deletion_when_heuristic()):
                self.__clause_deletion_when_iterator = self.__get_clause_deletion_when_iterator()
                self.__max_size_of_cache = next(self.__clause_deletion_when_iterator)

        # Check if parameters are valid
        if (not self.__use_learned_clauses and (not (self.__restart_strategy_enum == RestartStrategyEnum.none) or not (self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.none) or not (self.__clause_deletion_when_heuristic_enum == ClauseDeletionWhenHeuristicEnum.none))):
            raise MyException.InvalidParametersCnfException("use_learned_clauses is False but restartStrategyEnum, clauseDeletionHowHeuristicEnum or clauseDeletionWhenHeuristicEnum is not none")

        # Adjacency list
        if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
            # CNF
            self.__counter_list = []
            self.__adjacency_list_dictionary = {}
            self.__unit_clause_list = []
            self.__contradiction_clause_list = []

            # Learned clauses
            if (self.__use_learned_clauses):
                self.__counter_learned_clause_list = []
                self.__adjacency_list_learned_clause_dictionary = {}
                self.__unit_learned_clause_list = []
                self.__contradiction_learned_clause_list = []

        # Wacthed literals
        if (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
            # CNF
            self.__clause_watched_literals_list = []
            self.__variable_watched_literals_dictionary = {}

            # Learned clauses
            if (self.__use_learned_clauses):
                self.__learned_clause_watched_literals_list = []
                self.__variable_watched_literals_learned_clause_dictionary = {}

        self.__create_cnf(DIMACS_format)

        self.__variable_list = list(range(1, self.__number_of_variables + 1))
        self.__literal_list = list(range(-self.__number_of_variables, self.__number_of_variables + 1))
        self.__literal_list.remove(0)
        self.__undefined_literals_hashset = set(self.__literal_list)

        # Decision heuristic
        # Jeroslow-Wang
        if (self.__is_Jeroslow_Wang_decision_variable_heuristic()):
            self.__score_Jeroslow_Wang_dictionary = {}
            self.__score_Jeroslow_Wang_heap = None
            self.__initialize_Jeroslow_Wang_decision_variable_heuristic()
        # VSIDS
        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.VSIDS):
            self.__number_of_decay = 0
            self.__number_of_conflicts_VSIDS_decision_heuristic = 0
            self.__decay_constant_VSIDS_decision_heuristic = decay_constant_VSIDS_decision_heuristic
            self.__decay_period_VSIDS_decision_heuristic = decay_period_VSIDS_decision_heuristic
            self.__score_VSIDS_dictionary = {}
            self.__score_VSIDS_heap = None
            self.__initialize_VSIDS_decision_variable_heuristic()
        # eVSIDS
        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.eVSIDS):
            self.__decision_heuristic_enum = DecisionHeuristicEnum.VSIDS
            self.__number_of_decay = 0
            self.__number_of_conflicts_VSIDS_decision_heuristic = 0
            self.__decay_constant_VSIDS_decision_heuristic = 10/9
            self.__decay_period_VSIDS_decision_heuristic = 1
            self.__score_VSIDS_dictionary = {}
            self.__score_VSIDS_heap = None
            self.__initialize_VSIDS_decision_variable_heuristic()

        # Initialize adjacency_list_learned_clause_dictionary
        if (self.__use_learned_clauses and self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
            for variable in self.__variable_list:
                self.__adjacency_list_learned_clause_dictionary[variable] = set()

        # Initialize variable_watched_literals_learned_clause_dictionary
        # Complete the variable watched literals list
        if (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
            for variable in self.__variable_list:
                if (self.__use_learned_clauses):
                    self.__variable_watched_literals_learned_clause_dictionary[variable] = (set(), set())
                if (variable not in self.__variable_watched_literals_dictionary):
                    self.__variable_watched_literals_dictionary[variable] = (set(), set())

        # Initialize antecedent_dictionary
        if (self.__use_learned_clauses):
            for variable in self.__variable_list:
                self.__antecedent_dictionary[variable] = None

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

        if (abs(literal) in self.__variable_level_dictionary):
            return self.__variable_level_dictionary[abs(literal)]

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

    def undefined_variables_list(self, check_partial_assignment = False):
        """
        Returns a list of variables which are undefined in the partial assignment
        """

        if (check_partial_assignment and not(self.__check_partial_assignment())):
            raise MyException.InvalidLiteralInPartialAssignmentCnfException(str(self.__partial_assignment_list))
        
        return list(filter(lambda x: (x not in self.__partial_assignment_only_literals_hashset) and (-x not in self.__partial_assignment_only_literals_hashset), self.__variable_list))
        
    def first_undefined_variable(self):
        """
        If undefined variable does not exist returns None
        """

        if (not self.exists_undefined_variable()):
            return None

        for x in self.__undefined_literals_hashset:
            # Positive literal => variable
            if (x > 0):
                return x

    def exists_undefined_variable(self):
        if (self.__undefined_literals_hashset):
            return True

        return False

    def unit_propagation(self):
        """
        1) Learned clauses are not supported
            Return true if a contradiction occurs, otherwise false
        2) Learned clauses are supported
            If a contradiction occurs, return a clause which causes the contradiction, otherwise return None
        """

        temp_contradiction = None

        if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
            temp_contradiction = self.__unit_propagation_adjacency_list()
        elif (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
            temp_contradiction = self.__unit_propagation_watched_literals()
        else:
            raise MyException.UndefinedUnitPropagationCnfException(str(self.__unit_propagation_enum))

        # Learned clauses are not supported
        if (not self.__use_learned_clauses):
            # No contradiction
            if (temp_contradiction is None):
                return False
            # Contradiction
            else:
                self.__number_of_contradictions += 1
                return True

        # Learned clauses are supported
        return temp_contradiction

    def conflict_analysis(self, contradiction_clause):
        """
        Return new decision level (assertive level)
        """

        try:
            (clause_id, is_original_clause) = contradiction_clause
        except TypeError:
            raise MyException.SomethingWrongException("Invalid type of contradiction clause!")

        # Check if the clause causes a contradiction
        if (is_original_clause and not self.__is_clause_unsatisfied(clause_id)):
            raise MyException.ClauseDoesNotCauseAContradictionCnfException(self.__cnf[clause_id])
        if (not is_original_clause and not self.__is_learned_clause_unsatisfied(clause_id)):
            raise MyException.ClauseDoesNotCauseAContradictionCnfException(self.__learned_clauses[clause_id])

        self.__number_of_contradictions += 1
        if (not is_original_clause):
            self.__number_of_contradictions_caused_by_learned_clauses += 1

        # VSIDS
        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.VSIDS):
            self.__number_of_conflicts_VSIDS_decision_heuristic += 1
            self.__decay_VSIDS_decision_heuristic()

        # Restart
        if (self.__has_restart()):
            self.__increment_number_of_conflicts()
            if (self.__restart()):
                return 0 # New decision level

        # Update active_counter_learned_clause_dictionary
        if (self.__is_keep_active_clauses_heuristic() and not is_original_clause):
            if (clause_id not in self.__active_counter_learned_clause_dictionary):
                self.__active_counter_learned_clause_dictionary[clause_id] = 1
            else:
                self.__active_counter_learned_clause_dictionary[clause_id] += 1

        temp_contradiction_clause = []
        if (is_original_clause):
            temp_contradiction_clause = self.__cnf[clause_id]
        else:
            temp_contradiction_clause = self.__learned_clauses[clause_id]

        if (self.__clause_learning_enum == ClauseLearningEnum.StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent):
            assertive_clause = self.__create_assertive_clause(temp_contradiction_clause)
            assertive_level = self.__get_assertive_level(assertive_clause)
            self.__add_learned_clause(assertive_clause)
            self.__unit_propagation_clause_deletion()
            return assertive_level

        if (self.__clause_learning_enum == ClauseLearningEnum.StopAtTheFirstUIP):
            assertive_clause = self.__create_assertive_clause_with_1_uip(temp_contradiction_clause)
            assertive_level = self.__get_assertive_level(assertive_clause)
            self.__add_learned_clause(assertive_clause)
            self.__unit_propagation_clause_deletion()
            return assertive_level

        raise MyException.UndefinedClauseLearningCnfException(str(self.__clause_learning_enum))

    def __unit_propagation_clause_deletion(self):
        if (self.__has_clause_deletion_when_heuristic()):
            if (self.__max_size_of_cache <= self.__number_of_learned_clauses):
                self.__max_size_of_cache = next(self.__clause_deletion_when_iterator)
                self.__clause_deletion()

    def __unit_propagation_adjacency_list(self):
        temp_contradiction = None

        while (True):
            # CNF
            while (self.__unit_clause_list and (temp_contradiction is None)):
                clause_id = self.__unit_clause_list.pop()

                self.__increment_number_of_checked_clauses()
                undefined_literal_list = self.__undefined_literal_list_for_clause(clause_id)
                l = undefined_literal_list.pop()

                if (self.__use_learned_clauses):
                    self.__update_learned_clauses_unit_propagation(l, clause_id, True)

                self.__number_of_unit_propagations += 1
                self.add_literal_to_partial_assignment(l)

                if (len(self.__contradiction_clause_list) != 0):
                    temp_contradiction = (self.__contradiction_clause_list[0], True)

            # Learned clauses
            while (self.__use_learned_clauses and self.__unit_learned_clause_list and (temp_contradiction is None)):
                learned_clause_id = self.__unit_learned_clause_list.pop()

                self.__increment_number_of_checked_clauses()
                undefined_literal_list = self.__undefined_literal_list_for_learned_clause(learned_clause_id)
                l = undefined_literal_list.pop()

                self.__update_learned_clauses_unit_propagation(l, learned_clause_id, False)
                
                # Update active_counter_learned_clause_dictionary
                if (self.__is_keep_active_clauses_2_heuristic()):
                    if (learned_clause_id not in self.__active_counter_learned_clause_dictionary):
                        self.__active_counter_learned_clause_dictionary[learned_clause_id] = 1
                    else:
                        self.__active_counter_learned_clause_dictionary[learned_clause_id] += 1

                self.__number_of_unit_propagations += 1
                self.__number_of_unit_propagations_caused_by_learned_clauses += 1
                self.add_literal_to_partial_assignment(l)

                # Learned clauses - contradiction
                if (len(self.__contradiction_learned_clause_list) != 0):
                    temp_contradiction = (self.__contradiction_learned_clause_list[0], False)

                # Original CNF - contradiction
                if (len(self.__contradiction_clause_list) != 0):
                    temp_contradiction = (self.__contradiction_clause_list[0], True)

            if ((not self.__unit_clause_list and (not self.__use_learned_clauses or not self.__unit_learned_clause_list)) 
                or temp_contradiction is not None):
                break

        return temp_contradiction

    def __unit_propagation_watched_literals(self):
        end = False
        temp_contradiction = None
        unit_clause_literal_list = []

        while ((not end) and (temp_contradiction is None)):
            end = True
            for ((w_l_1, w_l_2), clause_id, is_original_clause) in self.__my_iteration_original_and_learned_wtached_literals():
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

                # Clause contains only one literal which is not satisfied => contradiction
                if (((w_l_1 is None) and (is_w_l_2_defined)) or ((w_l_2 is None) and (is_w_l_1_defined))):
                    temp_contradiction = (clause_id, is_original_clause)
                    break

                # Contradiction
                if (is_w_l_1_defined and is_w_l_2_defined):
                    temp_contradiction = (clause_id, is_original_clause)
                    break

                # First watched literal is undefined, the second one is unsatisfied
                if (not is_w_l_1_defined):
                    unit_clause_literal_list.append((w_l_1, clause_id, is_original_clause))
                    continue

                # Second watched literal is undefined, the first one is unsatisfied
                if (not is_w_l_2_defined):
                    unit_clause_literal_list.append((w_l_2, clause_id, is_original_clause))
                    continue
            
            temp_hashset = set()

            while (unit_clause_literal_list and (temp_contradiction is None)):
                (x, clause_id, is_original_clause) = unit_clause_literal_list.pop()

                if (x in temp_hashset):
                    continue

                if (-x not in temp_hashset):
                    end = False
                    temp_hashset.add(x)

                    if (self.__use_learned_clauses):
                        self.__update_learned_clauses_unit_propagation(x, clause_id, is_original_clause)
                        if (not is_original_clause):
                            self.__number_of_unit_propagations_caused_by_learned_clauses += 1

                    # Update active_counter_learned_clause_dictionary
                    if (not is_original_clause and self.__is_keep_active_clauses_2_heuristic()):
                        if (clause_id not in self.__active_counter_learned_clause_dictionary):
                            self.__active_counter_learned_clause_dictionary[clause_id] = 1
                        else:
                            self.__active_counter_learned_clause_dictionary[clause_id] += 1

                    self.__number_of_unit_propagations += 1
                    self.add_literal_to_partial_assignment(x)
                # Contradiction
                else:
                    temp_contradiction = (clause_id, is_original_clause)
        
        return temp_contradiction

    def add_literal_to_partial_assignment(self, literal, check_partial_assignment = False):
        self.__partial_assignment_list.append([literal, self.__current_decision_level])
        self.__partial_assignment_only_literals_hashset.add(literal)
        self.__variable_level_dictionary[abs(literal)] = self.__current_decision_level

        self.__undefined_literals_hashset.remove(literal)
        self.__undefined_literals_hashset.remove(-literal)

        # Check if the partial assignment is valid
        if (check_partial_assignment and not(self.__check_partial_assignment())):
            raise MyException.InvalidLiteralInPartialAssignmentCnfException(str(self.__partial_assignment_list))

        # Jeroslow-Wang
        if (self.__is_Jeroslow_Wang_decision_variable_heuristic() and 
            self.__score_Jeroslow_Wang_heap is not None and len(self.__score_Jeroslow_Wang_heap)):
            # Literal is the minimum in the heap
            if (literal == self.__score_Jeroslow_Wang_heap[0][1]):
                heapq.heappop(self.__score_Jeroslow_Wang_heap)
            else:
                self.__score_Jeroslow_Wang_heap = None

        # VSIDS
        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.VSIDS and
            self.__score_VSIDS_heap is not None and len(self.__score_VSIDS_heap)):
            # Literal is the minimum in the heap
            if (literal == self.__score_VSIDS_heap[0][1]):
                heapq.heappop(self.__score_VSIDS_heap)
            else:
                self.__score_VSIDS_heap = None

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
        
        # Jeroslow-Wang
        if (self.__is_Jeroslow_Wang_decision_variable_heuristic()):
            self.__add_variable_to_score_Jeroslow_Wang_heap(abs(literal))

        # VSIDS
        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.VSIDS):
            self.__add_variable_to_score_VSIDS_heap(abs(literal))

        level = self.level_in_partial_assignment_for_literal(literal)

        self.__variable_level_dictionary.pop(abs(literal))
        self.__partial_assignment_list.remove([literal, level])
        self.__partial_assignment_only_literals_hashset.remove(literal)

        self.__undefined_literals_hashset.add(literal)
        self.__undefined_literals_hashset.add(-literal)

        # Learned clauses
        if (self.__use_learned_clauses and self.__antecedent_dictionary[abs(literal)] is not None):
            (clause_id, is_original_clause) = self.__antecedent_dictionary[abs(literal)]
            self.__antecedent_dictionary[abs(literal)] = None
            if (not is_original_clause):
                self.__active_learned_clause_hashset.remove(clause_id)
        
        if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
            self.__update_counter(literal)
        elif (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
            pass;
        else:
            raise MyException.UndefinedUnitPropagationCnfException(str(self.__unit_propagation_enum))

    def __update_counter(self, literal):
        variable = abs(literal)

        # CNF
        for clause_id in self.__adjacency_list_dictionary[variable]:
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

        if (not self.__use_learned_clauses):
            return

        # Learned clauses
        for learned_clause_id in self.__adjacency_list_learned_clause_dictionary[variable]:
            if (learned_clause_id in self.__contradiction_learned_clause_list):
                self.__contradiction_learned_clause_list.remove(learned_clause_id)

            if (learned_clause_id in self.__unit_learned_clause_list):
                self.__unit_learned_clause_list.remove(learned_clause_id)

            self.__increment_number_of_checked_clauses()
            is_satisfied = self.__is_learned_clause_satisfied(learned_clause_id)

            # Clause is satisfied
            if (is_satisfied):
                self.__counter_learned_clause_list[learned_clause_id] = 0
            else:
                undefined_literal_list = self.__undefined_literal_list_for_learned_clause(learned_clause_id)
                # Clause is unsatisfied
                if (len(undefined_literal_list) == 0):
                    self.__counter_learned_clause_list[learned_clause_id] = 0
                    self.__contradiction_learned_clause_list.append(learned_clause_id)
                # Unit clause
                elif (len(undefined_literal_list) == 1):
                    self.__counter_learned_clause_list[learned_clause_id] = 1
                    self.__unit_learned_clause_list.append(learned_clause_id)
                else:
                    self.__counter_learned_clause_list[learned_clause_id] = len(undefined_literal_list)

    def __update_watched_literals(self, literal):
        variable = abs(literal)

        # CNF
        clauses_to_delete_list = []

        for clause_id in self.__variable_watched_literals_dictionary[variable][int (literal > 0)]:
            w_l_1 = -literal
            w_l_2 = self.__clause_watched_literals_list[clause_id][0] if (self.__clause_watched_literals_list[clause_id][0] != w_l_1) else self.__clause_watched_literals_list[clause_id][1]
            
            self.__increment_number_of_checked_clauses()
            valid_value_for_w_l_1_iterator = filter(lambda x: (-x not in self.__partial_assignment_only_literals_hashset) and (x != w_l_2), self.__cnf[clause_id])
            w_l_1 = next(valid_value_for_w_l_1_iterator, None)

            # Exists a new valid value for watched literal
            if (w_l_1 is not None):
                clauses_to_delete_list.append(clause_id)
                self.__variable_watched_literals_dictionary[abs(w_l_1)][int (-w_l_1 > 0)].add(clause_id)
                self.__clause_watched_literals_list[clause_id] = (w_l_1, w_l_2)

        for clause_id in clauses_to_delete_list:
            self.__variable_watched_literals_dictionary[variable][int (literal > 0)].remove(clause_id)

        if (not self.__use_learned_clauses):
            return

        # Learned clauses
        learned_clause_to_delete_list = []
        for learned_clause_id in self.__variable_watched_literals_learned_clause_dictionary[variable][int (literal > 0)]:
            w_l_1 = -literal
            w_l_2 = self.__learned_clause_watched_literals_list[learned_clause_id][0] if (self.__learned_clause_watched_literals_list[learned_clause_id][0] != w_l_1) else self.__learned_clause_watched_literals_list[learned_clause_id][1]
            
            self.__increment_number_of_checked_clauses()
            valid_value_for_w_l_1_iterator = filter(lambda x: (-x not in self.__partial_assignment_only_literals_hashset) and (x != w_l_2), self.__learned_clauses[learned_clause_id])
            w_l_1 = next(valid_value_for_w_l_1_iterator, None)

            # Exists a new valid value for watched literal
            if (w_l_1 is not None):
                learned_clause_to_delete_list.append(learned_clause_id)
                self.__variable_watched_literals_learned_clause_dictionary[abs(w_l_1)][int (-w_l_1 > 0)].add(learned_clause_id)
                self.__learned_clause_watched_literals_list[learned_clause_id] = (w_l_1, w_l_2)

        for learned_clause_id in learned_clause_to_delete_list:
            self.__variable_watched_literals_learned_clause_dictionary[variable][int (literal > 0)].remove(learned_clause_id)

    def __is_clause_satisfied(self, clause_id):
        clause = self.__cnf[clause_id]
        return any(x in self.__partial_assignment_only_literals_hashset for x in clause)
    
    def __is_clause_unsatisfied(self, clause_id):
        clause = self.__cnf[clause_id]
        return all(-x in self.__partial_assignment_only_literals_hashset for x in clause)

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

    def __my_iteration_original_and_learned_wtached_literals(self):
        """
        Return ((w_l_1, w_l_2), clause_id, isOriginal), where w_l_1 and w_l_2 are watched literals, isOriginal is True if it is not a learned clause, otherwise False
        """

        for (i, x) in enumerate(self.__clause_watched_literals_list):
            yield (x, i, True)

        if (not self.__use_learned_clauses):
            return

        for (i, x) in enumerate(self.__learned_clause_watched_literals_list):
            yield (x, i, False)

    # Decision level
    def increment_current_decision_level(self, number = 1):
        self.__current_decision_level += number

    def decrement_current_decision_level(self, number = 1):
        self.__current_decision_level -= number

    def backtrack_to_decision_level(self, decision_level):
        if (decision_level < 0 or decision_level > self.__current_decision_level):
            raise MyException.InvalidDecisionLevelCnfException(decision_level)

        while (self.__partial_assignment_list):
            (literal, level) = self.__partial_assignment_list[-1]
            if (level > decision_level):
                self.remove_literal_from_partial_assignment(literal)
            else:
                break

    # Learned clauses
    def __is_learned_clause_satisfied(self, learned_clause_id):
        learned_clause = self.__learned_clauses[learned_clause_id]
        return any(x in self.__partial_assignment_only_literals_hashset for x in learned_clause)

    def __is_learned_clause_unsatisfied(self, learned_clause_id):
        learned_clause = self.__learned_clauses[learned_clause_id]
        return all(-x in self.__partial_assignment_only_literals_hashset for x in learned_clause)

    def __undefined_literal_list_for_learned_clause(self, learned_clause_id):
        learned_clause = self.__learned_clauses[learned_clause_id]
        return (list(filter(lambda x: (x not in self.__partial_assignment_only_literals_hashset) and (-x not in self.__partial_assignment_only_literals_hashset), learned_clause)))

    def __add_learned_clause(self, learned_clause):
        # Check if the learned clause has valid literals
        if (not(all(x in self.__literal_list for x in learned_clause))):
            raise MyException.InvalidLiteralInLearnedClauseCnfException("Invalid literal in learned clause: {0}".format(learned_clause))
        
        # Learned clause is empty
        if (not learned_clause):
            return

        # Jeroslow-Wang
        if (self.__is_dynamic_Jeroslow_Wang_decision_variable_heuristic()):
            learned_clause_size = len(learned_clause)
            for literal in learned_clause:
                self.__update_score_Jeroslow_Wang_dictionary(literal, learned_clause_size)

        # VSIDS
        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.VSIDS):
            for literal in learned_clause:
                self.__update_score_VSIDS_dictionary(literal)

        learned_clause_id = self.__number_of_learned_clauses
        self.__number_of_learned_clauses += 1
        self.__learned_clauses.append(learned_clause)

        # Adjacency list
        if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
            is_satisfied = self.__is_learned_clause_satisfied(learned_clause_id)

            # Fill adjacency_list_learned_clause_dictionary
            for literal in learned_clause:
                self.__adjacency_list_learned_clause_dictionary[abs(literal)].add(learned_clause_id)

            # Learned clause is satisfied
            if (is_satisfied):
                self.__counter_learned_clause_list.append(0)
            else:
                undefined_literal_list = self.__undefined_literal_list_for_learned_clause(learned_clause_id)
                # Learned clause is unsatisfied
                if (len(undefined_literal_list) == 0):
                    self.__counter_learned_clause_list.append(0)
                    self.__contradiction_learned_clause_list.append(learned_clause_id)
                # Unit learned clause
                elif (len(undefined_literal_list) == 1):
                    self.__counter_learned_clause_list.append(1)
                    self.__unit_learned_clause_list.append(learned_clause_id)
                else:
                    self.__counter_learned_clause_list.append(len(undefined_literal_list))

        # Watched literals
        elif (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
            # Learned clause has only one literal
            if (len(learned_clause) == 1):
                temp_watched_literal = learned_clause[0]
                self.__learned_clause_watched_literals_list.append((temp_watched_literal, None))
                self.__variable_watched_literals_learned_clause_dictionary[abs(temp_watched_literal)][int (-temp_watched_literal > 0)].add(learned_clause_id)
            else:
                temp_satisfied_list = []
                temp_unsatisfied_list = []
                temp_undefined_list = []

                for (literal, _) in self.__partial_assignment_list:
                    # Satisfied literal
                    if (literal in learned_clause):
                        temp_satisfied_list.append(literal)
                    # Unsatisfied literal
                    elif (-literal in learned_clause):
                        temp_unsatisfied_list.append(-literal)

                temp_unsatisfied_list.reverse()

                for literal in learned_clause:
                    if (literal in self.__partial_assignment_only_literals_hashset or 
                        -literal in self.__partial_assignment_only_literals_hashset):
                        continue
                    else:
                        temp_undefined_list.append(literal)

                temp_list = temp_satisfied_list + temp_undefined_list + temp_unsatisfied_list
                temp_watched_literal_1 = temp_list[0]
                temp_watched_literal_2 = temp_list[1]
                self.__learned_clause_watched_literals_list.append((temp_watched_literal_1, temp_watched_literal_2))
                self.__variable_watched_literals_learned_clause_dictionary[abs(temp_watched_literal_1)][int (-temp_watched_literal_1 > 0)].add(learned_clause_id)
                self.__variable_watched_literals_learned_clause_dictionary[abs(temp_watched_literal_2)][int (-temp_watched_literal_2 > 0)].add(learned_clause_id)
        
        else:
            raise MyException.UndefinedUnitPropagationCnfException(str(self.__unit_propagation_enum))

    def __remove_learned_clauses(self, learned_clauses_to_delete_list):
        self.__increment_number_of_deleted_learned_clauses(len(learned_clauses_to_delete_list))
        learned_clauses_to_delete_list = sorted(learned_clauses_to_delete_list)
        learned_clauses_to_delete_hashset = set()

        for i in learned_clauses_to_delete_list:
            learned_clauses_to_delete_hashset.add(i)

        temp_list = []
        for i in range(self.__number_of_learned_clauses):
            if i not in learned_clauses_to_delete_list:
                temp_list.append(i)

        # Create mapping
        map_old_to_new_dictionary = {}
        map_new_to_old_dictionary = {}
        for i in range(len(temp_list)):
            map_old_to_new_dictionary[temp_list[i]] = i
            map_new_to_old_dictionary[i] = temp_list[i]

        # Learned clauses
        # learned_clauses and number_of_learned_clauses
        temp_learned_clauses = []
        for (learned_clause_id, learned_clause) in enumerate(self.__learned_clauses):
            if (learned_clause_id not in learned_clauses_to_delete_hashset):
                temp_learned_clauses.append(learned_clause)
        self.__learned_clauses = temp_learned_clauses
        self.__number_of_learned_clauses = len(self.__learned_clauses)
        # antecedent_dictionary
        for variable in self.__antecedent_dictionary:
            temp_antecedent = self.__antecedent_dictionary[variable]
            if (temp_antecedent is None):
                continue
            (clause_id, is_original_clause) = temp_antecedent
            if (is_original_clause):
                continue
            new_index = map_old_to_new_dictionary[clause_id]
            self.__antecedent_dictionary[variable] = (new_index, is_original_clause)
        # active_learned_clause_hashset
        temp_active_learned_clause_hashset = set()
        for learned_clause_id in self.__active_learned_clause_hashset:
            new_index = map_old_to_new_dictionary[learned_clause_id]
            temp_active_learned_clause_hashset.add(new_index)
        self.__active_learned_clause_hashset = temp_active_learned_clause_hashset

        # Keep active
        if (self.__is_keep_active_clauses_heuristic()):
            temp_active_counter_learned_clause_dictionary = {}
            for learned_clause_id in range(self.__number_of_learned_clauses):
                old_index = map_new_to_old_dictionary[learned_clause_id]
                temp_active_counter_learned_clause_dictionary[learned_clause_id] = self.__active_counter_learned_clause_dictionary.get(old_index, 0)
            self.__active_counter_learned_clause_dictionary = temp_active_counter_learned_clause_dictionary

        # Adjacency list
        if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
            # counter_learned_clause_list
            temp_counter_learned_clause_list = []
            for (learned_clause_id, counter) in enumerate(self.__counter_learned_clause_list):
                if (learned_clause_id not in learned_clauses_to_delete_hashset):
                    temp_counter_learned_clause_list.append(counter)
            self.__counter_learned_clause_list = temp_counter_learned_clause_list

            # adjacency_list_learned_clause_dictionary
            for variable in self.__adjacency_list_learned_clause_dictionary:
                temp_hashset = set()
                for learned_clause_id in self.__adjacency_list_learned_clause_dictionary[variable]:
                    if (learned_clause_id in learned_clauses_to_delete_hashset):
                        continue

                    new_index = map_old_to_new_dictionary[learned_clause_id]
                    temp_hashset.add(new_index)
                self.__adjacency_list_learned_clause_dictionary[variable] = temp_hashset

            # unit_learned_clause_list
            temp_unit_learned_clause_list = []
            for learned_clause_id in self.__unit_learned_clause_list:
                if (learned_clause_id not in learned_clauses_to_delete_hashset):
                    new_index = map_old_to_new_dictionary[learned_clause_id]
                    temp_unit_learned_clause_list.append(new_index)
            self.__unit_learned_clause_list = temp_unit_learned_clause_list

            # contradiction_learned_clause_list
            temp_contradiction_learned_clause_list = []
            for learned_clause_id in self.__contradiction_learned_clause_list:
                if (learned_clause_id not in learned_clauses_to_delete_hashset):
                    new_index = map_old_to_new_dictionary[learned_clause_id]
                    temp_contradiction_learned_clause_list.append(new_index)
            self.__contradiction_learned_clause_list = temp_contradiction_learned_clause_list

        # Watched literals
        if (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
            # learned_clause_watched_literals_list
            temp_learned_clause_watched_literals_list = []
            for (learned_clause_id, watched_literals) in enumerate(self.__learned_clause_watched_literals_list):
                if (learned_clause_id not in learned_clauses_to_delete_hashset):
                    temp_learned_clause_watched_literals_list.append(watched_literals)
            self.__learned_clause_watched_literals_list = temp_learned_clause_watched_literals_list

            # variable_watched_literals_learned_clause_dictionary
            for variable in self.__variable_watched_literals_learned_clause_dictionary:
                (positive_hashset, negative_hashset) = self.__variable_watched_literals_learned_clause_dictionary[variable]
                # Positive hashset
                temp_positive_hashset = set()
                for learned_clauses_id in positive_hashset:
                    if (learned_clauses_id in learned_clauses_to_delete_hashset):
                        continue

                    new_index = map_old_to_new_dictionary[learned_clauses_id]
                    temp_positive_hashset.add(new_index)
                # Negative hashset
                temp_negative_hashset = set()
                for learned_clauses_id in negative_hashset:
                    if (learned_clauses_id in learned_clauses_to_delete_hashset):
                        continue

                    new_index = map_old_to_new_dictionary[learned_clauses_id]
                    temp_negative_hashset.add(new_index)
                
                self.__variable_watched_literals_learned_clause_dictionary[variable] = (temp_positive_hashset, temp_negative_hashset)

    def __remove_all_learned_clauses(self):
        # Check if all learned clauses are not active
        if (self.__active_learned_clause_hashset):
            raise MyException.AttemptToDeleteActiveLearnedClauseCnfException()

        self.__number_of_learned_clauses = 0
        self.__learned_clauses = []

        # Keep active
        if (self.__is_keep_active_clauses_heuristic()):
            self.__active_counter_learned_clause_dictionary = {}

        # Adjacency list
        if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
            self.__counter_learned_clause_list = []
            self.__unit_learned_clause_list = []
            self.__contradiction_learned_clause_list = []
            self.__adjacency_list_learned_clause_dictionary = {}
            for variable in self.__variable_list:
                self.__adjacency_list_learned_clause_dictionary[variable] = set()

        # Watched literals
        elif (self.__unit_propagation_enum == UnitPropagationEnum.WatchedLiterals):
            self.__learned_clause_watched_literals_list = []
            self.__variable_watched_literals_learned_clause_dictionary = {}
            for variable in self.__variable_list:
                self.__variable_watched_literals_learned_clause_dictionary[variable] = (set(), set())

        else:
            raise MyException.UndefinedUnitPropagationCnfException(str(self.__unit_propagation_enum))

    def __update_learned_clauses_unit_propagation(self, literal, clause_id, is_original_clause):
        # Update antecedent_dictionary
        self.__antecedent_dictionary[abs(literal)] = (clause_id, is_original_clause)

        if (is_original_clause):
            return

        # Update active_learned_clause_hashset
        self.__active_learned_clause_hashset.add(clause_id)

    # Clause deletion (how)
    def __clause_deletion(self):
        self.__increment_number_of_clause_deletions()
        # None
        if (self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.none):
            return

        # Keep active clauses
        if (self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepActiveClauses or
            self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepActiveClauses2):
            learned_clauses_to_delete = self.__keep_active_clauses_heuristic()
            self.__remove_learned_clauses(learned_clauses_to_delete)
            return

        # Keep short clauses
        if (self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepShortClauses):
            learned_clauses_to_delete = self.__keep_short_clauses_heuristic()
            self.__remove_learned_clauses(learned_clauses_to_delete)
            return

        # Remove subsumed clauses
        if (self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.RemoveSubsumedClauses):
            learned_clauses_to_delete = self.__remove_subsumed_clauses_heuristic()
            self.__remove_learned_clauses(learned_clauses_to_delete)
            return

        # Keep active clauses and remove subsumed clauses
        if (self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepActiveClausesAndRemoveSubsumedClauses or
            self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepActiveClauses2AndRemoveSubsumedClauses):
            learned_clauses_to_delete = self.__remove_subsumed_clauses_heuristic()
            self.__remove_learned_clauses(learned_clauses_to_delete)
            learned_clauses_to_delete = self.__keep_active_clauses_heuristic()
            self.__remove_learned_clauses(learned_clauses_to_delete)
            return

        # Keep short clauses and remove subsumed clauses
        if (self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepShortClausesAndRemoveSubsumedClauses):
            learned_clauses_to_delete = self.__remove_subsumed_clauses_heuristic()
            self.__remove_learned_clauses(learned_clauses_to_delete)
            learned_clauses_to_delete = self.__keep_short_clauses_heuristic()
            self.__remove_learned_clauses(learned_clauses_to_delete)
            return

        raise MyException.UndefinedClauseDeletionHowHeuristicCnfException(str(self.__clause_deletion_how_heuristic_enum))

    def __keep_short_clauses_heuristic(self):
        """
        Clause deletion - keep short clauses heuristic 
        Return a list of learned clauses which should be deleted
        """

        learned_clauses_to_delete = []

        for learned_clause_id in range(self.__number_of_learned_clauses):
            # Learned clause is active
            if (learned_clause_id in self.__active_learned_clause_hashset):
                continue

            size = len(self.__learned_clauses[learned_clause_id])
            # Size of learned clause is bounded by k
            if (size <= self.__bound_keep_short_clauses_heuristic):
                continue

            # Size of learned clause is not bounded by k
            probability = 1 / (size - self.__bound_keep_short_clauses_heuristic + 1)
            if (random.random() >= probability):
                learned_clauses_to_delete.append(learned_clause_id)

        return learned_clauses_to_delete

    def __keep_active_clauses_heuristic(self):
        """
        Clause deletion - keep active clauses heuristic
        Return a list of learned clauses which should be deleted
        """

        learned_clauses_to_delete = []

        temp_learned_clause_list = [] # [[activity, size, id], ... ]
        for learned_clause_id in range(self.__number_of_learned_clauses):
            # Learned clause is active
            if (learned_clause_id in self.__active_learned_clause_hashset):
                continue
            if (learned_clause_id in self.__active_counter_learned_clause_dictionary):
                activity = self.__active_counter_learned_clause_dictionary[learned_clause_id]
                activity *= -1 # Hack - we don't need reverse this attribute
            else:
                activity = 0
            size = len(self.__learned_clauses[learned_clause_id])
            temp_learned_clause_list.append([activity, size, learned_clause_id])

        temp_learned_clause_list = sorted(temp_learned_clause_list, key = operator.itemgetter(0, 1, 2))

        for i in range(int(len(temp_learned_clause_list) * self.__ratio_keep_active_clauses_heuristic), len(temp_learned_clause_list)):
            learned_clauses_to_delete.append(temp_learned_clause_list[i][2])

        return learned_clauses_to_delete

    def __remove_subsumed_clauses_heuristic(self):
        """
        Clause deletion - remove subsumed clauses heuristic
        Return a list of learned clauses which should be deleted
        """

        learned_clauses_to_delete_hashset = set()

        for learned_clause_id in range(self.__number_of_learned_clauses):
            learned_clauses_to_delete_hashset = self.__supperset_learned_clause(learned_clause_id, learned_clauses_to_delete_hashset)

        return list(learned_clauses_to_delete_hashset)

    def __is_subset_learned_clause(self, clause_id):
        """
        Return true if the learned clause with the id (clause_id) is a subset of any saved learned clause, otherwise return false
        """
        
        clause = self.__learned_clauses[clause_id]

        for (learned_clause_id, learned_clause) in enumerate(self.__learned_clauses):
            # Same clause
            if (clause_id == learned_clause_id):
                continue

            if (all(x in learned_clause for x in clause)):
                return True

        return False

    def __supperset_learned_clause(self, clause_id, superset_hashset = {}):
        """
        Return a hashset contains all learned clauses which are supersets of the learned clause with the id (clause_id)
        """

        clause = self.__learned_clauses[clause_id]

        for (learned_clause_id, learned_clause) in enumerate(self.__learned_clauses):
            # Same clause
            if (learned_clause_id == clause_id):
                continue

            if (all(x in learned_clause for x in clause)):
                if (learned_clause_id in self.__active_learned_clause_hashset):
                    continue
                else:
                    superset_hashset.add(learned_clause_id)

        return superset_hashset

    def __is_keep_active_clauses_heuristic(self):
        """
        Return true if the clause deletion heuristic is keep active clauses, otherwise false
        """

        if (self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepActiveClauses or 
            self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepActiveClausesAndRemoveSubsumedClauses or
            self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepActiveClauses2 or 
            self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepActiveClauses2AndRemoveSubsumedClauses):
            return True

        return False

    def __is_keep_active_clauses_2_heuristic(self):
        """
        Return true if the clause deletion heuristic is keep active clauses 2, otherwise false
        """

        if (self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepActiveClauses2 or 
            self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepActiveClauses2AndRemoveSubsumedClauses):
            return True

        return False

    def __is_remove_subsumed_clauses_heuristic(self):
        """
        Return true if the clause deletion heuristic is remove subsumed clauses, otherwise false
        """

        if (self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.RemoveSubsumedClauses or
            self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepActiveClausesAndRemoveSubsumedClauses):
            return True

        return False

    def __is_keep_short_clauses_heuristic(self):
        """
        Return true if the clause deletion heuristic is keep short clauses, otherwise false
        """

        if (self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepShortClauses or 
            self.__clause_deletion_how_heuristic_enum == ClauseDeletionHowHeuristicEnum.KeepShortClausesAndRemoveSubsumedClauses):
            return True

        return False

    def __increment_number_of_deleted_learned_clauses(self, number = 1):
        self.__number_of_deleted_learned_clauses += number

    def __increment_number_of_clause_deletions(self, number = 1):
        self.__number_of_clause_deletions += number

    # Clause deletion (when)
    def __get_clause_deletion_when_iterator(self):
        # Restart
        if (self.__clause_deletion_when_heuristic_enum == ClauseDeletionWhenHeuristicEnum.Restart):
            return self.__max_value_iterator()

        # Cache - geometric
        if (self.__clause_deletion_when_heuristic_enum == ClauseDeletionWhenHeuristicEnum.CacheFull):
            return self.__geometric_cache_clause_deletion_iterator()

        raise MyException.UndefinedClauseDeletionWhenHeuristicCnfException(str(self.__clause_deletion_when_heuristic_enum))

    def __geometric_cache_clause_deletion_iterator(self):
        value = self.__first_term_geometric_cache_clause_deletion
        yield value

        while (True):
            value = int(value * self.__common_ratio_geometric_cache_clause_deletion)
            yield value

    def __max_value_iterator(self):
        while (True):
            yield sys.maxsize**10

    def __has_clause_deletion_when_heuristic(self):
        if (self.__clause_deletion_when_heuristic_enum != ClauseDeletionWhenHeuristicEnum.none):
            return True

        return False

    # Assertive clauses
    def __create_assertive_clause(self, contradiction_clause):
        clause = copy.deepcopy(contradiction_clause)

        while (True):
            literal_iterator = filter(lambda x : True if (self.__variable_level_dictionary[abs(x)] == self.__current_decision_level and self.__antecedent_dictionary[abs(x)] is not None) 
                                                      else False
                                     , clause)

            literal = next(literal_iterator, None)
            if (literal is None):
                break

            temp_clause = []
            (clause_id, is_original_clause) = self.__antecedent_dictionary[abs(literal)]
            if (is_original_clause):
                temp_clause = self.__cnf[clause_id]
            else:
                temp_clause = self.__learned_clauses[clause_id]
            clause = self.__resolution(clause, temp_clause, literal)

        return clause
   
    def __create_assertive_clause_with_1_uip(self, contradiction_clause):
        clause = copy.deepcopy(contradiction_clause)

        while (True):
            literal_list = list(filter(lambda x: True if (self.__variable_level_dictionary[abs(x)] == self.__current_decision_level) 
                                                      else False
                                      , clause))

            if (len(literal_list) <= 1):
                break

            literal = literal_list[0]
            for (x, _) in self.__partial_assignment_list[::-1]:
                if (x in literal_list):
                    literal = x
                    break

                elif (-x in literal_list):
                    literal = -x
                    break

            temp_clause = []
            (clause_id, is_original_clause) = self.__antecedent_dictionary[abs(literal)]
            if (is_original_clause):
                temp_clause = self.__cnf[clause_id]
            else:
                temp_clause = self.__learned_clauses[clause_id]
                
            clause = self.__resolution(clause, temp_clause, literal)
        return clause

    def __get_assertive_level(self, assertive_clause):
        # Assertive clause is a unit clause or an empty clause
        if (len(assertive_clause) == 0 or len(assertive_clause) == 1):
            return 0

        temp_list = []

        for x in assertive_clause:
            temp_list.append(self.__variable_level_dictionary[abs(x)])

        temp_list.remove(max(temp_list))

        return max(temp_list)

    def __resolution(self, clause_1, clause_2, literal):
        # Check if one of the clauses contains the literal and the second one contains negation of the literal
        if (not (literal in clause_1 and -literal in clause_2) and not (-literal in clause_1 and literal in clause_2)):
            raise MyException.ClausesDoNotContainLiteralResolutionCnfException("Literal: {0}, first clause: {1}, second clause: {2}".format(literal, clause_1, clause_2))

        resolvent = []

        for x in chain(clause_1, clause_2):
            if (abs(x) != abs(literal)):
                resolvent.append(x)

        # Get rid of redundancy
        resolvent = list(set(resolvent))

        return resolvent

    # Restart
    def __has_restart(self):
        """
        Return true if restarts are supported, otherwise false
        """

        if (self.__restart_strategy_enum != RestartStrategyEnum.none):
            return True

        return False

    def __increment_number_of_conflicts(self, number = 1):
        self.__number_of_conflicts += number

    def __reset_number_of_conflicts(self):
        self.__number_of_conflicts = 0

    def __get_restart_strategy_iterator(self):
        # Geometric strategy
        if (self.__restart_strategy_enum == RestartStrategyEnum.GeometricStrategy):
            return self.__geometric_restart_strategy_iterator()

        # Luby strategy
        if (self.__restart_strategy_enum == RestartStrategyEnum.LubyStrategy):
            return self.__luby_restart_strategy_iterator()

        raise MyException.UndefinedRestartStrategyCnfException(str(self.__restart_strategy_enum))

    def __geometric_restart_strategy_iterator(self):
        value = self.__first_term_geometric_restart_strategy
        yield value

        while (True):
            value = int(value * self.__common_ratio_geometric_restart_strategy)
            yield value

    def __luby_restart_strategy_iterator(self):
        for i in range(1, sys.maxsize**10):
            yield self.__unit_luby_restart_strategy * self.__luby_sequence(i)

    def __luby_sequence(self, i):
        for k in range(1, 32):
            if i == (1 << k) - 1:
                return 1 << (k - 1)
        for k in range(1, sys.maxsize**10):
            if (1 << (k - 1) <= i) and (i < (1 << k) - 1):
                return self.__luby_sequence(i - (1 << (k - 1)) + 1)

    def __restart(self):
        """
        Return true if restart happened otherwise false
        """

        if (self.__number_of_conflicts != self.__max_number_of_conflicts):
            return False

        self.__number_of_restarts += 1
        self.__number_of_conflicts = 0
        self.__max_number_of_conflicts = next(self.__restart_strategy_iterator)
        
        # Update data structures
        # Original CNF
        self.__partial_assignment_list = []
        self.__variable_level_dictionary = {}
        self.__partial_assignment_only_literals_hashset = set()
        self.__undefined_literals_hashset = set(self.__literal_list)

        # Learned clauses
        self.__active_learned_clause_hashset = set()
        for x in self.__antecedent_dictionary:
            self.__antecedent_dictionary[x] = None

        # Adjacency list
        if (self.__unit_propagation_enum == UnitPropagationEnum.AdjacencyList):
            for (i, clause) in enumerate(self.__cnf):
                self.__counter_list[i] = len(clause)

            for (i, learned_clause) in enumerate(self.__learned_clauses):
                self.__counter_learned_clause_list[i] = len(learned_clause)

            self.__unit_clause_list = []
            self.__contradiction_clause_list = []
            self.__unit_learned_clause_list = []
            self.__contradiction_learned_clause_list = []

        # Jeroslow-Wang
        if (self.__is_Jeroslow_Wang_decision_variable_heuristic()):
            self.__score_Jeroslow_Wang_heap = None
            # self.__initialize_Jeroslow_Wang_decision_variable_heuristic()

        # VSIDS
        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.VSIDS):
            self.__score_VSIDS_heap = None
            # self.__number_of_conflicts_VSIDS_decision_heuristic = 0
            # self.__initialize_VSIDS_decision_variable_heuristic()

        # Clause deletion
        if (self.__clause_deletion_when_heuristic_enum == ClauseDeletionWhenHeuristicEnum.Restart):
            self.__clause_deletion()
        
        return True

    # Decision variable
    def decision_literal(self):
        """
        Return a decision literal
        """

        # Greedy decision
        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.Greedy):
            return self.__decision_literal_greedy()

        # Random decision
        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.Random):
            return self.__decision_literal_random()

        # VSIDS
        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.VSIDS):
            # Heap is not created
            if (self.__score_VSIDS_heap is None):
                self.__create_score_VSIDS_heap()

            if (len(self.__score_VSIDS_heap)):
                return self.__score_VSIDS_heap[0][1] # (score, literal)
            else:
                return None

        # Jeroslow-Wang
        if (self.__is_Jeroslow_Wang_decision_variable_heuristic()):
            # Heap is not created
            if (self.__score_Jeroslow_Wang_heap is None):
                self.__create_score_Jeroslow_Wang_heap()

            if (len(self.__score_Jeroslow_Wang_heap)):
                return self.__score_Jeroslow_Wang_heap[0][1] # (score, literal)
            else:
                return None

        raise MyException.UndefinedDecisionHeuristicCnfException(str(self.__decision_heuristic_enum))

    def __decision_literal_greedy(self):
        """
        Return a decision literal
        """

        for clause in self.__cnf:
            # Clause is satisfied
            if (any(x in self.__partial_assignment_only_literals_hashset for x in clause)):
                continue

            # Clause is unresolved
            for x in clause:
                if (x not in self.__partial_assignment_only_literals_hashset) and (-x not in self.__partial_assignment_only_literals_hashset):
                    return x

        if (self.exists_undefined_variable()):
            return self.first_undefined_variable()

        return None

    def __decision_literal_random(self):
        """
        Return a random decision literal
        """

        # literal_hashset = set()

        # for clause in self.__cnf:
        #     # Clause is satisfied
        #     if (any(x in self.__partial_assignment_only_literals_hashset for x in clause)):
        #         continue

        #     # Clause is unresolved
        #     for x in clause:
        #         if (x not in self.__partial_assignment_only_literals_hashset) and (-x not in self.__partial_assignment_only_literals_hashset):
        #             literal_hashset.add(x)

        # if (literal_hashset):
        #     return random.sample(literal_hashset, 1)[0]

        # for x in self.__undefined_literals_hashset:
        #     if ((x not in self.__partial_assignment_list) and (-x not in self.__partial_assignment_list) and (-x is not literal_hashset)):
        #         return x

        # return None

        if (not self.__undefined_literals_hashset):
            return None

        return random.choice(list(self.__undefined_literals_hashset))

    def __is_Jeroslow_Wang_decision_variable_heuristic(self):
        """
        Return true if the decision variable heuristic is Jeroslow-Wang, otherwise false
        """
        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.JeroslowWangOneSided or
            self.__decision_heuristic_enum == DecisionHeuristicEnum.JeroslowWangOneSidedDynamic or
            self.__decision_heuristic_enum == DecisionHeuristicEnum.JeroslowWangTwoSided or
            self.__decision_heuristic_enum == DecisionHeuristicEnum.JeroslowWangTwoSidedDynamic):
            return True

        return False

    def __is_dynamic_Jeroslow_Wang_decision_variable_heuristic(self):
        """
        Return true if the decision variable heuristic is dynamic Jeroslow-Wang, otherwise false
        """

        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.JeroslowWangOneSidedDynamic or
            self.__decision_heuristic_enum == DecisionHeuristicEnum.JeroslowWangTwoSidedDynamic):
            return True

        return False

    def __is_one_sided_Jeroslow_Wang_decision_variable_heuristic(self):
        """
        Return true if the decision variable heuristic is one-sided Jeroslow-Wang, otherwise false
        """

        if (self.__decision_heuristic_enum == DecisionHeuristicEnum.JeroslowWangOneSided or
            self.__decision_heuristic_enum == DecisionHeuristicEnum.JeroslowWangOneSidedDynamic):
            return True

        return False

    def __initialize_Jeroslow_Wang_decision_variable_heuristic(self):
        self.__score_Jeroslow_Wang_dictionary = {}
        self.__score_Jeroslow_Wang_heap = None

        # Create dictionary
        for literal in self.__literal_list:
            self.__score_Jeroslow_Wang_dictionary[literal] = 0

        # Fill dictionary
        for clause in self.__cnf:
            clause_size = len(clause)
            for literal in clause:
                self.__update_score_Jeroslow_Wang_dictionary(literal, clause_size)

        # Create heap
        self.__create_score_Jeroslow_Wang_heap()

    def __update_score_Jeroslow_Wang_dictionary(self, literal, clause_size):
        self.__score_Jeroslow_Wang_dictionary[literal] += 2 ** (-clause_size)

        if (literal in self.__undefined_literals_hashset):
            self.__score_Jeroslow_Wang_heap = None

    def __create_score_Jeroslow_Wang_heap(self):
        temp_list = []

        for literal in self.__undefined_literals_hashset:
            # Negative literal
            if (literal < 0):
                continue

            score_positive = self.__score_Jeroslow_Wang_dictionary[literal]
            score_negative = self.__score_Jeroslow_Wang_dictionary[-literal]

            if (score_positive > score_negative):
                # One-sided
                if (self.__is_one_sided_Jeroslow_Wang_decision_variable_heuristic()):
                    temp_list.append((-score_positive, literal))
                # Two-sided
                else:
                    temp_list.append((-(score_positive + score_negative), literal))
            else:
                # One-sided
                if (self.__is_one_sided_Jeroslow_Wang_decision_variable_heuristic()):
                    temp_list.append((-score_negative, -literal))
                # Two-sided
                else:
                    temp_list.append((-(score_positive + score_negative), -literal))

        self.__score_Jeroslow_Wang_heap = temp_list
        heapq.heapify(self.__score_Jeroslow_Wang_heap)

    def __add_variable_to_score_Jeroslow_Wang_heap(self, variable):
        # Variable does not exist
        if (variable not in self.__variable_list):
            raise MyException.VariableDoesNotExistCnfException(str(variable))

        # Heap is not created
        if (self.__score_Jeroslow_Wang_heap is None):
            self.__create_score_Jeroslow_Wang_heap()

        score_positive = self.__score_Jeroslow_Wang_dictionary[variable]
        score_negative = self.__score_Jeroslow_Wang_dictionary[-variable]

        temp_tuple = (0, 0)

        if (score_positive > score_negative):
            # One-sided
            if (self.__is_one_sided_Jeroslow_Wang_decision_variable_heuristic()):
                temp_tuple = (-score_positive, variable)
            # Two-sided
            else:
                temp_tuple = (-(score_positive + score_negative), variable)
        else:
            # One-sided
            if (self.__is_one_sided_Jeroslow_Wang_decision_variable_heuristic()):
                temp_tuple = (-score_negative, -variable)
            # Two-sided
            else:
                temp_tuple = (-(score_positive + score_negative), -variable)

        if (temp_tuple in self.__score_Jeroslow_Wang_heap):
            raise MyException.SomethingWrongException("Duplication in the heap! (Jeroslow-Wang)\nValue: {0}\nHeap: {1}".format(temp_tuple, self.__score_Jeroslow_Wang_heap))

        heapq.heappush(self.__score_Jeroslow_Wang_heap, temp_tuple)

    def __initialize_VSIDS_decision_variable_heuristic(self):
        self.__score_VSIDS_dictionary = {}
        self.__score_VSIDS_heap = None

        # Create dictionary
        for literal in self.__literal_list:
            self.__score_VSIDS_dictionary[literal] = 0

        # Fill dictionary
        for clause in self.__cnf:
            for literal in clause:
                self.__update_score_VSIDS_dictionary(literal)

        # Create heap
        self.__create_score_VSIDS_heap()

    def __decay_VSIDS_decision_heuristic(self):
        """
        Return true if decay happened otherwise false
        """

        if (self.__number_of_conflicts_VSIDS_decision_heuristic != self.__decay_period_VSIDS_decision_heuristic):
            return False

        self.__number_of_decay += 1
        self.__number_of_conflicts_VSIDS_decision_heuristic = 0

        # Update dictionary
        for literal in self.__score_VSIDS_dictionary:
            self.__score_VSIDS_dictionary[literal] /= self.__decay_constant_VSIDS_decision_heuristic

        # Clear heap
        self.__score_VSIDS_heap = None
    
    def __update_score_VSIDS_dictionary(self, literal, number = 1):
        self.__score_VSIDS_dictionary[literal] += number

        if (literal in self.__undefined_literals_hashset):
            self.__score_VSIDS_heap = None
      
    def __create_score_VSIDS_heap(self):
        temp_list = []

        for literal in self.__undefined_literals_hashset:
            # Negative literal
            if (literal < 0):
                continue

            score_positive = self.__score_VSIDS_dictionary[literal]
            score_negative = self.__score_VSIDS_dictionary[-literal]

            if (score_positive > score_negative):
                temp_list.append((-score_positive, literal))
            else:
                temp_list.append((-score_negative, -literal))

        self.__score_VSIDS_heap = temp_list
        heapq.heapify(self.__score_VSIDS_heap)

    def __add_variable_to_score_VSIDS_heap(self, variable):
        # Variable does not exist
        if (variable not in self.__variable_list):
            raise MyException.VariableDoesNotExistCnfException(str(variable))

        # Heap is not created
        if (self.__score_VSIDS_heap is None):
            self.__create_score_VSIDS_heap()

        score_positive = self.__score_VSIDS_dictionary[variable]
        score_negative = self.__score_VSIDS_dictionary[-variable]

        temp_tuple = (0, 0)

        if (score_positive > score_negative):
            temp_tuple = (-score_positive, variable)
        else:
            temp_tuple = (-score_negative, -variable)

        if (temp_tuple in self.__score_VSIDS_heap):
            raise MyException.SomethingWrongException("Duplication in the heap! (VSIDS)\nValue: {0}\nHeap: {1}".format(temp_tuple, self.__score_VSIDS_heap))

        heapq.heappush(self.__score_VSIDS_heap, temp_tuple)

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
    def current_decision_level(self):
        """
        actual_level getter
        """

        return self.__current_decision_level

    @property
    def number_of_learned_clauses(self):
        """
        number_of_learned_clauses getter
        """

        return self.__number_of_learned_clauses

    @property
    def learned_clauses(self):
        """
        learned_clauses getter
        """

        if (not self.__use_learned_clauses):
            return None

        return self.__learned_clauses

    @current_decision_level.setter
    def current_decision_level(self, new_decision_level):
        """
        current_decision_level setter
        """

        # -1 == assumptions
        if (new_decision_level < -1):
            raise MyException.InvalidDecisionLevelCnfException(new_decision_level)

        self.__current_decision_level = new_decision_level

    @property
    def number_of_restarts(self):
        """
        number_of_restarts getter
        """

        return self.number_of_restarts

    @property
    def number_of_deleted_learned_clauses(self):
        """
        number_of_deleted_learned_clauses getter
        """

        return self.__number_of_deleted_learned_clauses

    @property
    def number_of_clause_deletions(self):
        """
        number_of_clause_deletions getter
        """

        return self.__number_of_clause_deletions

    @property
    def number_of_deleted_learned_clauses(self):
        """
        number_of_deleted_learned_clauses getter
        """

        return self.__number_of_deleted_learned_clauses

    @property
    def number_of_restarts(self):
        """
        number_of_restarts getter
        """

        return self.__number_of_restarts

    @property
    def number_of_contradictions(self):
        """
        number_of_contradictions getter
        """

        return self.__number_of_contradictions

    @property
    def number_of_unit_propagations(self):
        """
        number_of_unit_propagations getter
        """

        return self.__number_of_unit_propagations

    @property
    def number_of_contradictions_caused_by_learned_clauses(self):
        """
        number_of_contradictions_caused_by_learned_clauses getter
        """

        return self.__number_of_contradictions_caused_by_learned_clauses

    @property
    def number_of_unit_propagations_caused_by_learned_clauses(self):
        """
        number_of_unit_propagations_caused_by_learned_clauses getter
        """

        return self.__number_of_unit_propagations_caused_by_learned_clauses

    @property
    def active_learned_clause_hashset(self):
        """
        active_learned_clause_hashset getter
        """

        return self.__active_learned_clause_hashset

    @property
    def number_of_decay(self):
        """
        number_of_decay getter
        """

        return self.__number_of_decay