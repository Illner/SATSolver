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
count_list = [1024, 512, 256, 64]

log_StopAtTheFirstUIP_list = []
log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list = []

for i in range(len(dictionary_list)):
    print("\n" + str(i))
    log_StopAtTheFirstUIP_list.append([])
    log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list.append([])
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

        # StopAtTheFirstUIP
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
            raise MyException.SomethingWrongException("Invalid model - StopAtTheFirstUIP")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - StopAtTheFirstUIP")

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

        log_StopAtTheFirstUIP_list[i].append((cdcl.time, 
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

        # StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent
        cnf = CNF(input_formula, 
                  unit_propagation_enum=UnitPropagationEnum.WatchedLiterals,
                  decision_heuristic_enum=DecisionHeuristicEnum.Random,
                  clause_learning_enum=ClauseLearningEnum.StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent, 
                  clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses,
                  clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart,
                  restart_strategy_enum=RestartStrategyEnum.LubyStrategy)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent")

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

        log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i].append((cdcl.time, 
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

# Log StopAtTheFirstUIP
time_y_StopAtTheFirstUIP = []
number_of_decisions_y_StopAtTheFirstUIP = []
number_of_steps_of_unit_propagation_y_StopAtTheFirstUIP = []
number_of_checked_clauses_y_StopAtTheFirstUIP = []
number_of_deleted_learned_clauses_y_StopAtTheFirstUIP = []
number_of_clause_deletions_y_StopAtTheFirstUIP = []
number_of_contradiction_y_StopAtTheFirstUIP = []
number_of_contradictions_caused_by_learned_clauses_y_StopAtTheFirstUIP = []
number_of_unit_propagations_y_StopAtTheFirstUIP = []
number_of_unit_propagations_caused_by_learned_clauses_y_StopAtTheFirstUIP = []
number_of_restarts_y_StopAtTheFirstUIP = []

for i in range(len(log_StopAtTheFirstUIP_list)):
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

    for j in range(len(log_StopAtTheFirstUIP_list[i])):
        time_average += log_StopAtTheFirstUIP_list[i][j][0]
        number_of_decisions_average += log_StopAtTheFirstUIP_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_StopAtTheFirstUIP_list[i][j][2]
        number_of_checked_clauses_average += log_StopAtTheFirstUIP_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_StopAtTheFirstUIP_list[i][j][4]
        number_of_clause_deletions_average += log_StopAtTheFirstUIP_list[i][j][5]
        number_of_contradiction_average += log_StopAtTheFirstUIP_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_StopAtTheFirstUIP_list[i][j][7]
        number_of_unit_propagations_average += log_StopAtTheFirstUIP_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_StopAtTheFirstUIP_list[i][j][9]
        number_of_restarts_average += log_StopAtTheFirstUIP_list[i][j][10]
    size = len(log_StopAtTheFirstUIP_list[i])
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

    time_y_StopAtTheFirstUIP.append(time_average)
    number_of_decisions_y_StopAtTheFirstUIP.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_StopAtTheFirstUIP.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_StopAtTheFirstUIP.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_StopAtTheFirstUIP.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_StopAtTheFirstUIP.append(number_of_clause_deletions_average)
    number_of_contradiction_y_StopAtTheFirstUIP.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_StopAtTheFirstUIP.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_StopAtTheFirstUIP.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_StopAtTheFirstUIP.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_StopAtTheFirstUIP.append(number_of_restarts_average)

# Log StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent
time_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent = []
number_of_decisions_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent = []
number_of_steps_of_unit_propagation_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent = []
number_of_checked_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent = []
number_of_deleted_learned_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent = []
number_of_clause_deletions_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent = []
number_of_contradiction_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent = []
number_of_contradictions_caused_by_learned_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent = []
number_of_unit_propagations_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent = []
number_of_unit_propagations_caused_by_learned_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent = []
number_of_restarts_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent = []

for i in range(len(log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list)):
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

    for j in range(len(log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i])):
        time_average += log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i][j][0]
        number_of_decisions_average += log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i][j][2]
        number_of_checked_clauses_average += log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i][j][3]
        number_of_deleted_learned_clauses_average += log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i][j][4]
        number_of_clause_deletions_average += log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i][j][5]
        number_of_contradiction_average += log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i][j][6]
        number_of_contradictions_caused_by_learned_clauses_average += log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i][j][7]
        number_of_unit_propagations_average += log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i][j][8]
        number_of_unit_propagations_caused_by_learned_clauses_average += log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i][j][9]
        number_of_restarts_average += log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i][j][10]
    size = len(log_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent_list[i])
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

    time_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent.append(time_average)
    number_of_decisions_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent.append(number_of_checked_clauses_average)
    number_of_deleted_learned_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent.append(number_of_deleted_learned_clauses_average)
    number_of_clause_deletions_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent.append(number_of_clause_deletions_average)
    number_of_contradiction_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent.append(number_of_contradiction_average)
    number_of_contradictions_caused_by_learned_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent.append(number_of_contradictions_caused_by_learned_clauses_average)
    number_of_unit_propagations_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent.append(number_of_unit_propagations_average)
    number_of_unit_propagations_caused_by_learned_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent.append(number_of_unit_propagations_caused_by_learned_clauses_average)
    number_of_restarts_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent.append(number_of_restarts_average)

print("StopAtTheFirstUIP")
print("Time: ")
print(time_y_StopAtTheFirstUIP)
print("Number of decisions: ")
print(number_of_decisions_y_StopAtTheFirstUIP)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_StopAtTheFirstUIP)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_StopAtTheFirstUIP)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_StopAtTheFirstUIP)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_StopAtTheFirstUIP)
print("Number of contradictions: ")
print(number_of_contradiction_y_StopAtTheFirstUIP)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_StopAtTheFirstUIP)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_StopAtTheFirstUIP)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_StopAtTheFirstUIP)
print("Number of restarts: ")
print(number_of_restarts_y_StopAtTheFirstUIP)

print()

print("StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent")
print("Time: ")
print(time_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent)
print("Number of decisions: ")
print(number_of_decisions_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent)
print("Number of deleted learned clauses: ")
print(number_of_deleted_learned_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent)
print("Number of clause deletions: ")
print(number_of_clause_deletions_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent)
print("Number of contradictions: ")
print(number_of_contradiction_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent)
print("Number of contradictions caused by learned clauses: ")
print(number_of_contradictions_caused_by_learned_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent)
print("Number of unit propagations: ")
print(number_of_unit_propagations_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent)
print("Number of unit propagations caused by learned clauses: ")
print(number_of_unit_propagations_caused_by_learned_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent)
print("Number of restarts: ")
print(number_of_restarts_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent)

# Time
plt.plot(x_axis_variables, time_y_StopAtTheFirstUIP, color="blue", label='StopAtTheFirstUIP')
plt.plot(x_axis_variables, time_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent, color="red", label='StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent')
plt.title('Time')
plt.xlabel('Number of variables')
plt.ylabel('Time (s)')
plt.legend(loc="upper left")
plt.show()

# Number of checked clauses
plt.plot(x_axis_variables, number_of_decisions_y_StopAtTheFirstUIP, color="blue", label='StopAtTheFirstUIP')
plt.plot(x_axis_variables, number_of_decisions_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent, color="red", label='StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent')
plt.title('Number of checked clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of checked clauses')
plt.legend(loc="upper left")
plt.show()

# Number of decisions
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_StopAtTheFirstUIP, color="blue", label='StopAtTheFirstUIP')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent, color="red", label='StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent')
plt.title('Number of decisions')
plt.xlabel('Number of variables')
plt.ylabel('Number of decisions')
plt.legend(loc="upper left")
plt.show()

# Number of steps of unit propagation
plt.plot(x_axis_variables, number_of_checked_clauses_y_StopAtTheFirstUIP, color="blue", label='StopAtTheFirstUIP')
plt.plot(x_axis_variables, number_of_checked_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent, color="red", label='StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent')
plt.title('Number of steps of unit propagation')
plt.xlabel('Number of variables')
plt.ylabel('Number of steps of unit propagation')
plt.legend(loc="upper left")
plt.show()

# Number of deleted learned clauses
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_StopAtTheFirstUIP, color="blue", label='StopAtTheFirstUIP')
plt.plot(x_axis_variables, number_of_deleted_learned_clauses_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent, color="red", label='StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent')
plt.title('Number of deleted learned clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of deleted learned clauses')
plt.legend(loc="upper left")
plt.show()

# Number of clause deletions
plt.plot(x_axis_variables, number_of_clause_deletions_y_StopAtTheFirstUIP, color="blue", label='StopAtTheFirstUIP')
plt.plot(x_axis_variables, number_of_clause_deletions_y_StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent, color="red", label='StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent')
plt.title('Number of clause deletions')
plt.xlabel('Number of variables')
plt.ylabel('Number of clause deletions')
plt.legend(loc="upper left")
plt.show()