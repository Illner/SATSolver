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
dictionary_list = ["20-91", "50-218", "75-325", "100-430"]
x_axis_variables = [20, 50, 75, 100]
count_list = [1024, 256, 128, 64]

log_RemoveSubsumedClauses_list = []
log_KeepShortClauses_list = []
log_KeepActiveClauses_list = []
log_KeepActiveClauses2_list = []
log_KeepActiveClausesAndRemoveSubsumedClauses_list = []
log_KeepActiveClauses2AndRemoveSubsumedClauses_list = []
log_KeepShortClausesAndRemoveSubsumedClauses_list = []

for i in range(len(dictionary_list)):
    print("\n" + str(i))
    log_RemoveSubsumedClauses_list.append([])
    log_KeepShortClauses_list.append([])
    log_KeepActiveClauses_list.append([])
    log_KeepActiveClauses2_list.append([])
    log_KeepActiveClausesAndRemoveSubsumedClauses_list.append([])
    log_KeepActiveClauses2AndRemoveSubsumedClauses_list.append([])
    log_KeepShortClausesAndRemoveSubsumedClauses_list.append([])

    dictionary_path = os.path.join(path, dictionary_list[i])

    for j in range(count_list[i]):
        print("- "  + str(j))
        file = random.choice(os.listdir(dictionary_path))
        file_path = os.path.join(dictionary_path, file)

        print(file)

        is_sat = None
        if (file.startswith("uuf")):
            is_sat = False
            print("UNSAT")
        else:
            is_sat = True
            print("SAT")

        with open(file_path, "r") as input_file:
            input_formula = input_file.read()

        # RemoveSubsumedClauses
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.Random,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.RemoveSubsumedClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - RemoveSubsumedClauses")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - RemoveSubsumedClauses")

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

        log_RemoveSubsumedClauses_list[i].append((cdcl.time, 
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

        # KeepShortClauses
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.Random,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepShortClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - KeepShortClauses")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - KeepShortClauses")

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

        log_KeepShortClauses_list[i].append((cdcl.time, 
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

        # KeepActiveClauses
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
            raise MyException.SomethingWrongException("Invalid model - KeepActiveClauses")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - KeepActiveClauses")

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

        log_KeepActiveClauses_list[i].append((cdcl.time, 
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

        # KeepActiveClauses2
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.Random,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses2,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - KeepActiveClauses2")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - KeepActiveClauses2")

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

        log_KeepActiveClauses2_list[i].append((cdcl.time, 
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

        # KeepActiveClausesAndRemoveSubsumedClauses
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.Random,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClausesAndRemoveSubsumedClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - KeepActiveClausesAndRemoveSubsumedClauses")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - KeepActiveClausesAndRemoveSubsumedClauses")

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

        log_KeepActiveClausesAndRemoveSubsumedClauses_list[i].append((cdcl.time, 
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

        # KeepActiveClauses2AndRemoveSubsumedClauses
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.Random,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses2AndRemoveSubsumedClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - KeepActiveClauses2AndRemoveSubsumedClauses")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - KeepActiveClauses2AndRemoveSubsumedClauses")

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

        log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i].append((cdcl.time, 
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

        # KeepShortClausesAndRemoveSubsumedClauses
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.Random,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepShortClausesAndRemoveSubsumedClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - KeepShortClausesAndRemoveSubsumedClauses")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - KeepShortClausesAndRemoveSubsumedClauses")

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

        log_KeepShortClausesAndRemoveSubsumedClauses_list[i].append((cdcl.time, 
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

# Log RemoveSubsumedClauses
time_y_RemoveSubsumedClauses = []
number_of_decisions_y_RemoveSubsumedClauses = []
number_of_steps_of_unit_propagation_y_RemoveSubsumedClauses = []
number_of_checked_clauses_y_RemoveSubsumedClauses = []
number_of_deleted_learned_clauses_y_RemoveSubsumedClauses = []
number_of_clause_deletions_y_RemoveSubsumedClauses = []
number_of_contradiction_y_RemoveSubsumedClauses = []
number_of_contradictions_caused_by_learned_clauses_y_RemoveSubsumedClauses = []
number_of_unit_propagations_y_RemoveSubsumedClauses = []
number_of_unit_propagations_caused_by_learned_clauses_y_RemoveSubsumedClauses = []
number_of_restarts_y_RemoveSubsumedClauses = []

for i in range(len(log_RemoveSubsumedClauses_list)):
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

    for j in range(len(log_RemoveSubsumedClauses_list[i])):
        time_average += log_RemoveSubsumedClauses_list[i][j][0]
        number_of_decisions_average += log_RemoveSubsumedClauses_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_RemoveSubsumedClauses_list[i][j][2]
        number_of_checked_clauses_average += log_RemoveSubsumedClauses_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_RemoveSubsumedClauses_list[i][j][4]
        number_of_clause_deletions_average += log_RemoveSubsumedClauses_list[i][j][5]
        number_of_contradiction_average += log_RemoveSubsumedClauses_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_RemoveSubsumedClauses_list[i][j][7]
        number_of_unit_propagations_average += log_RemoveSubsumedClauses_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_RemoveSubsumedClauses_list[i][j][9]
        number_of_restarts_average += log_RemoveSubsumedClauses_list[i][j][10]
    size = len(log_RemoveSubsumedClauses_list[i])
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

    time_y_RemoveSubsumedClauses.append(time_average)
    number_of_decisions_y_RemoveSubsumedClauses.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_RemoveSubsumedClauses.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_RemoveSubsumedClauses.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_RemoveSubsumedClauses.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_RemoveSubsumedClauses.append(number_of_clause_deletions_average)
    number_of_contradiction_y_RemoveSubsumedClauses.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_RemoveSubsumedClauses.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_RemoveSubsumedClauses.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_RemoveSubsumedClauses.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_RemoveSubsumedClauses.append(number_of_restarts_average)

# Log KeepShortClauses
time_y_KeepShortClauses = []
number_of_decisions_y_KeepShortClauses = []
number_of_steps_of_unit_propagation_y_KeepShortClauses = []
number_of_checked_clauses_y_KeepShortClauses = []
number_of_deleted_learned_clauses_y_KeepShortClauses = []
number_of_clause_deletions_y_KeepShortClauses = []
number_of_contradiction_y_KeepShortClauses = []
number_of_contradictions_caused_by_learned_clauses_y_KeepShortClauses = []
number_of_unit_propagations_y_KeepShortClauses = []
number_of_unit_propagations_caused_by_learned_clauses_y_KeepShortClauses = []
number_of_restarts_y_KeepShortClauses = []

for i in range(len(log_KeepShortClauses_list)):
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

    for j in range(len(log_KeepShortClauses_list[i])):
        time_average += log_KeepShortClauses_list[i][j][0]
        number_of_decisions_average += log_KeepShortClauses_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_KeepShortClauses_list[i][j][2]
        number_of_checked_clauses_average += log_KeepShortClauses_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_KeepShortClauses_list[i][j][4]
        number_of_clause_deletions_average += log_KeepShortClauses_list[i][j][5]
        number_of_contradiction_average += log_KeepShortClauses_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_KeepShortClauses_list[i][j][7]
        number_of_unit_propagations_average += log_KeepShortClauses_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_KeepShortClauses_list[i][j][9]
        number_of_restarts_average += log_KeepShortClauses_list[i][j][10]
    size = len(log_KeepShortClauses_list[i])
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

    time_y_KeepShortClauses.append(time_average)
    number_of_decisions_y_KeepShortClauses.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_KeepShortClauses.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_KeepShortClauses.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_KeepShortClauses.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_KeepShortClauses.append(number_of_clause_deletions_average)
    number_of_contradiction_y_KeepShortClauses.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_KeepShortClauses.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_KeepShortClauses.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_KeepShortClauses.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_KeepShortClauses.append(number_of_restarts_average)

# Log KeepActiveClauses
time_y_KeepActiveClauses = []
number_of_decisions_y_KeepActiveClauses = []
number_of_steps_of_unit_propagation_y_KeepActiveClauses = []
number_of_checked_clauses_y_KeepActiveClauses = []
number_of_deleted_learned_clauses_y_KeepActiveClauses = []
number_of_clause_deletions_y_KeepActiveClauses = []
number_of_contradiction_y_KeepActiveClauses = []
number_of_contradictions_caused_by_learned_clauses_y_KeepActiveClauses = []
number_of_unit_propagations_y_KeepActiveClauses = []
number_of_unit_propagations_caused_by_learned_clauses_y_KeepActiveClauses = []
number_of_restarts_y_KeepActiveClauses = []

for i in range(len(log_KeepActiveClauses_list)):
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

    for j in range(len(log_KeepActiveClauses_list[i])):
        time_average += log_KeepActiveClauses_list[i][j][0]
        number_of_decisions_average += log_KeepActiveClauses_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_KeepActiveClauses_list[i][j][2]
        number_of_checked_clauses_average += log_KeepActiveClauses_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_KeepActiveClauses_list[i][j][4]
        number_of_clause_deletions_average += log_KeepActiveClauses_list[i][j][5]
        number_of_contradiction_average += log_KeepActiveClauses_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_KeepActiveClauses_list[i][j][7]
        number_of_unit_propagations_average += log_KeepActiveClauses_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_KeepActiveClauses_list[i][j][9]
        number_of_restarts_average += log_KeepActiveClauses_list[i][j][10]
    size = len(log_KeepActiveClauses_list[i])
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

    time_y_KeepActiveClauses.append(time_average)
    number_of_decisions_y_KeepActiveClauses.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_KeepActiveClauses.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_KeepActiveClauses.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_KeepActiveClauses.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_KeepActiveClauses.append(number_of_clause_deletions_average)
    number_of_contradiction_y_KeepActiveClauses.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_KeepActiveClauses.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_KeepActiveClauses.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_KeepActiveClauses.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_KeepActiveClauses.append(number_of_restarts_average)

# Log KeepActiveClauses2
time_y_KeepActiveClauses2 = []
number_of_decisions_y_KeepActiveClauses2 = []
number_of_steps_of_unit_propagation_y_KeepActiveClauses2 = []
number_of_checked_clauses_y_KeepActiveClauses2 = []
number_of_deleted_learned_clauses_y_KeepActiveClauses2 = []
number_of_clause_deletions_y_KeepActiveClauses2 = []
number_of_contradiction_y_KeepActiveClauses2 = []
number_of_contradictions_caused_by_learned_clauses_y_KeepActiveClauses2 = []
number_of_unit_propagations_y_KeepActiveClauses2 = []
number_of_unit_propagations_caused_by_learned_clauses_y_KeepActiveClauses2 = []
number_of_restarts_y_KeepActiveClauses2 = []

for i in range(len(log_KeepActiveClauses2_list)):
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

    for j in range(len(log_KeepActiveClauses2_list[i])):
        time_average += log_KeepActiveClauses2_list[i][j][0]
        number_of_decisions_average += log_KeepActiveClauses2_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_KeepActiveClauses2_list[i][j][2]
        number_of_checked_clauses_average += log_KeepActiveClauses2_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_KeepActiveClauses2_list[i][j][4]
        number_of_clause_deletions_average += log_KeepActiveClauses2_list[i][j][5]
        number_of_contradiction_average += log_KeepActiveClauses2_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_KeepActiveClauses2_list[i][j][7]
        number_of_unit_propagations_average += log_KeepActiveClauses2_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_KeepActiveClauses2_list[i][j][9]
        number_of_restarts_average += log_KeepActiveClauses2_list[i][j][10]
    size = len(log_KeepActiveClauses2_list[i])
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

    time_y_KeepActiveClauses2.append(time_average)
    number_of_decisions_y_KeepActiveClauses2.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_KeepActiveClauses2.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_KeepActiveClauses2.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_KeepActiveClauses2.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_KeepActiveClauses2.append(number_of_clause_deletions_average)
    number_of_contradiction_y_KeepActiveClauses2.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_KeepActiveClauses2.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_KeepActiveClauses2.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_KeepActiveClauses2.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_KeepActiveClauses2.append(number_of_restarts_average)

# Log KeepActiveClausesAndRemoveSubsumedClauses
time_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_decisions_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_steps_of_unit_propagation_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_checked_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_deleted_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_clause_deletions_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_contradiction_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_contradictions_caused_by_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_unit_propagations_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_unit_propagations_caused_by_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_restarts_y_KeepActiveClausesAndRemoveSubsumedClauses = []

for i in range(len(log_KeepActiveClausesAndRemoveSubsumedClauses_list)):
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

    for j in range(len(log_KeepActiveClausesAndRemoveSubsumedClauses_list[i])):
        time_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][0]
        number_of_decisions_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][2]
        number_of_checked_clauses_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][4]
        number_of_clause_deletions_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][5]
        number_of_contradiction_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][7]
        number_of_unit_propagations_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][9]
        number_of_restarts_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][10]
    size = len(log_KeepActiveClausesAndRemoveSubsumedClauses_list[i])
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

    time_y_KeepActiveClausesAndRemoveSubsumedClauses.append(time_average)
    number_of_decisions_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_clause_deletions_average)
    number_of_contradiction_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_restarts_average)

# Log KeepActiveClauses2AndRemoveSubsumedClauses
time_y_KeepActiveClauses2AndRemoveSubsumedClauses = []
number_of_decisions_y_KeepActiveClauses2AndRemoveSubsumedClauses = []
number_of_steps_of_unit_propagation_y_KeepActiveClauses2AndRemoveSubsumedClauses = []
number_of_checked_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses = []
number_of_deleted_learned_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses = []
number_of_clause_deletions_y_KeepActiveClauses2AndRemoveSubsumedClauses = []
number_of_contradiction_y_KeepActiveClauses2AndRemoveSubsumedClauses = []
number_of_contradictions_caused_by_learned_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses = []
number_of_unit_propagations_y_KeepActiveClauses2AndRemoveSubsumedClauses = []
number_of_unit_propagations_caused_by_learned_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses = []
number_of_restarts_y_KeepActiveClauses2AndRemoveSubsumedClauses = []

for i in range(len(log_KeepActiveClauses2AndRemoveSubsumedClauses_list)):
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

    for j in range(len(log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i])):
        time_average += log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i][j][0]
        number_of_decisions_average += log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i][j][2]
        number_of_checked_clauses_average += log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i][j][4]
        number_of_clause_deletions_average += log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i][j][5]
        number_of_contradiction_average += log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i][j][7]
        number_of_unit_propagations_average += log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i][j][9]
        number_of_restarts_average += log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i][j][10]
    size = len(log_KeepActiveClauses2AndRemoveSubsumedClauses_list[i])
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

    time_y_KeepActiveClauses2AndRemoveSubsumedClauses.append(time_average)
    number_of_decisions_y_KeepActiveClauses2AndRemoveSubsumedClauses.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_KeepActiveClauses2AndRemoveSubsumedClauses.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_KeepActiveClauses2AndRemoveSubsumedClauses.append(number_of_clause_deletions_average)
    number_of_contradiction_y_KeepActiveClauses2AndRemoveSubsumedClauses.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_KeepActiveClauses2AndRemoveSubsumedClauses.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_KeepActiveClauses2AndRemoveSubsumedClauses.append(number_of_restarts_average)

# Log KeepShortClausesAndRemoveSubsumedClauses
time_y_KeepShortClausesAndRemoveSubsumedClauses = []
number_of_decisions_y_KeepShortClausesAndRemoveSubsumedClauses = []
number_of_steps_of_unit_propagation_y_KeepShortClausesAndRemoveSubsumedClauses = []
number_of_checked_clauses_y_KeepShortClausesAndRemoveSubsumedClauses = []
number_of_deleted_learned_clauses_y_KeepShortClausesAndRemoveSubsumedClauses = []
number_of_clause_deletions_y_KeepShortClausesAndRemoveSubsumedClauses = []
number_of_contradiction_y_KeepShortClausesAndRemoveSubsumedClauses = []
number_of_contradictions_caused_by_learned_clauses_y_KeepShortClausesAndRemoveSubsumedClauses = []
number_of_unit_propagations_y_KeepShortClausesAndRemoveSubsumedClauses = []
number_of_unit_propagations_caused_by_learned_clauses_y_KeepShortClausesAndRemoveSubsumedClauses = []
number_of_restarts_y_KeepShortClausesAndRemoveSubsumedClauses = []

for i in range(len(log_KeepShortClausesAndRemoveSubsumedClauses_list)):
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

    for j in range(len(log_KeepShortClausesAndRemoveSubsumedClauses_list[i])):
        time_average += log_KeepShortClausesAndRemoveSubsumedClauses_list[i][j][0]
        number_of_decisions_average += log_KeepShortClausesAndRemoveSubsumedClauses_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_KeepShortClausesAndRemoveSubsumedClauses_list[i][j][2]
        number_of_checked_clauses_average += log_KeepShortClausesAndRemoveSubsumedClauses_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_KeepShortClausesAndRemoveSubsumedClauses_list[i][j][4]
        number_of_clause_deletions_average += log_KeepShortClausesAndRemoveSubsumedClauses_list[i][j][5]
        number_of_contradiction_average += log_KeepShortClausesAndRemoveSubsumedClauses_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_KeepShortClausesAndRemoveSubsumedClauses_list[i][j][7]
        number_of_unit_propagations_average += log_KeepShortClausesAndRemoveSubsumedClauses_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_KeepShortClausesAndRemoveSubsumedClauses_list[i][j][9]
        number_of_restarts_average += log_KeepShortClausesAndRemoveSubsumedClauses_list[i][j][10]
    size = len(log_KeepShortClausesAndRemoveSubsumedClauses_list[i])
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

    time_y_KeepShortClausesAndRemoveSubsumedClauses.append(time_average)
    number_of_decisions_y_KeepShortClausesAndRemoveSubsumedClauses.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_KeepShortClausesAndRemoveSubsumedClauses.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_KeepShortClausesAndRemoveSubsumedClauses.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_KeepShortClausesAndRemoveSubsumedClauses.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_KeepShortClausesAndRemoveSubsumedClauses.append(number_of_clause_deletions_average)
    number_of_contradiction_y_KeepShortClausesAndRemoveSubsumedClauses.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_KeepShortClausesAndRemoveSubsumedClauses.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_KeepShortClausesAndRemoveSubsumedClauses.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_KeepShortClausesAndRemoveSubsumedClauses.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_KeepShortClausesAndRemoveSubsumedClauses.append(number_of_restarts_average)

print("RemoveSubsumedClauses")
print("Time: ")
print(time_y_RemoveSubsumedClauses)
print("Number of decisions: ")
print(number_of_decisions_y_RemoveSubsumedClauses)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_RemoveSubsumedClauses)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_RemoveSubsumedClauses)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_RemoveSubsumedClauses)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_RemoveSubsumedClauses)
print("Number of contradictions: ")
print(number_of_contradiction_y_RemoveSubsumedClauses)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_RemoveSubsumedClauses)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_RemoveSubsumedClauses)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_RemoveSubsumedClauses)
print("Number of restarts: ")
print(number_of_restarts_y_RemoveSubsumedClauses)

print()

print("KeepShortClauses")
print("Time: ")
print(time_y_KeepShortClauses)
print("Number of decisions: ")
print(number_of_decisions_y_KeepShortClauses)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_KeepShortClauses)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_KeepShortClauses)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_KeepShortClauses)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_KeepShortClauses)
print("Number of contradictions: ")
print(number_of_contradiction_y_KeepShortClauses)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_KeepShortClauses)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_KeepShortClauses)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_KeepShortClauses)
print("Number of restarts: ")
print(number_of_restarts_y_KeepShortClauses)

print()

print("KeepShortClausesAndRemoveSubsumedClauses")
print("Time: ")
print(time_y_KeepShortClausesAndRemoveSubsumedClauses)
print("Number of decisions: ")
print(number_of_decisions_y_KeepShortClausesAndRemoveSubsumedClauses)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_KeepShortClausesAndRemoveSubsumedClauses)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_KeepShortClausesAndRemoveSubsumedClauses)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_KeepShortClausesAndRemoveSubsumedClauses)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_KeepShortClausesAndRemoveSubsumedClauses)
print("Number of contradictions: ")
print(number_of_contradiction_y_KeepShortClausesAndRemoveSubsumedClauses)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_KeepShortClausesAndRemoveSubsumedClauses)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_KeepShortClausesAndRemoveSubsumedClauses)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_KeepShortClausesAndRemoveSubsumedClauses)
print("Number of restarts: ")
print(number_of_restarts_y_KeepShortClausesAndRemoveSubsumedClauses)

print()

print("KeepActiveClauses")
print("Time: ")
print(time_y_KeepActiveClauses)
print("Number of decisions: ")
print(number_of_decisions_y_KeepActiveClauses)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_KeepActiveClauses)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_KeepActiveClauses)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_KeepActiveClauses)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_KeepActiveClauses)
print("Number of contradictions: ")
print(number_of_contradiction_y_KeepActiveClauses)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_KeepActiveClauses)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_KeepActiveClauses)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_KeepActiveClauses)
print("Number of restarts: ")
print(number_of_restarts_y_KeepActiveClauses)

print()

print("KeepActiveClausesAndRemoveSubsumedClauses")
print("Time: ")
print(time_y_KeepActiveClausesAndRemoveSubsumedClauses)
print("Number of decisions: ")
print(number_of_decisions_y_KeepActiveClausesAndRemoveSubsumedClauses)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_KeepActiveClausesAndRemoveSubsumedClauses)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_KeepActiveClausesAndRemoveSubsumedClauses)
print("Number of contradictions: ")
print(number_of_contradiction_y_KeepActiveClausesAndRemoveSubsumedClauses)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_KeepActiveClausesAndRemoveSubsumedClauses)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses)
print("Number of restarts: ")
print(number_of_restarts_y_KeepActiveClausesAndRemoveSubsumedClauses)

print()

print("KeepActiveClauses2")
print("Time: ")
print(time_y_KeepActiveClauses2)
print("Number of decisions: ")
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_KeepActiveClauses2)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_KeepActiveClauses2)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_KeepActiveClauses2)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_KeepActiveClauses2)
print("Number of contradictions: ")
print(number_of_contradiction_y_KeepActiveClauses2)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_KeepActiveClauses2)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_KeepActiveClauses2)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_KeepActiveClauses2)
print("Number of restarts: ")
print(number_of_restarts_y_KeepActiveClauses2)

print()

print("KeepActiveClauses2AndRemoveSubsumedClauses")
print("Time: ")
print(time_y_KeepActiveClauses2AndRemoveSubsumedClauses)
print("Number of decisions: ")
print(number_of_decisions_y_KeepActiveClauses2AndRemoveSubsumedClauses)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_KeepActiveClauses2AndRemoveSubsumedClauses)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_KeepActiveClauses2AndRemoveSubsumedClauses)
print("Number of contradictions: ")
print(number_of_contradiction_y_KeepActiveClauses2AndRemoveSubsumedClauses)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_KeepActiveClauses2AndRemoveSubsumedClauses)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses)
print("Number of restarts: ")
print(number_of_restarts_y_KeepActiveClauses2AndRemoveSubsumedClauses)

# Time
plt.plot(x_axis_variables, time_y_RemoveSubsumedClauses, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, time_y_KeepShortClauses, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, time_y_KeepShortClausesAndRemoveSubsumedClauses, color="purple", label='KeepShortClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, time_y_KeepActiveClauses, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, time_y_KeepActiveClausesAndRemoveSubsumedClauses, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, time_y_KeepActiveClauses2, color="orange", label='KeepActiveClauses2')
plt.plot(x_axis_variables, time_y_KeepActiveClauses2AndRemoveSubsumedClauses, color="black", label='KeepActiveClauses2AndRemoveSubsumedClauses')
plt.title('Time')
plt.xlabel('Number of variables')
plt.ylabel('Time (s)')
plt.legend(loc="upper left")
plt.show()

# Number of checked clauses
plt.plot(x_axis_variables, number_of_checked_clauses_y_RemoveSubsumedClauses, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_checked_clauses_y_KeepShortClauses, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, number_of_checked_clauses_y_KeepShortClausesAndRemoveSubsumedClauses, color="purple", label='KeepShortClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_checked_clauses_y_KeepActiveClauses, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, number_of_checked_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_checked_clauses_y_KeepActiveClauses2, color="orange", label='KeepActiveClauses2')
plt.plot(x_axis_variables, number_of_checked_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses, color="black", label='KeepActiveClauses2AndRemoveSubsumedClauses')
plt.title('Number of checked clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of checked clauses')
plt.legend(loc="upper left")
plt.show()

# Number of decisions
plt.plot(x_axis_variables, number_of_decisions_y_RemoveSubsumedClauses, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_decisions_y_KeepShortClauses, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, number_of_decisions_y_KeepShortClausesAndRemoveSubsumedClauses, color="purple", label='KeepShortClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_decisions_y_KeepActiveClauses, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, number_of_decisions_y_KeepActiveClausesAndRemoveSubsumedClauses, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_decisions_y_KeepActiveClauses2, color="orange", label='KeepActiveClauses2')
plt.plot(x_axis_variables, number_of_decisions_y_KeepActiveClauses2AndRemoveSubsumedClauses, color="black", label='KeepActiveClauses2AndRemoveSubsumedClauses')
plt.title('Number of decisions')
plt.xlabel('Number of variables')
plt.ylabel('Number of decisions')
plt.legend(loc="upper left")
plt.show()

# Number of steps of unit propagation
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_RemoveSubsumedClauses, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_KeepShortClauses, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_KeepShortClausesAndRemoveSubsumedClauses, color="purple", label='KeepShortClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_KeepActiveClauses, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_KeepActiveClausesAndRemoveSubsumedClauses, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_KeepActiveClauses2, color="orange", label='KeepActiveClauses2')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_KeepActiveClauses2AndRemoveSubsumedClauses, color="black", label='KeepActiveClauses2AndRemoveSubsumedClauses')
plt.title('Number of steps of unit propagation')
plt.xlabel('Number of variables')
plt.ylabel('Number of steps of unit propagation')
plt.legend(loc="upper left")
plt.show()

# Number of deleted learned clauses
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_RemoveSubsumedClauses, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_KeepShortClauses, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_KeepShortClausesAndRemoveSubsumedClauses, color="purple", label='KeepShortClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_KeepActiveClauses, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_KeepActiveClauses2, color="orange", label='KeepActiveClauses2')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_KeepActiveClauses2AndRemoveSubsumedClauses, color="black", label='KeepActiveClauses2AndRemoveSubsumedClauses')
plt.title('Number of deleted learned clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of deleted learned clauses')
plt.legend(loc="upper left")
plt.show()

# Number of clause deletions
plt.plot(x_axis_variables, number_of_clause_deletions_y_RemoveSubsumedClauses, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_clause_deletions_y_KeepShortClauses, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, number_of_clause_deletions_y_KeepShortClausesAndRemoveSubsumedClauses, color="purple", label='KeepShortClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_clause_deletions_y_KeepActiveClauses, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, number_of_clause_deletions_y_KeepActiveClausesAndRemoveSubsumedClauses, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_clause_deletions_y_KeepActiveClauses2, color="orange", label='KeepActiveClauses2')
plt.plot(x_axis_variables, number_of_clause_deletions_y_KeepActiveClauses2AndRemoveSubsumedClauses, color="black", label='KeepActiveClauses2AndRemoveSubsumedClauses')
plt.title('Number of clause deletions')
plt.xlabel('Number of variables')
plt.ylabel('Number of clause deletions')
plt.legend(loc="upper left")
plt.show()