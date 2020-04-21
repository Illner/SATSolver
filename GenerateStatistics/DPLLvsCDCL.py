import os
import random
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '../')

import MyException
from CNF import CNF
from DPLL import DPLL
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
count_list = [1024, 128, 16, 8]

log_dpll = []
log_cdcl = []

for i in range(len(dictionary_list)):
    print("\n" + str(i))
    log_dpll.append([])
    log_cdcl.append([])
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

        # DPLL
        cnf = CNF(input_formula, unit_propagation_enum=UnitPropagationEnum.WatchedLiterals)
        dpll = DPLL(cnf)
        result = dpll.DPLL()

        if (not cnf.verify(result)):
            raise MyException.SomethingWrongException("Invalid model - DPLL")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - DPLL")

        print("Time: " + str(dpll.time))
        print("Number of decisions: " + str(dpll.number_of_decisions))
        print("Number of steps of unit propagation: " + str(dpll.number_of_steps_of_unit_propagation))
        print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))

        log_dpll[i].append((dpll.time, dpll.number_of_decisions, dpll.number_of_steps_of_unit_propagation, cnf.number_of_checked_clauses))

        print()

        # CDCL
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
            raise MyException.SomethingWrongException("Invalid model - CDCL")

        if (is_sat and result is None):
            raise MyException.SomethingWrongException("Invalid model - CDCL")

        print("Time: " + str(cdcl.time))
        print("Number of decisions: " + str(cdcl.number_of_decisions))
        print("Number of steps of unit propagation: " + str(cdcl.number_of_steps_of_unit_propagation))
        print("Number of checked clauses: " + str(cnf.number_of_checked_clauses))

        log_cdcl[i].append((cdcl.time, cdcl.number_of_decisions, cdcl.number_of_steps_of_unit_propagation, cnf.number_of_checked_clauses))

# Log DPLL
time_y_dpll = []
number_of_decisions_y_dpll = []
number_of_steps_of_unit_propagation_y_dpll = []
number_of_checked_clauses_y_dpll = []

for i in range(len(log_dpll)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0

    for j in range(len(log_dpll[i])):
        time_average += log_dpll[i][j][0]
        number_of_decisions_average += log_dpll[i][j][1]
        number_of_steps_of_unit_propagation_average += log_dpll[i][j][2]
        number_of_checked_clauses_average += log_dpll[i][j][3]
    if (len(log_dpll[i]) != 0):
        time_average /= len(log_dpll[i])
        number_of_decisions_average /= len(log_dpll[i])
        number_of_steps_of_unit_propagation_average /= len(log_dpll[i])
        number_of_checked_clauses_average /= len(log_dpll[i])

    time_y_dpll.append(time_average)
    number_of_decisions_y_dpll.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_dpll.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_dpll.append(number_of_checked_clauses_average)

# Log CDCL
time_y_cdcl = []
number_of_decisions_y_cdcl = []
number_of_steps_of_unit_propagation_y_cdcl = []
number_of_checked_clauses_y_cdcl = []

for i in range(len(log_cdcl)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0
    number_of_checked_clauses_average = 0

    for j in range(len(log_cdcl[i])):
        time_average += log_cdcl[i][j][0]
        number_of_decisions_average += log_cdcl[i][j][1]
        number_of_steps_of_unit_propagation_average += log_cdcl[i][j][2]
        number_of_checked_clauses_average += log_cdcl[i][j][3]
    if (len(log_cdcl[i]) != 0):
        time_average /= len(log_cdcl[i])
        number_of_decisions_average /= len(log_cdcl[i])
        number_of_steps_of_unit_propagation_average /= len(log_cdcl[i])
        number_of_checked_clauses_average /= len(log_cdcl[i])

    time_y_cdcl.append(time_average)
    number_of_decisions_y_cdcl.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y_cdcl.append(number_of_steps_of_unit_propagation_average)
    number_of_checked_clauses_y_cdcl.append(number_of_checked_clauses_average)

print("DPLL")
print("Time: ")
print(time_y_dpll)
print("Number of decisions: ")
print(number_of_decisions_y_dpll)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_dpll)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_dpll)

print()

print("CDCL")
print("Time: ")
print(time_y_cdcl)
print("Number of decisions: ")
print(number_of_decisions_y_cdcl)
print("Number of steps of unit propagation: ")
print(number_of_steps_of_unit_propagation_y_cdcl)
print("Number of checked clauses: ")
print(number_of_checked_clauses_y_cdcl)

# Time
plt.plot(x_axis_variables, time_y_dpll, color="blue", label='DPLL')
plt.plot(x_axis_variables, time_y_cdcl, color="red", label='CDCL')
plt.title('Time')
plt.xlabel('Number of variables')
plt.ylabel('Time (s)')
plt.legend(loc="upper left")
plt.show()

# Number of checked clauses
plt.plot(x_axis_variables, number_of_checked_clauses_y_dpll, color="blue", label='DPLL')
plt.plot(x_axis_variables, number_of_checked_clauses_y_cdcl, color="red", label='CDCL')
plt.title('Number of checked clauses')
plt.xlabel('Number of variables')
plt.ylabel('Number of checked clauses')
plt.legend(loc="upper left")
plt.show()

# Number of decisions
plt.plot(x_axis_variables, number_of_decisions_y_dpll, color="blue", label='DPLL')
plt.plot(x_axis_variables, number_of_decisions_y_cdcl, color="red", label='CDCL')
plt.title('Number of decisions')
plt.xlabel('Number of variables')
plt.ylabel('Number of decisions')
plt.legend(loc="upper left")
plt.show()

# Number of steps of unit propagation
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_dpll, color="blue", label='DPLL')
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y_cdcl, color="red", label='CDCL')
plt.title('Number of steps of unit propagation')
plt.xlabel('Number of variables')
plt.ylabel('Number of steps of unit propagation')
plt.legend(loc="upper left")
plt.show()