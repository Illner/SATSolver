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
dictionary_list = ["20-91", "50-218", "75-325", "100-430", "125-538"]
x_axis_variables = [20, 50, 75, 100, 125]
count_list = [1024, 128, 16, 8, 4]

log_RemoveSubsumedClauses_list = []
log_KeepShortClauses_list = []
log_KeepActiveClauses_list = []
log_KeepActiveClausesAndRemoveSubsumedClauses_list = []

for i in range(len(dictionary_list)):
    print("\n" + str(i))
    log_RemoveSubsumedClauses_list.append([])
    log_KeepShortClauses_list.append([])
    log_KeepActiveClauses_list.append([])
    log_KeepActiveClausesAndRemoveSubsumedClauses_list.append([])

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
                  decision_heuristic_enum=DecisionHeuristicEnum.Greedy,
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

        log_RemoveSubsumedClauses_list[i].append((cdcl.time, 
                                                  cdcl.number_of_decisions, 
                                                  cdcl.number_of_steps_of_unit_propagation, 
                                                  cnf.number_of_checked_clauses,
                                                  cnf.number_of_deleted_learned_clauses,
                                                  cnf.number_of_clause_deletions))

        print()

        # KeepShortClauses
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.Greedy,
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

        log_KeepShortClauses_list[i].append((cdcl.time, 
                                             cdcl.number_of_decisions, 
                                             cdcl.number_of_steps_of_unit_propagation, 
                                             cnf.number_of_checked_clauses,
                                             cnf.number_of_deleted_learned_clauses,
                                             cnf.number_of_clause_deletions))

        print()

        # KeepActiveClauses
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.Greedy,
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

        log_KeepActiveClauses_list[i].append((cdcl.time, 
                                              cdcl.number_of_decisions, 
                                              cdcl.number_of_steps_of_unit_propagation, 
                                              cnf.number_of_checked_clauses,
                                              cnf.number_of_deleted_learned_clauses,
                                              cnf.number_of_clause_deletions))

        print()

        # KeepActiveClausesAndRemoveSubsumedClauses
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.Greedy,
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

        log_KeepActiveClausesAndRemoveSubsumedClauses_list[i].append((cdcl.time, 
                                                                      cdcl.number_of_decisions, 
                                                                      cdcl.number_of_steps_of_unit_propagation, 
                                                                      cnf.number_of_checked_clauses,
                                                                      cnf.number_of_deleted_learned_clauses,
                                                                      cnf.number_of_clause_deletions))

        print()

# Log RemoveSubsumedClauses
time_y_RemoveSubsumedClauses = []
number_of_decisions_y_RemoveSubsumedClauses = []
number_of_steps_of_unit_propagation_y_RemoveSubsumedClauses = []
number_of_checked_clauses_y_RemoveSubsumedClauses = []
number_of_deleted_learned_clauses_y_RemoveSubsumedClauses = []
number_of_clause_deletions_y_RemoveSubsumedClauses = []

for i in range(len(log_RemoveSubsumedClauses_list)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0
    number_of_deleted_learned_clauses_average = 0
    number_of_clause_deletions_average = 0

    for j in range(len(log_RemoveSubsumedClauses_list[i])):
        time_average += log_RemoveSubsumedClauses_list[i][j][0]
        number_of_decisions_average += log_RemoveSubsumedClauses_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_RemoveSubsumedClauses_list[i][j][2]
        number_of_checked_clauses_average += log_RemoveSubsumedClauses_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_RemoveSubsumedClauses_list[i][j][4]
        number_of_clause_deletions_average += log_RemoveSubsumedClauses_list[i][j][5]
    size = len(log_RemoveSubsumedClauses_list[i])
    if (size != 0):
        time_average /= size
        number_of_decisions_average /= size
        number_of_steps_of_unit_propagation_average /= size
        number_of_checked_clauses_average /= size
        number_of_deleted_learned_clauses_average /= size
        number_of_clause_deletions_average /= size

    time_y_RemoveSubsumedClauses.append(time_average)
    number_of_decisions_y_RemoveSubsumedClauses.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_RemoveSubsumedClauses.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_RemoveSubsumedClauses.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_RemoveSubsumedClauses.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_RemoveSubsumedClauses.append(number_of_clause_deletions_average)

# Log KeepShortClauses
time_y_KeepShortClauses = []
number_of_decisions_y_KeepShortClauses = []
number_of_steps_of_unit_propagation_y_KeepShortClauses = []
number_of_checked_clauses_y_KeepShortClauses = []
number_of_deleted_learned_clauses_y_KeepShortClauses = []
number_of_clause_deletions_y_KeepShortClauses = []

for i in range(len(log_KeepShortClauses_list)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0
    number_of_deleted_learned_clauses_average = 0
    number_of_clause_deletions_average = 0

    for j in range(len(log_KeepShortClauses_list[i])):
        time_average += log_KeepShortClauses_list[i][j][0]
        number_of_decisions_average += log_KeepShortClauses_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_KeepShortClauses_list[i][j][2]
        number_of_checked_clauses_average += log_KeepShortClauses_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_KeepShortClauses_list[i][j][4]
        number_of_clause_deletions_average += log_KeepShortClauses_list[i][j][5]
    size = len(log_KeepShortClauses_list[i])
    if (size != 0):
        time_average /= size
        number_of_decisions_average /= size
        number_of_steps_of_unit_propagation_average /= size
        number_of_checked_clauses_average /= size
        number_of_deleted_learned_clauses_average /= size
        number_of_clause_deletions_average /= size

    time_y_KeepShortClauses.append(time_average)
    number_of_decisions_y_KeepShortClauses.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_KeepShortClauses.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_KeepShortClauses.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_KeepShortClauses.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_KeepShortClauses.append(number_of_clause_deletions_average)

# Log KeepActiveClauses
time_y_KeepActiveClauses = []
number_of_decisions_y_KeepActiveClauses = []
number_of_steps_of_unit_propagation_y_KeepActiveClauses = []
number_of_checked_clauses_y_KeepActiveClauses = []
number_of_deleted_learned_clauses_y_KeepActiveClauses = []
number_of_clause_deletions_y_KeepActiveClauses = []

for i in range(len(log_KeepActiveClauses_list)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0
    number_of_deleted_learned_clauses_average = 0
    number_of_clause_deletions_average = 0

    for j in range(len(log_KeepActiveClauses_list[i])):
        time_average += log_KeepActiveClauses_list[i][j][0]
        number_of_decisions_average += log_KeepActiveClauses_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_KeepActiveClauses_list[i][j][2]
        number_of_checked_clauses_average += log_KeepActiveClauses_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_KeepActiveClauses_list[i][j][4]
        number_of_clause_deletions_average += log_KeepActiveClauses_list[i][j][5]
    size = len(log_KeepActiveClauses_list[i])
    if (size != 0):
        time_average /= size
        number_of_decisions_average /= size
        number_of_steps_of_unit_propagation_average /= size
        number_of_checked_clauses_average /= size
        number_of_deleted_learned_clauses_average /= size
        number_of_clause_deletions_average /= size

    time_y_KeepActiveClauses.append(time_average)
    number_of_decisions_y_KeepActiveClauses.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_KeepActiveClauses.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_KeepActiveClauses.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_KeepActiveClauses.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_KeepActiveClauses.append(number_of_clause_deletions_average)

# Log KeepActiveClausesAndRemoveSubsumedClauses
time_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_decisions_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_steps_of_unit_propagation_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_checked_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_deleted_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses = []
number_of_clause_deletions_y_KeepActiveClausesAndRemoveSubsumedClauses = []

for i in range(len(log_KeepActiveClausesAndRemoveSubsumedClauses_list)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0
    number_of_deleted_learned_clauses_average = 0
    number_of_clause_deletions_average = 0

    for j in range(len(log_KeepActiveClausesAndRemoveSubsumedClauses_list[i])):
        time_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][0]
        number_of_decisions_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][2]
        number_of_checked_clauses_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][4]
        number_of_clause_deletions_average += log_KeepActiveClausesAndRemoveSubsumedClauses_list[i][j][5]
    size = len(log_KeepActiveClausesAndRemoveSubsumedClauses_list[i])
    if (size != 0):
        time_average /= size
        number_of_decisions_average /= size
        number_of_steps_of_unit_propagation_average /= size
        number_of_checked_clauses_average /= size
        number_of_deleted_learned_clauses_average /= size
        number_of_clause_deletions_average /= size

    time_y_KeepActiveClausesAndRemoveSubsumedClauses.append(time_average)
    number_of_decisions_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_KeepActiveClausesAndRemoveSubsumedClauses.append(number_of_clause_deletions_average)

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

# Time
plt.plot(x_axis_variables, time_y_RemoveSubsumedClauses, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, time_y_KeepShortClauses, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, time_y_KeepActiveClauses, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, time_y_KeepActiveClausesAndRemoveSubsumedClauses, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.title('Time')
plt.xlabel('Number of variables')
plt.ylabel('Time (s)')
plt.legend(loc="upper left")
plt.show()

# Number of checked clauses
plt.plot(x_axis_variables, number_of_decisions_y_RemoveSubsumedClauses, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_decisions_y_KeepShortClauses, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, number_of_decisions_y_KeepActiveClauses, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, number_of_decisions_y_KeepActiveClausesAndRemoveSubsumedClauses, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.title('Number of checked clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of checked clauses')
plt.legend(loc="upper left")
plt.show()

# Number of decisions
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_RemoveSubsumedClauses, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_KeepShortClauses, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_KeepActiveClauses, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_KeepActiveClausesAndRemoveSubsumedClauses, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.title('Number of decisions')
plt.xlabel('Number of variables')
plt.ylabel('Number of decisions')
plt.legend(loc="upper left")
plt.show()

# Number of steps of unit propagation
plt.plot(x_axis_variables, number_of_checked_clauses_y_RemoveSubsumedClauses, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_checked_clauses_y_KeepShortClauses, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, number_of_checked_clauses_y_KeepActiveClauses, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, number_of_checked_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.title('Number of steps of unit propagation')
plt.xlabel('Number of variables')
plt.ylabel('Number of steps of unit propagation')
plt.legend(loc="upper left")
plt.show()

# Number of deleted learned clauses
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_RemoveSubsumedClauses, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_KeepShortClauses, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_KeepActiveClauses, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_KeepActiveClausesAndRemoveSubsumedClauses, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.title('Number of deleted learned clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of deleted learned clauses')
plt.legend(loc="upper left")
plt.show()

# Number of clause deletions
plt.plot(x_axis_variables, number_of_clause_deletions_y_RemoveSubsumedClauses, color="blue", label='RemoveSubsumedClauses')
plt.plot(x_axis_variables, number_of_clause_deletions_y_KeepShortClauses, color="red", label='KeepShortClauses')
plt.plot(x_axis_variables, number_of_clause_deletions_y_KeepActiveClauses, color="green", label='KeepActiveClauses')
plt.plot(x_axis_variables, number_of_clause_deletions_y_KeepActiveClausesAndRemoveSubsumedClauses, color="yellow", label='KeepActiveClausesAndRemoveSubsumedClauses')
plt.title('Number of clause deletions')
plt.xlabel('Number of variables')
plt.ylabel('Number of clause deletions')
plt.legend(loc="upper left")
plt.show()