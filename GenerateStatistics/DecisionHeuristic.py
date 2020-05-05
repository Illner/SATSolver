import os
import random
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '../')

import MyException
from CNF import CNF
from CDCL import CDCL
from DerivationTree import DerivationTree
from LogicalSignEnum import LogicalSignEnum
from TseitinEncoding import TseitinEncoding
from ClauseLearningEnum import ClauseLearningEnum
from UnitPropagationEnum import UnitPropagationEnum
from RestartStrategyEnum import RestartStrategyEnum
from DecisionHeuristicEnum import DecisionHeuristicEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionHowHeuristicEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionWhenHeuristicEnum

path = os.path.join(os.path.dirname(__file__), '../CNF')
dictionary_list = ["20-91", "50-218", "75-325", "100-430", "125-538", "150-645"]
# dictionary_list = ["20-91", "50-218", "75-325", "100-430"]
# dictionary_list = ["JNH"]
# dictionary_list = ["AIS"]

x_axis_variables = [20, 50, 75, 100, 125, 150]
# x_axis_variables = [20, 50, 75, 100]
# x_axis_variables = [0]

count_list = [1024, 256, 128, 64, 32, 16]
# count_list = [1024, 256, 128, 64]
# count_list = [20]
# count_list = [4]

use_random = False

log_Random_list = []
log_JeroslowWangOneSided_list = []
log_JeroslowWangTwoSided_list = []
log_JeroslowWangOneSidedDynamic_list = []
log_JeroslowWangTwoSidedDynamic_list = []
log_VSIDS_list = []
log_eVSIDS_list = []

for i in range(len(dictionary_list)):
    print("\n" + str(i))
    log_Random_list.append([])
    log_JeroslowWangOneSided_list.append([])
    log_JeroslowWangTwoSided_list.append([])
    log_JeroslowWangOneSidedDynamic_list.append([])
    log_JeroslowWangTwoSidedDynamic_list.append([])
    log_VSIDS_list.append([])
    log_eVSIDS_list.append([])

    dictionary_path = os.path.join(path, dictionary_list[i])

    for j in range(count_list[i]):
        print("- "  + str(j))
        file = random.choice(os.listdir(dictionary_path))
        # file = "jnh" + str(j + 1) + ".cnf"
        # file = "ais" + str(6 + (j * 2)) + ".cnf"
        file_path = os.path.join(dictionary_path, file)

        print(file)

        is_sat = None
        if (file.startswith("uuf")):
            is_sat = False
            print("UNSAT")
        else:
            is_sat = True
            print("SAT")

        # is_sat = False

        with open(file_path, "r") as input_file:
            input_formula = input_file.read()

        # Random
        if (use_random):
            cnf = CNF(input_formula, 
                      unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                      decision_heuristic_enum=DecisionHeuristicEnum.Random,
                      clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                      clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses,
                      clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                      restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
            cdcl = CDCL(cnf)
            result = cdcl.CDCL()

            if (not cnf.verify(result)):
                raise MyException.SomethingWrongException("Invalid model - Random")

            if (is_sat and result is None):
                raise MyException.SomethingWrongException("Invalid model - Random")

            print("Time: " + str(cdcl.time))
            print("Number of decisions: " + str(cdcl.number_of_decisions))
            print("Number of steps of unit propagation: " + str(cdcl.number_of_steps_of_unit_propagation))
            print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))
            print("Number of deleted learned clauses: " + str(cnf.number_of_deleted_learned_clauses))
            print("Number of clause deletions: " + str(cnf.number_of_clause_deletions))
            print("Number of contradictions: " + str(cnf.number_of_contradictions))
            print("Number of contradictions caused by learned clauses: " + str(cnf.number_of_contradictions_caused_by_learned_clauses))
            print("Number of unit propagations: " + str(cnf.number_of_unit_propagations))
            print("Number of unit propagations caused by learned clauses: " + str(cnf.number_of_unit_propagations_caused_by_learned_clauses))
            print("Number of restarts: " + str(cnf.number_of_restarts))

            log_Random_list[i].append((cdcl.time, 
                                       cdcl.number_of_decisions, 
                                       cdcl.number_of_steps_of_unit_propagation, 
                                       cnf.number_of_checked_clauses,
                                       cnf.number_of_deleted_learned_clauses,
                                       cnf.number_of_clause_deletions,
                                       cnf.number_of_contradictions,
                                       cnf.number_of_contradictions_caused_by_learned_clauses,
                                       cnf.number_of_unit_propagations,
                                       cnf.number_of_unit_propagations_caused_by_learned_clauses,
                                       cnf.number_of_restarts))

            print()

        # JeroslowWangOneSided
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.JeroslowWangOneSided,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - JeroslowWangOneSided")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - JeroslowWangOneSided")

        print("Time: " + str(cdcl.time))
        print("Number of decisions: " + str(cdcl.number_of_decisions))
        print("Number of steps of unit propagation: " + str(cdcl.number_of_steps_of_unit_propagation))
        print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))
        print("Number of deleted learned clauses: " + str(cnf.number_of_deleted_learned_clauses))
        print("Number of clause deletions: " + str(cnf.number_of_clause_deletions))
        print("Number of contradictions: " + str(cnf.number_of_contradictions))
        print("Number of contradictions caused by learned clauses: " + str(cnf.number_of_contradictions_caused_by_learned_clauses))
        print("Number of unit propagations: " + str(cnf.number_of_unit_propagations))
        print("Number of unit propagations caused by learned clauses: " + str(cnf.number_of_unit_propagations_caused_by_learned_clauses))
        print("Number of restarts: " + str(cnf.number_of_restarts))

        log_JeroslowWangOneSided_list[i].append((cdcl.time, 
                                                 cdcl.number_of_decisions, 
                                                 cdcl.number_of_steps_of_unit_propagation, 
                                                 cnf.number_of_checked_clauses,
                                                 cnf.number_of_deleted_learned_clauses,
                                                 cnf.number_of_clause_deletions,
                                                 cnf.number_of_contradictions,
                                                 cnf.number_of_contradictions_caused_by_learned_clauses,
                                                 cnf.number_of_unit_propagations,
                                                 cnf.number_of_unit_propagations_caused_by_learned_clauses,
                                                 cnf.number_of_restarts))

        print()

        # JeroslowWangTwoSided
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.JeroslowWangTwoSided,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - JeroslowWangTwoSided")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - JeroslowWangTwoSided")

        print("Time: " + str(cdcl.time))
        print("Number of decisions: " + str(cdcl.number_of_decisions))
        print("Number of steps of unit propagation: " + str(cdcl.number_of_steps_of_unit_propagation))
        print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))
        print("Number of deleted learned clauses: " + str(cnf.number_of_deleted_learned_clauses))
        print("Number of clause deletions: " + str(cnf.number_of_clause_deletions))
        print("Number of contradictions: " + str(cnf.number_of_contradictions))
        print("Number of contradictions caused by learned clauses: " + str(cnf.number_of_contradictions_caused_by_learned_clauses))
        print("Number of unit propagations: " + str(cnf.number_of_unit_propagations))
        print("Number of unit propagations caused by learned clauses: " + str(cnf.number_of_unit_propagations_caused_by_learned_clauses))
        print("Number of restarts: " + str(cnf.number_of_restarts))

        log_JeroslowWangTwoSided_list[i].append((cdcl.time, 
                                                 cdcl.number_of_decisions, 
                                                 cdcl.number_of_steps_of_unit_propagation, 
                                                 cnf.number_of_checked_clauses,
                                                 cnf.number_of_deleted_learned_clauses,
                                                 cnf.number_of_clause_deletions,
                                                 cnf.number_of_contradictions,
                                                 cnf.number_of_contradictions_caused_by_learned_clauses,
                                                 cnf.number_of_unit_propagations,
                                                 cnf.number_of_unit_propagations_caused_by_learned_clauses,
                                                 cnf.number_of_restarts))

        print()

        # JeroslowWangOneSidedDynamic
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.JeroslowWangOneSidedDynamic,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - JeroslowWangOneSidedDynamic")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - JeroslowWangOneSidedDynamic")

        print("Time: " + str(cdcl.time))
        print("Number of decisions: " + str(cdcl.number_of_decisions))
        print("Number of steps of unit propagation: " + str(cdcl.number_of_steps_of_unit_propagation))
        print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))
        print("Number of deleted learned clauses: " + str(cnf.number_of_deleted_learned_clauses))
        print("Number of clause deletions: " + str(cnf.number_of_clause_deletions))
        print("Number of contradictions: " + str(cnf.number_of_contradictions))
        print("Number of contradictions caused by learned clauses: " + str(cnf.number_of_contradictions_caused_by_learned_clauses))
        print("Number of unit propagations: " + str(cnf.number_of_unit_propagations))
        print("Number of unit propagations caused by learned clauses: " + str(cnf.number_of_unit_propagations_caused_by_learned_clauses))
        print("Number of restarts: " + str(cnf.number_of_restarts))

        log_JeroslowWangOneSidedDynamic_list[i].append((cdcl.time, 
                                                        cdcl.number_of_decisions, 
                                                        cdcl.number_of_steps_of_unit_propagation, 
                                                        cnf.number_of_checked_clauses,
                                                        cnf.number_of_deleted_learned_clauses,
                                                        cnf.number_of_clause_deletions,
                                                        cnf.number_of_contradictions,
                                                        cnf.number_of_contradictions_caused_by_learned_clauses,
                                                        cnf.number_of_unit_propagations,
                                                        cnf.number_of_unit_propagations_caused_by_learned_clauses,
                                                        cnf.number_of_restarts))

        print()

        # JeroslowWangTwoSidedDynamic
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.JeroslowWangTwoSidedDynamic,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - JeroslowWangTwoSidedDynamic")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - JeroslowWangTwoSidedDynamic")

        print("Time: " + str(cdcl.time))
        print("Number of decisions: " + str(cdcl.number_of_decisions))
        print("Number of steps of unit propagation: " + str(cdcl.number_of_steps_of_unit_propagation))
        print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))
        print("Number of deleted learned clauses: " + str(cnf.number_of_deleted_learned_clauses))
        print("Number of clause deletions: " + str(cnf.number_of_clause_deletions))
        print("Number of contradictions: " + str(cnf.number_of_contradictions))
        print("Number of contradictions caused by learned clauses: " + str(cnf.number_of_contradictions_caused_by_learned_clauses))
        print("Number of unit propagations: " + str(cnf.number_of_unit_propagations))
        print("Number of unit propagations caused by learned clauses: " + str(cnf.number_of_unit_propagations_caused_by_learned_clauses))
        print("Number of restarts: " + str(cnf.number_of_restarts))

        log_JeroslowWangTwoSidedDynamic_list[i].append((cdcl.time, 
                                                        cdcl.number_of_decisions, 
                                                        cdcl.number_of_steps_of_unit_propagation,
                                                        cnf.number_of_checked_clauses,
                                                        cnf.number_of_deleted_learned_clauses,
                                                        cnf.number_of_clause_deletions,
                                                        cnf.number_of_contradictions,
                                                        cnf.number_of_contradictions_caused_by_learned_clauses,
                                                        cnf.number_of_unit_propagations,
                                                        cnf.number_of_unit_propagations_caused_by_learned_clauses,
                                                        cnf.number_of_restarts))

        print()

        # VSIDS
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.VSIDS,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - VSIDS")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - VSIDS")

        print("Time: " + str(cdcl.time))
        print("Number of decisions: " + str(cdcl.number_of_decisions))
        print("Number of steps of unit propagation: " + str(cdcl.number_of_steps_of_unit_propagation))
        print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))
        print("Number of deleted learned clauses: " + str(cnf.number_of_deleted_learned_clauses))
        print("Number of clause deletions: " + str(cnf.number_of_clause_deletions))
        print("Number of contradictions: " + str(cnf.number_of_contradictions))
        print("Number of contradictions caused by learned clauses: " + str(cnf.number_of_contradictions_caused_by_learned_clauses))
        print("Number of unit propagations: " + str(cnf.number_of_unit_propagations))
        print("Number of unit propagations caused by learned clauses: " + str(cnf.number_of_unit_propagations_caused_by_learned_clauses))
        print("Number of restarts: " + str(cnf.number_of_restarts))
        print("Number of decay: " + str(cnf.number_of_decay))

        log_VSIDS_list[i].append((cdcl.time, 
                                  cdcl.number_of_decisions, 
                                  cdcl.number_of_steps_of_unit_propagation,
                                  cnf.number_of_checked_clauses,
                                  cnf.number_of_deleted_learned_clauses,
                                  cnf.number_of_clause_deletions,
                                  cnf.number_of_contradictions,
                                  cnf.number_of_contradictions_caused_by_learned_clauses,
                                  cnf.number_of_unit_propagations,
                                  cnf.number_of_unit_propagations_caused_by_learned_clauses,
                                  cnf.number_of_restarts,
                                  cnf.number_of_decay))

        print()

        # eVSIDS
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.eVSIDS,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - eVSIDS")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - eVSIDS")

        print("Time: " + str(cdcl.time))
        print("Number of decisions: " + str(cdcl.number_of_decisions))
        print("Number of steps of unit propagation: " + str(cdcl.number_of_steps_of_unit_propagation))
        print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))
        print("Number of deleted learned clauses: " + str(cnf.number_of_deleted_learned_clauses))
        print("Number of clause deletions: " + str(cnf.number_of_clause_deletions))
        print("Number of contradictions: " + str(cnf.number_of_contradictions))
        print("Number of contradictions caused by learned clauses: " + str(cnf.number_of_contradictions_caused_by_learned_clauses))
        print("Number of unit propagations: " + str(cnf.number_of_unit_propagations))
        print("Number of unit propagations caused by learned clauses: " + str(cnf.number_of_unit_propagations_caused_by_learned_clauses))
        print("Number of restarts: " + str(cnf.number_of_restarts))
        print("Number of decay: " + str(cnf.number_of_decay))

        log_eVSIDS_list[i].append((cdcl.time, 
                                  cdcl.number_of_decisions, 
                                  cdcl.number_of_steps_of_unit_propagation,
                                  cnf.number_of_checked_clauses,
                                  cnf.number_of_deleted_learned_clauses,
                                  cnf.number_of_clause_deletions,
                                  cnf.number_of_contradictions,
                                  cnf.number_of_contradictions_caused_by_learned_clauses,
                                  cnf.number_of_unit_propagations,
                                  cnf.number_of_unit_propagations_caused_by_learned_clauses,
                                  cnf.number_of_restarts,
                                  cnf.number_of_decay))

# Log Random
if (use_random):
    time_y_Random = []
    number_of_decisions_y_Random = []
    number_of_steps_of_unit_propagation_y_Random = []
    number_of_checked_clauses_y_Random = []
    number_of_deleted_learned_clauses_y_Random = []
    number_of_clause_deletions_y_Random = []
    number_of_contradiction_y_Random = []
    number_of_contradictions_caused_by_learned_clauses_y_Random = []
    number_of_unit_propagations_y_Random = []
    number_of_unit_propagations_caused_by_learned_clauses_y_Random = []
    number_of_restarts_y_Random = []

    for i in range(len(log_Random_list)):
        time_average = 0
        number_of_decisions_average = 0
        number_of_steps_of_unit_propagation_average = 0
        number_of_checked_clauses_average = 0
        number_of_deleted_learned_clauses_average = 0
        number_of_clause_deletions_average = 0
        number_of_contradiction_average = 0
        number_of_contradictions_caused_by_learned_clauses_average = 0
        number_of_unit_propagations_average = 0
        number_of_unit_propagations_caused_by_learned_clauses_average = 0
        number_of_restarts_average = 0

        for j in range(len(log_Random_list[i])):
            time_average += log_Random_list[i][j][0]
            number_of_decisions_average += log_Random_list[i][j][1]
            number_of_steps_of_unit_propagation_average += log_Random_list[i][j][2]
            number_of_checked_clauses_average += log_Random_list[i][j][3]
            number_of_deleted_learned_clauses_average += log_Random_list[i][j][4]
            number_of_clause_deletions_average += log_Random_list[i][j][5]
            number_of_contradiction_average += log_Random_list[i][j][6]
            number_of_contradictions_caused_by_learned_clauses_average += log_Random_list[i][j][7]
            number_of_unit_propagations_average += log_Random_list[i][j][8]
            number_of_unit_propagations_caused_by_learned_clauses_average += log_Random_list[i][j][9]
            number_of_restarts_average += log_Random_list[i][j][10]
        size = len(log_Random_list[i])
        if (size != 0):
            time_average /= size
            number_of_decisions_average /= size
            number_of_steps_of_unit_propagation_average /= size
            number_of_checked_clauses_average /= size
            number_of_deleted_learned_clauses_average /= size
            number_of_clause_deletions_average /= size
            number_of_contradiction_average /= size
            number_of_contradictions_caused_by_learned_clauses_average /= size
            number_of_unit_propagations_average /= size
            number_of_unit_propagations_caused_by_learned_clauses_average /= size
            number_of_restarts_average /= size

        time_y_Random.append(time_average)
        number_of_decisions_y_Random.append(number_of_decisions_average)
        number_of_steps_of_unit_propagation_y_Random.append(number_of_steps_of_unit_propagation_average)
        number_of_checked_clauses_y_Random.append(number_of_checked_clauses_average)
        number_of_deleted_learned_clauses_y_Random.append(number_of_deleted_learned_clauses_average)
        number_of_clause_deletions_y_Random.append(number_of_clause_deletions_average)
        number_of_contradiction_y_Random.append(number_of_contradiction_average)
        number_of_contradictions_caused_by_learned_clauses_y_Random.append(number_of_contradictions_caused_by_learned_clauses_average)
        number_of_unit_propagations_y_Random.append(number_of_unit_propagations_average)
        number_of_unit_propagations_caused_by_learned_clauses_y_Random.append(number_of_unit_propagations_caused_by_learned_clauses_average)
        number_of_restarts_y_Random.append(number_of_restarts_average)

# Log JeroslowWangOneSided
time_y_JeroslowWangOneSided = []
number_of_decisions_y_JeroslowWangOneSided = []
number_of_steps_of_unit_propagation_y_JeroslowWangOneSided = []
number_of_checked_clauses_y_JeroslowWangOneSided = []
number_of_deleted_learned_clauses_y_JeroslowWangOneSided = []
number_of_clause_deletions_y_JeroslowWangOneSided = []
number_of_contradiction_y_JeroslowWangOneSided = []
number_of_contradictions_caused_by_learned_clauses_y_JeroslowWangOneSided = []
number_of_unit_propagations_y_JeroslowWangOneSided = []
number_of_unit_propagations_caused_by_learned_clauses_y_JeroslowWangOneSided = []
number_of_restarts_y_JeroslowWangOneSided = []

for i in range(len(log_JeroslowWangOneSided_list)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0
    number_of_deleted_learned_clauses_average = 0
    number_of_clause_deletions_average = 0
    number_of_contradiction_average = 0
    number_of_contradictions_caused_by_learned_clauses_average = 0
    number_of_unit_propagations_average = 0
    number_of_unit_propagations_caused_by_learned_clauses_average = 0
    number_of_restarts_average = 0

    for j in range(len(log_JeroslowWangOneSided_list[i])):
        time_average += log_JeroslowWangOneSided_list[i][j][0]
        number_of_decisions_average += log_JeroslowWangOneSided_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_JeroslowWangOneSided_list[i][j][2]
        number_of_checked_clauses_average += log_JeroslowWangOneSided_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_JeroslowWangOneSided_list[i][j][4]
        number_of_clause_deletions_average += log_JeroslowWangOneSided_list[i][j][5]
        number_of_contradiction_average += log_JeroslowWangOneSided_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_JeroslowWangOneSided_list[i][j][7]
        number_of_unit_propagations_average += log_JeroslowWangOneSided_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_JeroslowWangOneSided_list[i][j][9]
        number_of_restarts_average += log_JeroslowWangOneSided_list[i][j][10]
    size = len(log_JeroslowWangOneSided_list[i])
    if (size != 0):
        time_average /= size
        number_of_decisions_average /= size
        number_of_steps_of_unit_propagation_average /= size
        number_of_checked_clauses_average /= size
        number_of_deleted_learned_clauses_average /= size
        number_of_clause_deletions_average /= size
        number_of_contradiction_average /= size
        number_of_contradictions_caused_by_learned_clauses_average /= size
        number_of_unit_propagations_average /= size
        number_of_unit_propagations_caused_by_learned_clauses_average /= size
        number_of_restarts_average /= size

    time_y_JeroslowWangOneSided.append(time_average)
    number_of_decisions_y_JeroslowWangOneSided.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_JeroslowWangOneSided.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_JeroslowWangOneSided.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_JeroslowWangOneSided.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_JeroslowWangOneSided.append(number_of_clause_deletions_average)
    number_of_contradiction_y_JeroslowWangOneSided.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_JeroslowWangOneSided.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_JeroslowWangOneSided.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_JeroslowWangOneSided.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_JeroslowWangOneSided.append(number_of_restarts_average)

# Log JeroslowWangTwoSided
time_y_JeroslowWangTwoSided = []
number_of_decisions_y_JeroslowWangTwoSided = []
number_of_steps_of_unit_propagation_y_JeroslowWangTwoSided = []
number_of_checked_clauses_y_JeroslowWangTwoSided = []
number_of_deleted_learned_clauses_y_JeroslowWangTwoSided = []
number_of_clause_deletions_y_JeroslowWangTwoSided = []
number_of_contradiction_y_JeroslowWangTwoSided = []
number_of_contradictions_caused_by_learned_clauses_y_JeroslowWangTwoSided = []
number_of_unit_propagations_y_JeroslowWangTwoSided = []
number_of_unit_propagations_caused_by_learned_clauses_y_JeroslowWangTwoSided = []
number_of_restarts_y_JeroslowWangTwoSided = []

for i in range(len(log_JeroslowWangTwoSided_list)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0
    number_of_deleted_learned_clauses_average = 0
    number_of_clause_deletions_average = 0
    number_of_contradiction_average = 0
    number_of_contradictions_caused_by_learned_clauses_average = 0
    number_of_unit_propagations_average = 0
    number_of_unit_propagations_caused_by_learned_clauses_average = 0
    number_of_restarts_average = 0

    for j in range(len(log_JeroslowWangTwoSided_list[i])):
        time_average += log_JeroslowWangTwoSided_list[i][j][0]
        number_of_decisions_average += log_JeroslowWangTwoSided_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_JeroslowWangTwoSided_list[i][j][2]
        number_of_checked_clauses_average += log_JeroslowWangTwoSided_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_JeroslowWangTwoSided_list[i][j][4]
        number_of_clause_deletions_average += log_JeroslowWangTwoSided_list[i][j][5]
        number_of_contradiction_average += log_JeroslowWangTwoSided_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_JeroslowWangTwoSided_list[i][j][7]
        number_of_unit_propagations_average += log_JeroslowWangTwoSided_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_JeroslowWangTwoSided_list[i][j][9]
        number_of_restarts_average += log_JeroslowWangTwoSided_list[i][j][10]
    size = len(log_JeroslowWangTwoSided_list[i])
    if (size != 0):
        time_average /= size
        number_of_decisions_average /= size
        number_of_steps_of_unit_propagation_average /= size
        number_of_checked_clauses_average /= size
        number_of_deleted_learned_clauses_average /= size
        number_of_clause_deletions_average /= size
        number_of_contradiction_average /= size
        number_of_contradictions_caused_by_learned_clauses_average /= size
        number_of_unit_propagations_average /= size
        number_of_unit_propagations_caused_by_learned_clauses_average /= size
        number_of_restarts_average /= size

    time_y_JeroslowWangTwoSided.append(time_average)
    number_of_decisions_y_JeroslowWangTwoSided.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_JeroslowWangTwoSided.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_JeroslowWangTwoSided.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_JeroslowWangTwoSided.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_JeroslowWangTwoSided.append(number_of_clause_deletions_average)
    number_of_contradiction_y_JeroslowWangTwoSided.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_JeroslowWangTwoSided.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_JeroslowWangTwoSided.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_JeroslowWangTwoSided.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_JeroslowWangTwoSided.append(number_of_restarts_average)

# Log JeroslowWangOneSidedDynamic
time_y_JeroslowWangOneSidedDynamic = []
number_of_decisions_y_JeroslowWangOneSidedDynamic = []
number_of_steps_of_unit_propagation_y_JeroslowWangOneSidedDynamic = []
number_of_checked_clauses_y_JeroslowWangOneSidedDynamic = []
number_of_deleted_learned_clauses_y_JeroslowWangOneSidedDynamic = []
number_of_clause_deletions_y_JeroslowWangOneSidedDynamic = []
number_of_contradiction_y_JeroslowWangOneSidedDynamic = []
number_of_contradictions_caused_by_learned_clauses_y_JeroslowWangOneSidedDynamic = []
number_of_unit_propagations_y_JeroslowWangOneSidedDynamic = []
number_of_unit_propagations_caused_by_learned_clauses_y_JeroslowWangOneSidedDynamic = []
number_of_restarts_y_JeroslowWangOneSidedDynamic = []

for i in range(len(log_JeroslowWangOneSidedDynamic_list)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0
    number_of_deleted_learned_clauses_average = 0
    number_of_clause_deletions_average = 0
    number_of_contradiction_average = 0
    number_of_contradictions_caused_by_learned_clauses_average = 0
    number_of_unit_propagations_average = 0
    number_of_unit_propagations_caused_by_learned_clauses_average = 0
    number_of_restarts_average = 0

    for j in range(len(log_JeroslowWangOneSidedDynamic_list[i])):
        time_average += log_JeroslowWangOneSidedDynamic_list[i][j][0]
        number_of_decisions_average += log_JeroslowWangOneSidedDynamic_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_JeroslowWangOneSidedDynamic_list[i][j][2]
        number_of_checked_clauses_average += log_JeroslowWangOneSidedDynamic_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_JeroslowWangOneSidedDynamic_list[i][j][4]
        number_of_clause_deletions_average += log_JeroslowWangOneSidedDynamic_list[i][j][5]
        number_of_contradiction_average += log_JeroslowWangOneSidedDynamic_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_JeroslowWangOneSidedDynamic_list[i][j][7]
        number_of_unit_propagations_average += log_JeroslowWangOneSidedDynamic_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_JeroslowWangOneSidedDynamic_list[i][j][9]
        number_of_restarts_average += log_JeroslowWangOneSidedDynamic_list[i][j][10]
    size = len(log_JeroslowWangOneSidedDynamic_list[i])
    if (size != 0):
        time_average /= size
        number_of_decisions_average /= size
        number_of_steps_of_unit_propagation_average /= size
        number_of_checked_clauses_average /= size
        number_of_deleted_learned_clauses_average /= size
        number_of_clause_deletions_average /= size
        number_of_contradiction_average /= size
        number_of_contradictions_caused_by_learned_clauses_average /= size
        number_of_unit_propagations_average /= size
        number_of_unit_propagations_caused_by_learned_clauses_average /= size
        number_of_restarts_average /= size

    time_y_JeroslowWangOneSidedDynamic.append(time_average)
    number_of_decisions_y_JeroslowWangOneSidedDynamic.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_JeroslowWangOneSidedDynamic.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_JeroslowWangOneSidedDynamic.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_JeroslowWangOneSidedDynamic.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_JeroslowWangOneSidedDynamic.append(number_of_clause_deletions_average)
    number_of_contradiction_y_JeroslowWangOneSidedDynamic.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_JeroslowWangOneSidedDynamic.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_JeroslowWangOneSidedDynamic.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_JeroslowWangOneSidedDynamic.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_JeroslowWangOneSidedDynamic.append(number_of_restarts_average)

# Log JeroslowWangTwoSidedDynamic
time_y_JeroslowWangTwoSidedDynamic = []
number_of_decisions_y_JeroslowWangTwoSidedDynamic = []
number_of_steps_of_unit_propagation_y_JeroslowWangTwoSidedDynamic = []
number_of_checked_clauses_y_JeroslowWangTwoSidedDynamic = []
number_of_deleted_learned_clauses_y_JeroslowWangTwoSidedDynamic = []
number_of_clause_deletions_y_JeroslowWangTwoSidedDynamic = []
number_of_contradiction_y_JeroslowWangTwoSidedDynamic = []
number_of_contradictions_caused_by_learned_clauses_y_JeroslowWangTwoSidedDynamic = []
number_of_unit_propagations_y_JeroslowWangTwoSidedDynamic = []
number_of_unit_propagations_caused_by_learned_clauses_y_JeroslowWangTwoSidedDynamic = []
number_of_restarts_y_JeroslowWangTwoSidedDynamic = []

for i in range(len(log_JeroslowWangTwoSidedDynamic_list)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0
    number_of_deleted_learned_clauses_average = 0
    number_of_clause_deletions_average = 0
    number_of_contradiction_average = 0
    number_of_contradictions_caused_by_learned_clauses_average = 0
    number_of_unit_propagations_average = 0
    number_of_unit_propagations_caused_by_learned_clauses_average = 0
    number_of_restarts_average = 0

    for j in range(len(log_JeroslowWangTwoSidedDynamic_list[i])):
        time_average += log_JeroslowWangTwoSidedDynamic_list[i][j][0]
        number_of_decisions_average += log_JeroslowWangTwoSidedDynamic_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_JeroslowWangTwoSidedDynamic_list[i][j][2]
        number_of_checked_clauses_average += log_JeroslowWangTwoSidedDynamic_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_JeroslowWangTwoSidedDynamic_list[i][j][4]
        number_of_clause_deletions_average += log_JeroslowWangTwoSidedDynamic_list[i][j][5]
        number_of_contradiction_average += log_JeroslowWangTwoSidedDynamic_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_JeroslowWangTwoSidedDynamic_list[i][j][7]
        number_of_unit_propagations_average += log_JeroslowWangTwoSidedDynamic_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_JeroslowWangTwoSidedDynamic_list[i][j][9]
        number_of_restarts_average += log_JeroslowWangTwoSidedDynamic_list[i][j][10]
    size = len(log_JeroslowWangTwoSidedDynamic_list[i])
    if (size != 0):
        time_average /= size
        number_of_decisions_average /= size
        number_of_steps_of_unit_propagation_average /= size
        number_of_checked_clauses_average /= size
        number_of_deleted_learned_clauses_average /= size
        number_of_clause_deletions_average /= size
        number_of_contradiction_average /= size
        number_of_contradictions_caused_by_learned_clauses_average /= size
        number_of_unit_propagations_average /= size
        number_of_unit_propagations_caused_by_learned_clauses_average /= size
        number_of_restarts_average /= size

    time_y_JeroslowWangTwoSidedDynamic.append(time_average)
    number_of_decisions_y_JeroslowWangTwoSidedDynamic.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_JeroslowWangTwoSidedDynamic.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_JeroslowWangTwoSidedDynamic.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_JeroslowWangTwoSidedDynamic.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_JeroslowWangTwoSidedDynamic.append(number_of_clause_deletions_average)
    number_of_contradiction_y_JeroslowWangTwoSidedDynamic.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_JeroslowWangTwoSidedDynamic.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_JeroslowWangTwoSidedDynamic.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_JeroslowWangTwoSidedDynamic.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_JeroslowWangTwoSidedDynamic.append(number_of_restarts_average)

# Log VSIDS
time_y_VSIDS = []
number_of_decisions_y_VSIDS = []
number_of_steps_of_unit_propagation_y_VSIDS = []
number_of_checked_clauses_y_VSIDS = []
number_of_deleted_learned_clauses_y_VSIDS = []
number_of_clause_deletions_y_VSIDS = []
number_of_contradiction_y_VSIDS = []
number_of_contradictions_caused_by_learned_clauses_y_VSIDS = []
number_of_unit_propagations_y_VSIDS = []
number_of_unit_propagations_caused_by_learned_clauses_y_VSIDS = []
number_of_restarts_y_VSIDS = []
number_of_decay_y_VSIDS = []

for i in range(len(log_VSIDS_list)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0
    number_of_deleted_learned_clauses_average = 0
    number_of_clause_deletions_average = 0
    number_of_contradiction_average = 0
    number_of_contradictions_caused_by_learned_clauses_average = 0
    number_of_unit_propagations_average = 0
    number_of_unit_propagations_caused_by_learned_clauses_average = 0
    number_of_restarts_average = 0
    number_of_decay_average = 0

    for j in range(len(log_VSIDS_list[i])):
        time_average += log_VSIDS_list[i][j][0]
        number_of_decisions_average += log_VSIDS_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_VSIDS_list[i][j][2]
        number_of_checked_clauses_average += log_VSIDS_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_VSIDS_list[i][j][4]
        number_of_clause_deletions_average += log_VSIDS_list[i][j][5]
        number_of_contradiction_average += log_VSIDS_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_VSIDS_list[i][j][7]
        number_of_unit_propagations_average += log_VSIDS_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_VSIDS_list[i][j][9]
        number_of_restarts_average += log_VSIDS_list[i][j][10]
        number_of_decay_average += log_VSIDS_list[i][j][11]
    size = len(log_VSIDS_list[i])
    if (size != 0):
        time_average /= size
        number_of_decisions_average /= size
        number_of_steps_of_unit_propagation_average /= size
        number_of_checked_clauses_average /= size
        number_of_deleted_learned_clauses_average /= size
        number_of_clause_deletions_average /= size
        number_of_contradiction_average /= size
        number_of_contradictions_caused_by_learned_clauses_average /= size
        number_of_unit_propagations_average /= size
        number_of_unit_propagations_caused_by_learned_clauses_average /= size
        number_of_restarts_average /= size
        number_of_decay_average /= size

    time_y_VSIDS.append(time_average)
    number_of_decisions_y_VSIDS.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_VSIDS.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_VSIDS.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_VSIDS.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_VSIDS.append(number_of_clause_deletions_average)
    number_of_contradiction_y_VSIDS.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_VSIDS.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_VSIDS.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_VSIDS.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_VSIDS.append(number_of_restarts_average)
    number_of_decay_y_VSIDS.append(number_of_decay_average)

# Log eVSIDS
time_y_eVSIDS = []
number_of_decisions_y_eVSIDS = []
number_of_steps_of_unit_propagation_y_eVSIDS = []
number_of_checked_clauses_y_eVSIDS = []
number_of_deleted_learned_clauses_y_eVSIDS = []
number_of_clause_deletions_y_eVSIDS = []
number_of_contradiction_y_eVSIDS = []
number_of_contradictions_caused_by_learned_clauses_y_eVSIDS = []
number_of_unit_propagations_y_eVSIDS = []
number_of_unit_propagations_caused_by_learned_clauses_y_eVSIDS = []
number_of_restarts_y_eVSIDS = []
number_of_decay_y_eVSIDS = []

for i in range(len(log_eVSIDS_list)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0
    number_of_deleted_learned_clauses_average = 0
    number_of_clause_deletions_average = 0
    number_of_contradiction_average = 0
    number_of_contradictions_caused_by_learned_clauses_average = 0
    number_of_unit_propagations_average = 0
    number_of_unit_propagations_caused_by_learned_clauses_average = 0
    number_of_restarts_average = 0
    number_of_decay_average = 0

    for j in range(len(log_eVSIDS_list[i])):
        time_average += log_eVSIDS_list[i][j][0]
        number_of_decisions_average += log_eVSIDS_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_eVSIDS_list[i][j][2]
        number_of_checked_clauses_average += log_eVSIDS_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_eVSIDS_list[i][j][4]
        number_of_clause_deletions_average += log_eVSIDS_list[i][j][5]
        number_of_contradiction_average += log_eVSIDS_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_eVSIDS_list[i][j][7]
        number_of_unit_propagations_average += log_eVSIDS_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_eVSIDS_list[i][j][9]
        number_of_restarts_average += log_eVSIDS_list[i][j][10]
        number_of_decay_average += log_eVSIDS_list[i][j][11]
    size = len(log_eVSIDS_list[i])
    if (size != 0):
        time_average /= size
        number_of_decisions_average /= size
        number_of_steps_of_unit_propagation_average /= size
        number_of_checked_clauses_average /= size
        number_of_deleted_learned_clauses_average /= size
        number_of_clause_deletions_average /= size
        number_of_contradiction_average /= size
        number_of_contradictions_caused_by_learned_clauses_average /= size
        number_of_unit_propagations_average /= size
        number_of_unit_propagations_caused_by_learned_clauses_average /= size
        number_of_restarts_average /= size
        number_of_decay_average /= size

    time_y_eVSIDS.append(time_average)
    number_of_decisions_y_eVSIDS.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_eVSIDS.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_eVSIDS.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_eVSIDS.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_eVSIDS.append(number_of_clause_deletions_average)
    number_of_contradiction_y_eVSIDS.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_eVSIDS.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_eVSIDS.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_eVSIDS.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_eVSIDS.append(number_of_restarts_average)
    number_of_decay_y_eVSIDS.append(number_of_decay_average)

if (use_random):
    print("Random")
    print("Time: ")
    print(time_y_Random)
    print("Number of decisions: ")
    print(number_of_decisions_y_Random)
    print("Number of steps of unit propagation: ")
    print(number_of_steps_of_unit_propagation_y_Random)
    print("Number of checked clauses: ")
    print(number_of_checked_clauses_y_Random)
    print("Number of deleted learned clauses: ")
    print(number_of_deleted_learned_clauses_y_Random)
    print("Number of clause deletions: ")
    print(number_of_clause_deletions_y_Random)
    print("Number of contradictions: ")
    print(number_of_contradiction_y_Random)
    print("Number of contradictions caused by learned clauses: ")
    print(number_of_contradictions_caused_by_learned_clauses_y_Random)
    print("Number of unit propagations: ")
    print(number_of_unit_propagations_y_Random)
    print("Number of unit propagations caused by learned clauses: ")
    print(number_of_unit_propagations_caused_by_learned_clauses_y_Random)
    print("Number of restarts: ")
    print(number_of_restarts_y_Random)

print()

print("JeroslowWangOneSided")
print("Time: ")
print(time_y_JeroslowWangOneSided)
print("Number of decisions: ")
print(number_of_decisions_y_JeroslowWangOneSided)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_JeroslowWangOneSided)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_JeroslowWangOneSided)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_JeroslowWangOneSided)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_JeroslowWangOneSided)
print("Number of contradictions: ")
print(number_of_contradiction_y_JeroslowWangOneSided)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_JeroslowWangOneSided)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_JeroslowWangOneSided)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_JeroslowWangOneSided)
print("Number of restarts: ")
print(number_of_restarts_y_JeroslowWangOneSided)

print()

print("JeroslowWangTwoSided")
print("Time: ")
print(time_y_JeroslowWangTwoSided)
print("Number of decisions: ")
print(number_of_decisions_y_JeroslowWangTwoSided)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_JeroslowWangTwoSided)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_JeroslowWangTwoSided)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_JeroslowWangTwoSided)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_JeroslowWangTwoSided)
print("Number of contradictions: ")
print(number_of_contradiction_y_JeroslowWangTwoSided)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_JeroslowWangTwoSided)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_JeroslowWangTwoSided)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_JeroslowWangTwoSided)
print("Number of restarts: ")
print(number_of_restarts_y_JeroslowWangTwoSided)

print()

print("JeroslowWangOneSidedDynamic")
print("Time: ")
print(time_y_JeroslowWangOneSidedDynamic)
print("Number of decisions: ")
print(number_of_decisions_y_JeroslowWangOneSidedDynamic)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_JeroslowWangOneSidedDynamic)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_JeroslowWangOneSidedDynamic)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_JeroslowWangOneSidedDynamic)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_JeroslowWangOneSidedDynamic)
print("Number of contradictions: ")
print(number_of_contradiction_y_JeroslowWangOneSidedDynamic)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_JeroslowWangOneSidedDynamic)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_JeroslowWangOneSidedDynamic)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_JeroslowWangOneSidedDynamic)
print("Number of restarts: ")
print(number_of_restarts_y_JeroslowWangOneSidedDynamic)

print()

print("JeroslowWangTwoSidedDynamic")
print("Time: ")
print(time_y_JeroslowWangTwoSidedDynamic)
print("Number of decisions: ")
print(number_of_decisions_y_JeroslowWangTwoSidedDynamic)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_JeroslowWangTwoSidedDynamic)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_JeroslowWangTwoSidedDynamic)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_JeroslowWangTwoSidedDynamic)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_JeroslowWangTwoSidedDynamic)
print("Number of contradictions: ")
print(number_of_contradiction_y_JeroslowWangTwoSidedDynamic)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_JeroslowWangTwoSidedDynamic)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_JeroslowWangTwoSidedDynamic)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_JeroslowWangTwoSidedDynamic)
print("Number of restarts: ")
print(number_of_restarts_y_JeroslowWangTwoSidedDynamic)

print()

print("VSIDS")
print("Time: ")
print(time_y_VSIDS)
print("Number of decisions: ")
print(number_of_decisions_y_VSIDS)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_VSIDS)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_VSIDS)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_VSIDS)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_VSIDS)
print("Number of contradictions: ")
print(number_of_contradiction_y_VSIDS)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_VSIDS)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_VSIDS)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_VSIDS)
print("Number of restarts: ")
print(number_of_restarts_y_VSIDS)
print("Number of decay: ")
print(number_of_decay_y_VSIDS)

print()

print("eVSIDS")
print("Time: ")
print(time_y_eVSIDS)
print("Number of decisions: ")
print(number_of_decisions_y_eVSIDS)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_eVSIDS)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_eVSIDS)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_eVSIDS)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_eVSIDS)
print("Number of contradictions: ")
print(number_of_contradiction_y_eVSIDS)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_eVSIDS)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_eVSIDS)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_eVSIDS)
print("Number of restarts: ")
print(number_of_restarts_y_eVSIDS)
print("Number of decay: ")
print(number_of_decay_y_eVSIDS)

# Time
if (use_random):
    plt.plot(x_axis_variables, time_y_Random, color="blue", label='Random')
plt.plot(x_axis_variables, time_y_JeroslowWangOneSided, color="red", label='JeroslowWangOneSided')
plt.plot(x_axis_variables, time_y_JeroslowWangTwoSided, color="green", label='JeroslowWangTwoSided')
plt.plot(x_axis_variables, time_y_JeroslowWangOneSidedDynamic, color="yellow", label='JeroslowWangOneSidedDynamic')
plt.plot(x_axis_variables, time_y_JeroslowWangTwoSidedDynamic, color="purple", label='JeroslowWangTwoSidedDynamic')
plt.plot(x_axis_variables, time_y_VSIDS, color="cyan", label='VSIDS')
plt.plot(x_axis_variables, time_y_eVSIDS, color="black", label='eVSIDS')
plt.title('Time')
plt.xlabel('Number of variables')
plt.ylabel('Time (s)')
plt.legend(loc="upper left")
plt.show()

# Number of checked clauses
if (use_random):
    plt.plot(x_axis_variables, number_of_decisions_y_Random, color="blue", label='Random')
plt.plot(x_axis_variables, number_of_decisions_y_JeroslowWangOneSided, color="red", label='JeroslowWangOneSided')
plt.plot(x_axis_variables, number_of_decisions_y_JeroslowWangTwoSided, color="green", label='JeroslowWangTwoSided')
plt.plot(x_axis_variables, number_of_decisions_y_JeroslowWangOneSidedDynamic, color="yellow", label='JeroslowWangOneSidedDynamic')
plt.plot(x_axis_variables, number_of_decisions_y_JeroslowWangTwoSidedDynamic, color="purple", label='JeroslowWangTwoSidedDynamic')
plt.plot(x_axis_variables, number_of_decisions_y_VSIDS, color="cyan", label='VSIDS')
plt.plot(x_axis_variables, number_of_decisions_y_eVSIDS, color="black", label='eVSIDS')
plt.title('Number of checked clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of checked clauses')
plt.legend(loc="upper left")
plt.show()

# Number of decisions
if (use_random):
    plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_Random, color="blue", label='Random')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_JeroslowWangOneSided, color="red", label='JeroslowWangOneSided')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_JeroslowWangTwoSided, color="green", label='JeroslowWangTwoSided')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_JeroslowWangOneSidedDynamic, color="yellow", label='JeroslowWangOneSidedDynamic')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_JeroslowWangTwoSidedDynamic, color="purple", label='JeroslowWangTwoSidedDynamic')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_VSIDS, color="cyan", label='VSIDS')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_eVSIDS, color="black", label='eVSIDS')
plt.title('Number of decisions')
plt.xlabel('Number of variables')
plt.ylabel('Number of decisions')
plt.legend(loc="upper left")
plt.show()

# Number of steps of unit propagation
if (use_random):
    plt.plot(x_axis_variables, number_of_checked_clauses_y_Random, color="blue", label='Random')
plt.plot(x_axis_variables, number_of_checked_clauses_y_JeroslowWangOneSided, color="red", label='JeroslowWangOneSided')
plt.plot(x_axis_variables, number_of_checked_clauses_y_JeroslowWangTwoSided, color="green", label='JeroslowWangTwoSided')
plt.plot(x_axis_variables, number_of_checked_clauses_y_JeroslowWangOneSidedDynamic, color="yellow", label='JeroslowWangOneSidedDynamic')
plt.plot(x_axis_variables, number_of_checked_clauses_y_JeroslowWangTwoSidedDynamic, color="purple", label='JeroslowWangTwoSidedDynamic')
plt.plot(x_axis_variables, number_of_checked_clauses_y_VSIDS, color="cyan", label='VSIDS')
plt.plot(x_axis_variables, number_of_checked_clauses_y_eVSIDS, color="black", label='eVSIDS')
plt.title('Number of steps of unit propagation')
plt.xlabel('Number of variables')
plt.ylabel('Number of steps of unit propagation')
plt.legend(loc="upper left")
plt.show()

# Number of deleted learned clauses
if (use_random):
    plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_Random, color="blue", label='Random')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_JeroslowWangOneSided, color="red", label='JeroslowWangOneSided')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_JeroslowWangTwoSided, color="green", label='JeroslowWangTwoSided')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_JeroslowWangOneSidedDynamic, color="yellow", label='JeroslowWangOneSidedDynamic')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_JeroslowWangTwoSidedDynamic, color="purple", label='JeroslowWangTwoSidedDynamic')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_VSIDS, color="cyan", label='VSIDS')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_eVSIDS, color="black", label='eVSIDS')
plt.title('Number of deleted learned clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of deleted learned clauses')
plt.legend(loc="upper left")
plt.show()

# Number of clause deletions
if (use_random):
    plt.plot(x_axis_variables, number_of_clause_deletions_y_Random, color="blue", label='Random')
plt.plot(x_axis_variables, number_of_clause_deletions_y_JeroslowWangOneSided, color="red", label='JeroslowWangOneSided')
plt.plot(x_axis_variables, number_of_clause_deletions_y_JeroslowWangTwoSided, color="green", label='JeroslowWangTwoSided')
plt.plot(x_axis_variables, number_of_clause_deletions_y_JeroslowWangOneSidedDynamic, color="yellow", label='JeroslowWangOneSidedDynamic')
plt.plot(x_axis_variables, number_of_clause_deletions_y_JeroslowWangTwoSidedDynamic, color="purple", label='JeroslowWangTwoSidedDynamic')
plt.plot(x_axis_variables, number_of_clause_deletions_y_VSIDS, color="cyan", label='VSIDS')
plt.plot(x_axis_variables, number_of_clause_deletions_y_eVSIDS, color="black", label='eVSIDS')
plt.title('Number of clause deletions')
plt.xlabel('Number of variables')
plt.ylabel('Number of clause deletions')
plt.legend(loc="upper left")
plt.show()