import os
import random
import MyException
from CNF import CNF
from CDCL import CDCL
import matplotlib.pyplot as plt
from DerivationTree import DerivationTree
from LogicalSignEnum import LogicalSignEnum
from TseitinEncoding import TseitinEncoding
from ClauseLearningEnum import ClauseLearningEnum
from UnitPropagationEnum import UnitPropagationEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionHowHeuristicEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionWhenHeuristicEnum

path = os.path.join(os.path.dirname(__file__), 'CNF')
dictionary_list = ["20-91", "50-218", "75-325", "100-430"]
# dictionary_list = ["JNH"]
x_axis_variables = [20, 50, 75, 100]
# x_axis_variables = [0]
count_list = [1024, 128, 16, 8]
# count_list = [20]
log_adjacency_list = []
log_watched_literals = []

for i in range(len(dictionary_list)):
    print("\n" + str(i))
    log_adjacency_list.append([])
    log_watched_literals.append([])
    dictionary_path = os.path.join(path, dictionary_list[i])

    for j in range(count_list[i]):
        print("- "  + str(j))
        file = random.choice(os.listdir(dictionary_path))
        # file = "jnh" + str(j + 1) + ".cnf"
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

        # Adjacency list
        cnf = CNF(input_formula, unit_propagation_enum=UnitPropagationEnum.AdjacencyList, clause_learning_enum=ClauseLearningEnum.StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent, clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepShortClauses)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - adjacency list")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - adjacency list")

        print("Time: " + str(cdcl.time))
        print("Number of decisions: " + str(cdcl.number_of_decisions))
        print("Number of steps of unit propagation: " + str(cdcl.number_of_steps_of_unit_propagation))
        print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))

        log_adjacency_list[i].append((cdcl.time, cdcl.number_of_decisions, cdcl.number_of_steps_of_unit_propagation, cnf.number_of_checked_clauses))

        print()
        
        # Watched literals
        cnf = CNF(input_formula, unit_propagation_enum=UnitPropagationEnum.WatchedLiterals, clause_learning_enum=ClauseLearningEnum.StopWhenTheLiteralAtCurrentDecisionLevelHasNoAntecedent, clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepShortClauses)
        cdcl = CDCL(cnf)
        result = cdcl.CDCL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - watched literals")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - watched literals")

        print("Time: " + str(cdcl.time))
        print("Number of decisions: " + str(cdcl.number_of_decisions))
        print("Number of steps of unit propagation: " + str(cdcl.number_of_steps_of_unit_propagation))
        print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))

        log_watched_literals[i].append((cdcl.time, cdcl.number_of_decisions, cdcl.number_of_steps_of_unit_propagation, cnf.number_of_checked_clauses))

# Log adjacency list
time_y_adjacency_list = []
number_of_decisions_y_adjacency_list = []
number_of_steps_of_unit_propagation_y_adjacency_list = []
number_of_checked_clauses_y_adjacency_list = []

for i in range(len(log_adjacency_list)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0

    for j in range(len(log_adjacency_list[i])):
        time_average += log_adjacency_list[i][j][0]
        number_of_decisions_average += log_adjacency_list[i][j][1]
        number_of_steps_of_unit_propagation_average += log_adjacency_list[i][j][2]
        number_of_checked_clauses_average += log_adjacency_list[i][j][3]
    if (len(log_adjacency_list[i]) != 0):
        time_average /= len(log_adjacency_list[i])
        number_of_decisions_average /= len(log_adjacency_list[i])
        number_of_steps_of_unit_propagation_average /= len(log_adjacency_list[i])
        number_of_checked_clauses_average /= len(log_adjacency_list[i])

    time_y_adjacency_list.append(time_average)
    number_of_decisions_y_adjacency_list.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_adjacency_list.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_adjacency_list.append(number_of_checked_clauses_average)

# Log watched literals
time_y_watched_literals = []
number_of_decisions_y_watched_literals = []
number_of_steps_of_unit_propagation_y_watched_literals = []
number_of_checked_clauses_y_watched_literals = []

for i in range(len(log_watched_literals)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0

    for j in range(len(log_watched_literals[i])):
        time_average += log_watched_literals[i][j][0]
        number_of_decisions_average += log_watched_literals[i][j][1]
        number_of_steps_of_unit_propagation_average += log_watched_literals[i][j][2]
        number_of_checked_clauses_average += log_watched_literals[i][j][3]
    if (len(log_watched_literals[i]) != 0):
        time_average /= len(log_watched_literals[i])
        number_of_decisions_average /= len(log_watched_literals[i])
        number_of_steps_of_unit_propagation_average /= len(log_watched_literals[i])
        number_of_checked_clauses_average /= len(log_watched_literals[i])

    time_y_watched_literals.append(time_average)
    number_of_decisions_y_watched_literals.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_watched_literals.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_watched_literals.append(number_of_checked_clauses_average)

print("Adjacency list")
print("Time: ")
print(time_y_adjacency_list)
print("Number of decisions: ")
print(number_of_decisions_y_adjacency_list)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_adjacency_list)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_adjacency_list)

print()

print("Watched literals")
print("Time: ")
print(time_y_watched_literals)
print("Number of decisions: ")
print(number_of_decisions_y_watched_literals)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_watched_literals)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_watched_literals)

# Time
plt.plot(x_axis_variables, time_y_adjacency_list, color="blue", label='Adjacency list')
plt.plot(x_axis_variables, time_y_watched_literals, color="red", label='Watched literals')
plt.title('Time')
plt.xlabel('Number of variables')
plt.ylabel('Time (s)')
plt.legend(loc="upper left")
plt.show()

# Number of checked clauses
plt.plot(x_axis_variables, number_of_checked_clauses_y_adjacency_list, color="blue", label='Adjacency list')
plt.plot(x_axis_variables, number_of_checked_clauses_y_watched_literals, color="red", label='Watched literals')
plt.title('Number of checked clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of checked clauses')
plt.legend(loc="upper left")
plt.show()

# Number of decisions
plt.plot(x_axis_variables, number_of_decisions_y_adjacency_list, color="blue", label='Adjacency list')
plt.plot(x_axis_variables, number_of_decisions_y_watched_literals, color="red", label='Watched literals')
plt.title('Number of decisions')
plt.xlabel('Number of variables')
plt.ylabel('Number of decisions')
plt.legend(loc="upper left")
plt.show()

# Number of steps of unit propagation
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_adjacency_list, color="blue", label='Adjacency list')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_watched_literals, color="red", label='Watched literals')
plt.title('Number of steps of unit propagation')
plt.xlabel('Number of variables')
plt.ylabel('Number of steps of unit propagation')
plt.legend(loc="upper left")
plt.show()