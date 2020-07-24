import time
import statistics
import matplotlib.pyplot as plt
from Applications.EncodeNQueensProblem import EncodeNQueensProblem

from pysat.formula import CNF

from pysat.solvers import Minisat22
from pysat.solvers import Glucose4
from pysat.solvers import Lingeling
from pysat.solvers import Cadical
from pysat.solvers import Minicard
from pysat.solvers import Maplesat
from pysat.solvers import MapleCM
from pysat.solvers import MapleChrono

from CDCL import CDCL
from CNF import CNF as myCNF
from DerivationTree import DerivationTree
from TseitinEncoding import TseitinEncoding
from ClauseLearningEnum import ClauseLearningEnum
from RestartStrategyEnum import RestartStrategyEnum
from UnitPropagationEnum import UnitPropagationEnum
from DecisionHeuristicEnum import DecisionHeuristicEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionHowHeuristicEnum
from ClauseDeletionHeuristicEnum import ClauseDeletionWhenHeuristicEnum

# Variable
min = 1
max = 20
file = False
iteration = 2
max_myCDCL = 10
folder_path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Rozhodovací procedury a verifikace (NAIL094)\Cvičení\Úkoly\task1\nQueensProblem"

x = [x for x in range(min, max + 1)]
x_myCDCL = [x for x in range(min, max_myCDCL + 1)]
solvers_list = ["Minisat", "Glucose", "Lingeling", "CaDiCaL", "Minicard", "Maplesat", "MapleCM", "MapleLCMDistChronoBT", "myCDCL"]
time_list_Minisat = []
time_list_Minisat_parsing = []
time_list_Glucose = []
time_list_Glucose_parsing = []
time_list_Lingeling = []
time_list_Lingeling_parsing = []
time_list_CaDiCaL = []
time_list_CaDiCaL_parsing = []
time_list_Minicard = []
time_list_Minicard_parsing = []
time_list_Maplesat = []
time_list_Maplesat_parsing = []
time_list_MapleCM = []
time_list_MapleCM_parsing = []
time_list_MapleLCMDistChronoBT = []
time_list_MapleLCMDistChronoBT_parsing = []
time_list_myCDCL = []

for i in range(min - 1, max):
    if (file):
        formula = CNF(from_file=folder_path + r"\{0}.cnf".format(i + 1))
    else:
        n_queens_problem = EncodeNQueensProblem(i + 1)
        formula = CNF(from_string=n_queens_problem.DIMACS_format)

    print("{0}".format(i + 1))

    # Minisat
    print("- Minisat")
    time_temp = []
    time_temp_parsing = []
    for _ in range(iteration):
        g = Minisat22()

        start_parsing = time.time()
        g.append_formula(formula)
        start = time.time()
        g.solve()
        end = time.time()

        time_temp.append(end - start)
        time_temp_parsing.append(end - start_parsing)
    time_list_Minisat.append(statistics.mean(time_temp))
    time_list_Minisat_parsing.append(statistics.mean(time_temp_parsing))

    # Glucose
    print("- Glucose")
    time_temp = []
    time_temp_parsing = []
    for _ in range(iteration):
        g = Glucose4()

        start_parsing = time.time()
        g.append_formula(formula)
        start = time.time()
        g.solve()
        end = time.time()

        time_temp.append(end - start)
        time_temp_parsing.append(end - start_parsing)
    time_list_Glucose.append(statistics.mean(time_temp))
    time_list_Glucose_parsing.append(statistics.mean(time_temp_parsing))
    
    # Lingeling
    print("- Lingeling")
    time_temp = []
    time_temp_parsing = []
    for _ in range(iteration):
        g = Lingeling()

        start_parsing = time.time()
        g.append_formula(formula)
        start = time.time()
        g.solve()
        end = time.time()

        time_temp.append(end - start)
        time_temp_parsing.append(end - start_parsing)
    time_list_Lingeling.append(statistics.mean(time_temp))
    time_list_Lingeling_parsing.append(statistics.mean(time_temp_parsing))
    
    # CaDiCaL
    print("- CaDiCaL")
    time_temp = []
    time_temp_parsing = []
    for _ in range(iteration):
        g = Cadical()

        start_parsing = time.time()
        g.append_formula(formula)
        start = time.time()
        g.solve()
        end = time.time()

        time_temp.append(end - start)
        time_temp_parsing.append(end - start_parsing)
    time_list_CaDiCaL.append(statistics.mean(time_temp))
    time_list_CaDiCaL_parsing.append(statistics.mean(time_temp_parsing))

    # Minicard
    print("- Minicard")
    time_temp = []
    time_temp_parsing = []
    for _ in range(iteration):
        g = Minicard()

        start_parsing = time.time()
        g.append_formula(formula)
        start = time.time()
        g.solve()
        end = time.time()

        time_temp.append(end - start)
        time_temp_parsing.append(end - start_parsing)
    time_list_Minicard.append(statistics.mean(time_temp))
    time_list_Minicard_parsing.append(statistics.mean(time_temp_parsing))

    # Maplesat
    print("- Maplesat")
    time_temp = []
    time_temp_parsing = []
    for _ in range(iteration):
        g = Maplesat()

        start_parsing = time.time()
        g.append_formula(formula)
        start = time.time()
        g.solve()
        end = time.time()

        time_temp.append(end - start)
        time_temp_parsing.append(end - start_parsing)
    time_list_Maplesat.append(statistics.mean(time_temp))
    time_list_Maplesat_parsing.append(statistics.mean(time_temp_parsing))

    # MapleCM
    print("- MapleCM")
    time_temp = []
    time_temp_parsing = []
    for _ in range(iteration):
        g = MapleCM()

        start_parsing = time.time()
        g.append_formula(formula)
        start = time.time()
        g.solve()
        end = time.time()

        time_temp.append(end - start)
        time_temp_parsing.append(end - start_parsing)
    time_list_MapleCM.append(statistics.mean(time_temp))
    time_list_MapleCM_parsing.append(statistics.mean(time_temp_parsing))

    # MapleLCMDistChronoBT
    print("- MapleLCMDistChronoBT")
    time_temp = []
    time_temp_parsing = []
    for _ in range(iteration):
        g = MapleChrono()

        start_parsing = time.time()
        g.append_formula(formula)
        start = time.time()
        g.solve()
        end = time.time()

        time_temp.append(end - start)
        time_temp_parsing.append(end - start_parsing)
    time_list_MapleLCMDistChronoBT.append(statistics.mean(time_temp))
    time_list_MapleLCMDistChronoBT_parsing.append(statistics.mean(time_temp_parsing))

    if (i >= max_myCDCL):
        continue
    
    if (file):
        my_file = open(folder_path + r"\{0}.cnf".format(i + 1), "r")
        my_formula = my_file.read()
    else:
        my_formula = n_queens_problem.DIMACS_format
    # myCDCL
    print("- myCDCL")
    time_temp = []
    for _ in range(iteration):
        my_cnf = myCNF(my_formula, unit_propagation_enum=UnitPropagationEnum.WatchedLiterals, clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP, restart_strategy_enum=RestartStrategyEnum.LubyStrategy, clause_deletion_when_heuristic_enum=ClauseDeletionWhenHeuristicEnum.Restart, clause_deletion_how_heuristic_enum=ClauseDeletionHowHeuristicEnum.KeepActiveClauses, decision_heuristic_enum=DecisionHeuristicEnum.eVSIDS)
        my_cdcl = CDCL(my_cnf)

        my_cdcl.CDCL()

        time_temp.append(my_cdcl.time)
    time_list_myCDCL.append(statistics.mean(time_temp))

print("time_list_Minisat")
print(time_list_Minisat)
print("time_list_Minisat_parsing")
print(time_list_Minisat_parsing)

print()

print("time_list_Glucose")
print(time_list_Glucose)
print("time_list_Glucose_parsing")
print(time_list_Glucose_parsing)

print()

print("time_list_Lingeling")
print(time_list_Lingeling)
print("time_list_Lingeling_parsing")
print(time_list_Lingeling_parsing)

print()

print("time_list_CaDiCaL")
print(time_list_CaDiCaL)
print("time_list_CaDiCaL_parsing")
print(time_list_CaDiCaL_parsing)

print()

print("time_list_Minicard")
print(time_list_Minicard)
print("time_list_Minicard_parsing")
print(time_list_Minicard_parsing)

print()

print("time_list_Maplesat")
print(time_list_Maplesat)
print("time_list_Maplesat_parsing")
print(time_list_Maplesat_parsing)

print()

print("time_list_MapleCM")
print(time_list_MapleCM)
print("time_list_MapleCM_parsing")
print(time_list_MapleCM_parsing)

print()

print("time_list_MapleLCMDistChronoBT")
print(time_list_MapleLCMDistChronoBT)
print("time_list_MapleLCMDistChronoBT_parsing")
print(time_list_MapleLCMDistChronoBT_parsing)

print()

print("time_list_myCDCL")
print(time_list_myCDCL)

print()
print()

plt.plot(x, time_list_Minisat, color="blue", label='Minisat')
plt.plot(x, time_list_Glucose, color="red", label='Glucose')
plt.plot(x, time_list_Lingeling, color="purple", label='Lingeling')
plt.plot(x, time_list_CaDiCaL, color="green", label='CaDiCaL')
plt.plot(x, time_list_Minicard, color="yellow", label='Minicard')
plt.plot(x, time_list_Maplesat, color="orange", label='Maplesat')
plt.plot(x, time_list_MapleCM, color="black", label='MapleCM')
plt.plot(x, time_list_MapleLCMDistChronoBT, color="cyan", label='MapleLCMDistChronoBT')
plt.plot(x_myCDCL, time_list_myCDCL, color="brown", label='myCDCL')
plt.title('Time')
plt.xlabel('N-queens problem')
plt.ylabel('Time [s] (log)')
plt.legend(loc="upper left")
plt.yscale('log')
plt.show()

plt.plot(x, time_list_Minisat_parsing, color="blue", label='Minisat')
plt.plot(x, time_list_Glucose_parsing, color="red", label='Glucose')
plt.plot(x, time_list_Lingeling_parsing, color="purple", label='Lingeling')
plt.plot(x, time_list_CaDiCaL_parsing, color="green", label='CaDiCaL')
plt.plot(x, time_list_Minicard_parsing, color="yellow", label='Minicard')
plt.plot(x, time_list_Maplesat_parsing, color="orange", label='Maplesat')
plt.plot(x, time_list_MapleCM_parsing, color="black", label='MapleCM')
plt.plot(x, time_list_MapleLCMDistChronoBT_parsing, color="cyan", label='MapleLCMDistChronoBT')
plt.plot(x_myCDCL, time_list_myCDCL, color="brown", label='myCDCL')
plt.title('Time (including parsing)')
plt.xlabel('N-queens problem')
plt.ylabel('Time [s] (log)')
plt.legend(loc="upper left")
plt.yscale('log')
plt.show()