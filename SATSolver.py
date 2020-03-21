from DerivationTree import DerivationTree
from LogicalSignEnum import LogicalSignEnum
from TseitinEncoding import TseitinEncoding
import matplotlib.pyplot as plt
import os
import random
from DPLL import DPLL
from CNF import CNF
import MyException

path = os.path.join(os.path.dirname(__file__), 'CNF')
dictionary_list = ["20-91", "50-218", "75-325", "100-430", "125-538"]
x_axis_variables = [20, 50, 75, 100, 125]
count_list = [256, 64, 16, 4, 1]
log = []

for i in range(len(dictionary_list)):
    print(i)
    dictionary_path = os.path.join(path, dictionary_list[i])
    log.append([])
    for j in range(count_list[i]):
        print("- "  + str(j))
        file = random.choice(os.listdir(dictionary_path))
        file_path = os.path.join(dictionary_path, file)

        with open(file_path, "r") as input_file:
            input_formula = input_file.read()

        cnf = CNF(input_formula)
        dpll = DPLL(cnf)
        result = dpll.DPLL()

        log[i].append((dpll.time, dpll.number_of_decisions, dpll.number_of_steps_of_unit_propagation))

time_y = []
number_of_decisions_y = []
number_of_steps_of_unit_propagation_y = []

for i in range(len(log)):
    time_average = 0
    number_of_decisions_average = 0
    number_of_steps_of_unit_propagation_average = 0

    for j in range(len(log[i])):
        time_average += log[i][j][0]
        number_of_decisions_average += log[i][j][1]
        number_of_steps_of_unit_propagation_average += log[i][j][2]
    if (len(log[i]) != 0):
        time_average /= len(log[i])
        number_of_decisions_average /= len(log[i])
        number_of_steps_of_unit_propagation_average /= len(log[i])

    time_y.append(time_average)
    number_of_decisions_y.append(number_of_decisions_average)
    number_of_steps_of_unit_propagation_y.append(number_of_steps_of_unit_propagation_average)

print(time_y)
print(number_of_decisions_y)
print(number_of_steps_of_unit_propagation_y)

# Time
plt.plot(x_axis_variables, time_y, color="blue")
plt.title('Time')
plt.xlabel('Number of variables')
plt.ylabel('Time (s)')
plt.show()

# Number of decisions
plt.plot(x_axis_variables, number_of_decisions_y, color="blue")
plt.title('Number of decisions')
plt.xlabel('Number of variables')
plt.ylabel('Number of decisions')
plt.show()

# Number of decisions
plt.plot(x_axis_variables, number_of_steps_of_unit_propagation_y, color="blue")
plt.title('Number of steps of unit propagation')
plt.xlabel('Number of variables')
plt.ylabel('Number of steps of unit propagation')
plt.show()