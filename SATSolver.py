import matplotlib.pyplot as plt

from CNF import CNF
from CDCL import CDCL
from ClauseLearningEnum import ClauseLearningEnum
from Applications.EncodeNQueensProblem import EncodeNQueensProblem

folder = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Rozhodovací procedury a verifikace (NAIL094)\Cvičení\SATSolver\CNF\nQueensProblem"
number_of_clauses_list = []

for i in range(1, 5):
    n_queen_problem = EncodeNQueensProblem(i)
    n_queen_problem.save_to_file(folder + r"\{0}.cnf".format(i))

    number_of_clauses = n_queen_problem.number_of_clauses
    number_of_clauses_list.append(number_of_clauses)

    print("{0}".format(i))

    cnf = CNF(n_queen_problem.DIMACS_format, clause_learning_enum=ClauseLearningEnum.StopAtTheFirstUIP)
    cdcl = CDCL(cnf)
    result = cdcl.CDCL()

print()
print("Number of clauses list: ")
print(number_of_clauses_list)