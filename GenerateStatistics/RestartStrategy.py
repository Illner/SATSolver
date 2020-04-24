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

log_LubyStrategy_list = []
log_GeometricStrategy_list = []

for i in range(len(dictionary_list)):
    print("\n" + str(i))
    log_LubyStrategy_list.append([])
    log_GeometricStrategy_list.append([])
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

        # LubyStrategy
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
            raise MyException.SomethingWrongException("Invalid model - LubyStrategy")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - LubyStrategy")

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

        log_LubyStrategy_list[i].append((cdcl.time,
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

        # GeometricStrategy
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.Random,
                  clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.GeometricStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - GeometricStrategy")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - GeometricStrategy")

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

        log_GeometricStrategy_list[i].append((cdcl.time, 
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

# Log LubyStrategy
time_y_LubyStrategy = []
number_of_decisions_y_LubyStrategy = []
number_of_steps_of_unit_propagation_y_LubyStrategy = []
number_of_checked_clauses_y_LubyStrategy = []
number_of_deleted_learned_clauses_y_LubyStrategy = []
number_of_clause_deletions_y_LubyStrategy = []
number_of_contradiction_y_LubyStrategy = []
number_of_contradictions_caused_by_learned_clauses_y_LubyStrategy = []
number_of_unit_propagations_y_LubyStrategy = []
number_of_unit_propagations_caused_by_learned_clauses_y_LubyStrategy = []
number_of_restarts_y_LubyStrategy = []

for i in range(len(log_LubyStrategy_list)):
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

    for j in range(len(log_LubyStrategy_list[i])):
        time_average += log_LubyStrategy_list[i][j][0]
        number_of_decisions_average += log_LubyStrategy_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_LubyStrategy_list[i][j][2]
        number_of_checked_clauses_average += log_LubyStrategy_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_LubyStrategy_list[i][j][4]
        number_of_clause_deletions_average += log_LubyStrategy_list[i][j][5]
        number_of_contradiction_average += log_LubyStrategy_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_LubyStrategy_list[i][j][7]
        number_of_unit_propagations_average += log_LubyStrategy_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_LubyStrategy_list[i][j][9]
        number_of_restarts_average += log_LubyStrategy_list[i][j][10]
    size = len(log_LubyStrategy_list[i])
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

    time_y_LubyStrategy.append(time_average)
    number_of_decisions_y_LubyStrategy.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_LubyStrategy.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_LubyStrategy.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_LubyStrategy.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_LubyStrategy.append(number_of_clause_deletions_average)
    number_of_contradiction_y_LubyStrategy.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_LubyStrategy.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_LubyStrategy.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_LubyStrategy.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_LubyStrategy.append(number_of_restarts_average)

# Log GeometricStrategy
time_y_GeometricStrategy = []
number_of_decisions_y_GeometricStrategy = []
number_of_steps_of_unit_propagation_y_GeometricStrategy = []
number_of_checked_clauses_y_GeometricStrategy = []
number_of_deleted_learned_clauses_y_GeometricStrategy = []
number_of_clause_deletions_y_GeometricStrategy = []
number_of_contradiction_y_GeometricStrategy = []
number_of_contradictions_caused_by_learned_clauses_y_GeometricStrategy = []
number_of_unit_propagations_y_GeometricStrategy = []
number_of_unit_propagations_caused_by_learned_clauses_y_GeometricStrategy = []
number_of_restarts_y_GeometricStrategy = []

for i in range(len(log_GeometricStrategy_list)):
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

    for j in range(len(log_GeometricStrategy_list[i])):
        time_average += log_GeometricStrategy_list[i][j][0]
        number_of_decisions_average += log_GeometricStrategy_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_GeometricStrategy_list[i][j][2]
        number_of_checked_clauses_average += log_GeometricStrategy_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_GeometricStrategy_list[i][j][4]
        number_of_clause_deletions_average += log_GeometricStrategy_list[i][j][5]
        number_of_contradiction_average += log_GeometricStrategy_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_GeometricStrategy_list[i][j][7]
        number_of_unit_propagations_average += log_GeometricStrategy_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_GeometricStrategy_list[i][j][9]
        number_of_restarts_average += log_GeometricStrategy_list[i][j][10]
    size = len(log_GeometricStrategy_list[i])
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

    time_y_GeometricStrategy.append(time_average)
    number_of_decisions_y_GeometricStrategy.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_GeometricStrategy.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_GeometricStrategy.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_GeometricStrategy.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_GeometricStrategy.append(number_of_clause_deletions_average)
    number_of_contradiction_y_GeometricStrategy.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_GeometricStrategy.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_GeometricStrategy.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_GeometricStrategy.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_GeometricStrategy.append(number_of_restarts_average)

print("LubyStrategy")
print("Time: ")
print(time_y_LubyStrategy)
print("Number of decisions: ")
print(number_of_decisions_y_LubyStrategy)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_LubyStrategy)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_LubyStrategy)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_LubyStrategy)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_LubyStrategy)
print("Number of contradictions: ")
print(number_of_contradiction_y_LubyStrategy)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_LubyStrategy)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_LubyStrategy)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_LubyStrategy)
print("Number of restarts: ")
print(number_of_restarts_y_LubyStrategy)

print()

print("GeometricStrategy")
print("Time: ")
print(time_y_GeometricStrategy)
print("Number of decisions: ")
print(number_of_decisions_y_GeometricStrategy)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_GeometricStrategy)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_GeometricStrategy)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_GeometricStrategy)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_GeometricStrategy)
print("Number of contradictions: ")
print(number_of_contradiction_y_GeometricStrategy)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_GeometricStrategy)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_GeometricStrategy)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_GeometricStrategy)
print("Number of restarts: ")
print(number_of_restarts_y_GeometricStrategy)

# Time
plt.plot(x_axis_variables, time_y_LubyStrategy, color="blue", label='LubyStrategy')
plt.plot(x_axis_variables, time_y_GeometricStrategy, color="red", label='GeometricStrategy')
plt.title('Time')
plt.xlabel('Number of variables')
plt.ylabel('Time (s)')
plt.legend(loc="upper left")
plt.show()

# Number of checked clauses
plt.plot(x_axis_variables, number_of_decisions_y_LubyStrategy, color="blue", label='LubyStrategy')
plt.plot(x_axis_variables, number_of_decisions_y_GeometricStrategy, color="red", label='GeometricStrategy')
plt.title('Number of checked clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of checked clauses')
plt.legend(loc="upper left")
plt.show()

# Number of decisions
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_LubyStrategy, color="blue", label='LubyStrategy')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_GeometricStrategy, color="red", label='GeometricStrategy')
plt.title('Number of decisions')
plt.xlabel('Number of variables')
plt.ylabel('Number of decisions')
plt.legend(loc="upper left")
plt.show()

# Number of steps of unit propagation
plt.plot(x_axis_variables, number_of_checked_clauses_y_LubyStrategy, color="blue", label='LubyStrategy')
plt.plot(x_axis_variables, number_of_checked_clauses_y_GeometricStrategy, color="red", label='GeometricStrategy')
plt.title('Number of steps of unit propagation')
plt.xlabel('Number of variables')
plt.ylabel('Number of steps of unit propagation')
plt.legend(loc="upper left")
plt.show()

# Number of deleted learned clauses
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_LubyStrategy, color="blue", label='LubyStrategy')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_GeometricStrategy, color="red", label='GeometricStrategy')
plt.title('Number of deleted learned clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of deleted learned clauses')
plt.legend(loc="upper left")
plt.show()

# Number of clause deletions
plt.plot(x_axis_variables, number_of_clause_deletions_y_LubyStrategy, color="blue", label='LubyStrategy')
plt.plot(x_axis_variables, number_of_clause_deletions_y_GeometricStrategy, color="red", label='GeometricStrategy')
plt.title('Number of clause deletions')
plt.xlabel('Number of variables')
plt.ylabel('Number of clause deletions')
plt.legend(loc="upper left")
plt.show()